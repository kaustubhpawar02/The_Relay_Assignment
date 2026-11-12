
from pathlib import Path
from pypdf import PdfReader


PAPERS = {
    "attention": {
        "title": "Attention Is All You Need",
        "filename": "attention_is_all_you_need.pdf"
    },
    "moshi": {
        "title": "Moshi: a speech-text foundation model for real-time dialogue",
        "filename": "moshi.pdf"
    },
    "dynamic_chunking": {
        "title": "Dynamic Chunking for End-to-End Hierarchical Sequence Modeling",
        "filename": "dynamic_chunking.pdf"
    }
}


BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "papers"


def load_papers():
    documents = []

    for paper_id, paper_info in PAPERS.items():
        file_path = PAPERS_DIR / paper_info["filename"]

        if not file_path.exists():
            raise FileNotFoundError(f"Paper not found: {file_path}")

        reader = PdfReader(str(file_path))

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            if page_text.strip():
                documents.append({
                    "paper_id": paper_id,
                    "title": paper_info["title"],
                    "page": page_number,
                    "text": page_text
                })

    return documents


if __name__ == "__main__":
    documents = load_papers()

    print("Papers loaded successfully!")
    print("Total pages extracted:", len(documents))

    for document in documents:
        print(
            document["title"],
            "| Page:", document["page"]
        )

    print("\nSample extracted text:\n")
    print(documents[0]["text"][:500])
