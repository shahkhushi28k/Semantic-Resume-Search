import os
import numpy as np
import streamlit as st
import base64
import re
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Load resumes and embeddings
with open('resumes.pkl', 'rb') as f:
    resumes = pickle.load(f)
resume_embeddings = np.load('resume_embeddings.npy')

# Initialize model and FAISS index
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('faiss_index.idx')

# Streamlit interface
st.title('Resume Semantic Search')

# Input field for search query
query = st.text_input('Whom would you like to hire? (Enter skills or experience)')

# Function to perform semantic search for a given query
def search_resumes(query, k=5):
    # Encode query and perform search
    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding.astype(np.float32), k)
    return I[0]

# Function to get matching resumes based on a query
def get_matching_resumes(query):
    if 'phd' in query.lower():
        # Search specifically for resumes mentioning 'phd'
        return [resume for resume in resumes if 'phd' in resume['text'].lower()]
    else:
        # Perform semantic search
        indices = search_resumes(query)
        return [resumes[i] for i in indices]

# Function to create a download link for a resume
def create_download_link(file_path):
    with open(file_path, "rb") as file:
        encoded_pdf = base64.b64encode(file.read()).decode('utf-8')
    return f'<a href="data:application/pdf;base64,{encoded_pdf}" download="{os.path.basename(file_path)}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Download Resume</a>'

# Function to highlight keywords in text
def highlight_keywords(text, keywords):
    for keyword in keywords:
        regex = re.compile(re.escape(keyword), re.IGNORECASE)
        text = regex.sub(f'<span style="background-color: yellow;">{keyword}</span>', text)
    return text

# Display matching resumes when query is provided
if st.button("Search"):
    if query:
        matching_resumes = get_matching_resumes(query)
        if not matching_resumes:
            st.write("No matching resumes found.")
        else:
            st.write("Search Results:")
            keywords = query.split()  # Split query into individual keywords
            for idx, resume in enumerate(matching_resumes, 1):
                # Highlight keywords and display resume details
                highlighted_text = highlight_keywords(resume['text'][:500], keywords)
                st.markdown(f"""
                <div style='border: 2px solid #4CAF50; padding: 10px; border-radius: 10px; margin-bottom: 20px;'>
                    <h3>{idx}. Resume: {resume['filename']}</h3>
                    <img src="data:image/png;base64,{base64.b64encode(open(resume['thumbnail'], 'rb').read()).decode('utf-8')}" style='display: block; margin: 0 auto; width: 300px; height: auto; padding-bottom: 10px;' />
                    <p style='text-align: justify;'>{highlighted_text}...</p>
                    {create_download_link(os.path.join('data/resume', resume['filename']))}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Please enter a search query.")
