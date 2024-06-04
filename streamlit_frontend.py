import streamlit as st
from resume_parser import ResumeParser
from semantic_search import SemanticSearch

class StreamlitFrontend:
    def __init__(self, semantic_search):
        self.semantic_search = semantic_search

    @st.cache_data
    def _load_resume_data(_self, folder_path):
        parser = ResumeParser()
        parser.parse_resumes_from_folder(folder_path)
        return parser.resume_data

    def search(self):
        st.title("Semantic Resume Search")
        query = st.text_input("Whom would you like to hire? (Enter skills or experience)")
        if st.button("Search"):
            resume_data = self._load_resume_data("data/resumes")  # Replace with your actual resume folder path
            search_engine = SemanticSearch(resume_data)
            results = search_engine.search(query)
            if not results:
                st.write("No matching resumes found.")
            else:
                st.write("Search Results:")
                for idx, (result, similarity) in enumerate(results, 1):
                    st.write(f"{idx}. Resume: {result['file_name']}")
                    st.write(f"Similarity: {similarity:.2f}")
                    st.write(f"Preview: {result['resume_text'][:500]}...")
                    download_button = st.button(f"Download Resume {idx}")
                    if download_button:
                        self.download_resume(result)

    def download_resume(self, result):
        file_path = os.path.join("data", "resumes", result["file_name"])
        with open(file_path, "rb") as file:
            resume_content = file.read()
        st.download_button(label="Download", data=resume_content, file_name=result["file_name"])