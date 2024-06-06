import os
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to extract text and generate a thumbnail from a resume PDF
def extract_text_and_thumbnail_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()

            # Generate a thumbnail from the first page
            pix = doc[0].get_pixmap()
            thumbnail_path = file_path.replace(".pdf", ".png")
            pix.save(thumbnail_path)

        return {"filename": os.path.basename(file_path), "text": text, "thumbnail": thumbnail_path}
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to load and preprocess resumes using parallel processing
def load_and_preprocess_resumes(directory):
    resume_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(".pdf")]
    resumes = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(extract_text_and_thumbnail_from_pdf, file): file for file in resume_files}
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                resumes.append(result)
    return resumes

# Directory containing the resumes
resume_directory = 'data/resume'

# Load and preprocess resumes
resumes = load_and_preprocess_resumes(resume_directory)

# Initialize the model for creating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings for all resume texts in batches to optimize memory usage
resume_texts = [resume['text'] for resume in resumes]
batch_size = 64  # Adjust the batch size according to your system's memory capacity
resume_embeddings = []

for i in range(0, len(resume_texts), batch_size):
    batch_embeddings = model.encode(resume_texts[i:i+batch_size], convert_to_numpy=True)
    resume_embeddings.append(batch_embeddings)

resume_embeddings = np.vstack(resume_embeddings)

# Save the resumes and embeddings
with open('resumes.pkl', 'wb') as f:
    pickle.dump(resumes, f)
np.save('resume_embeddings.npy', resume_embeddings)

# Initialize FAISS index for semantic search
dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)
index.add(np.array(resume_embeddings, dtype=np.float32))

# Save the FAISS index
faiss.write_index(index, 'faiss_index.idx')

print("Model training and preprocessing completed successfully!")
