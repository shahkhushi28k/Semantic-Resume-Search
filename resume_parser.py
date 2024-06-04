import os
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfReader

class ResumeParser:
    def __init__(self):
        self.resume_data = []

    def parse_resume(self, filename, resume_text):
        self.resume_data.append({"file_name": filename, "resume_text": resume_text})

    def parse_resumes_from_folder(self, folder_path):
        """
        Parses resumes from a folder in a background thread using ThreadPoolExecutor.
        """
        with ThreadPoolExecutor() as executor:
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf"):
                    executor.submit(self.parse_single_resume, folder_path, filename)

    def parse_single_resume(self, folder_path, filename):
        try:
            with open(os.path.join(folder_path, filename), "rb") as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                self.parse_resume(filename, text)
        except Exception as e:
            print(f"Error reading {filename}: {e}")