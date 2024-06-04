import streamlit as st
from resume_parser import ResumeParser
from semantic_search import SemanticSearch
from streamlit_frontend import StreamlitFrontend

if __name__ == "__main__":
    frontend = StreamlitFrontend(None)
    frontend.search()