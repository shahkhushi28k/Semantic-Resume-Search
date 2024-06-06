##Resume Semantic Search

This project is a web-based application for performing semantic search on resumes using natural language queries. The application leverages machine learning models to encode resumes and queries, and it uses FAISS for efficient similarity search. The web interface is built with Streamlit.

**Features**

Semantic Search: Search resumes based on skills, experience, and other criteria using natural language.
Resume Display: View resume details including name, email, contact, skills, and education.
Keyword Highlighting: Keywords from the search query are highlighted in the resume text.
Similarity Score: Each resume is accompanied by a similarity score indicating how closely it matches the query.
Downloadable Resumes: Provides links to download the resumes as PDF files.


**Setup and Installation**

1. Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/resume-semantic-search.git
cd resume-semantic-search

2. Install Dependencies:
Make sure you have Python 3.7 or higher installed. Then, install the required Python packages using:

bash
Copy code
pip install -r requirements.txt

3. Prepare Data:
Ensure you have the following files in the project directory:

resumes.pkl: A pickle file containing a list of resumes. Each resume should be a dictionary with keys text, name, email, contact, skills, education, filename, and thumbnail.
resume_embeddings.npy: A numpy file containing the embeddings of the resumes.
faiss_index.idx: A FAISS index file built from the resume embeddings.

4. Run the Application:

bash
Copy code
streamlit run app.py


**Usage**

Open the web application in your browser. The default URL is http://localhost:8501.
Enter your search query in the input field and click the "Search" button.
The application will display a list of matching resumes, each with highlighted keywords, a similarity score, and a download link for the resume PDF.
Code Overview
app.py: The main application file that sets up the Streamlit interface and handles search functionality.
highlight_keywords(text, keywords): Highlights the specified keywords in the given text.
search_resumes(query, k=5): Performs semantic search on the resumes using FAISS.
get_matching_resumes(query): Retrieves matching resumes based on the query. Special handling is done for queries mentioning "phd".
create_download_link(file_path): Creates a download link for the resume PDF.


**Dependencies**

numpy
streamlit
sentence-transformers
faiss
pickle
re
base64
os


**Acknowledgements**

This project uses the Sentence Transformers library for encoding text.
The FAISS library by Facebook AI Research is used for efficient similarity search.
Streamlit is used for building the web interface.
Feel free to modify the README.md file as per your project's specific details and requirements.
