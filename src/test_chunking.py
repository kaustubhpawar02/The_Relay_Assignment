
from document_loader import load_papers
from chunking import chunk_documents

documents = load_papers()

chunks = chunk_documents(
    documents,
    chunk_size=1000,
    overlap=200
)

print("Total documents:", len(documents))
print("Total chunks:", len(chunks))

print("\nFirst chunk:")
print(chunks[0]["text"][:500])

print("\nChunk source:")
print("Paper:", chunks[0]["title"])
print("Page:", chunks[0]["page"])
