from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever

documents = load_papers()
chunks = chunk_documents(documents, chunk_size=500, overlap=100)

retriever = PaperRetriever(chunks)

question = "Why is hierarchical sequence modeling useful?"

results = retriever.search(question, top_k=3)

for i, passage in enumerate(results, start=1):
    print(f"\nPassage {i}")
    print("Paper:", passage["title"])
    print("Page:", passage["page"])
    print("Score:", passage["score"])
    print("Text:", passage["text"])