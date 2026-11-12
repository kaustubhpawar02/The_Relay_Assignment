
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from document_loader import load_papers
from chunking import chunk_documents


class PaperRetriever:

    def __init__(self, chunks):
        self.chunks = chunks

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.chunk_vectors = self.vectorizer.fit_transform(
            [chunk["text"] for chunk in chunks]
        )

    def search(self, question, top_k=3):
        question_vector = self.vectorizer.transform([question])

        scores = cosine_similarity(
            question_vector,
            self.chunk_vectors
        ).flatten()

        top_indices = scores.argsort()[::-1][:top_k]

        results = []

        for index in top_indices:
            if scores[index] > 0:
                result = self.chunks[index].copy()
                result["score"] = float(scores[index])
                results.append(result)

        return results



if __name__ == "__main__":
    documents = load_papers()
    chunks = chunk_documents(documents)

    print("Documents loaded:", len(documents))
    print("Chunks created:", len(chunks))

    retriever = PaperRetriever(chunks)

    question = "What is the Transformer architecture?"
    results = retriever.search(question, top_k=3)

    print("\nQuestion:", question)

    for result in results:
        print("\nPaper:", result["title"])
        print("Page:", result["page"])
        print("Similarity:", round(result["score"], 4))
        print("Passage:", result["text"][:300])
