import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_md")

class SemanticSearch:
    def __init__(self, resume_data):
        self.resume_data = resume_data
        self.document_vectors = [nlp(resume["resume_text"]).vector for resume in self.resume_data]

    def search(self, query):
        if not query:
            return []

        query_vector = nlp(query).vector
        similarities = cosine_similarity([query_vector], self.document_vectors)[0]
        results = [(resume, similarity) for resume, similarity in zip(self.resume_data, similarities)]

        # Adjust threshold dynamically based on maximum similarity score
        if results:
            max_similarity = max(similarity for _, similarity in results)
            threshold = max(0.3, max_similarity - 0.1)
        else:
            threshold = 0

        matching_results = [(resume, similarity) for resume, similarity in results if similarity > threshold]
        matching_results.sort(key=lambda x: x[1], reverse=True)
        return matching_results