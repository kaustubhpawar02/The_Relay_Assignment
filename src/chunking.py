
def chunk_documents(documents, chunk_size=1000, overlap=200):
    chunks = []

    for document in documents:
        text = document["text"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                boundary = text.rfind(" ", start, end)

                if boundary > start:
                    end = boundary

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": len(chunks) + 1,
                    "paper_id": document["paper_id"],
                    "title": document["title"],
                    "page": document["page"],
                    "text": chunk_text
                })

            if end >= len(text):
                break

            start = end - overlap

    return chunks
