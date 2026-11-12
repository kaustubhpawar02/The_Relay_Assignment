
import csv
from pathlib import Path

from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever
from evaluation_questions import evaluation_questions

documents = load_papers()

settings = [
    {"name": "small", "chunk_size": 500, "overlap": 100, "top_k": 3},
    {"name": "medium", "chunk_size": 1000, "overlap": 200, "top_k": 3},
    {"name": "large", "chunk_size": 1500, "overlap": 300, "top_k": 3}
]

all_results = []

for setting in settings:
    print("\nTesting:", setting["name"])

    chunks = chunk_documents(
        documents,
        chunk_size=setting["chunk_size"],
        overlap=setting["overlap"]
    )

    retriever = PaperRetriever(chunks)

    correct = 0
    total_tokens = 0
    total_passages = 0

    for item in evaluation_questions:
        retrieved = retriever.search(
            item["question"],
            top_k=setting["top_k"]
        )

        found = any(
            item["paper"] in result["paper_id"].lower()
            for result in retrieved
        )

        if found:
            correct += 1

        total_passages += len(retrieved)

        total_tokens += sum(
            len(result["text"].split())
            for result in retrieved
        )

    hit_rate = correct / len(evaluation_questions) * 100
    average_tokens = total_tokens / len(evaluation_questions)
    average_passages = total_passages / len(evaluation_questions)

    result = {
        "setting": setting["name"],
        "chunk_size": setting["chunk_size"],
        "overlap": setting["overlap"],
        "top_k": setting["top_k"],
        "total_chunks": len(chunks),
        "correct_papers": correct,
        "total_questions": len(evaluation_questions),
        "hit_rate_percent": round(hit_rate, 2),
        "average_passages": round(average_passages, 2),
        "average_context_words": round(average_tokens, 2)
    }

    all_results.append(result)

    print("Total chunks:", len(chunks))
    print("Correct papers:", correct)
    print("Hit rate:", round(hit_rate, 2), "%")
    print("Average passages:", round(average_passages, 2))
    print("Average context words:", round(average_tokens, 2))


output_file = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "retrieval_settings.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_results[0].keys())
    writer.writeheader()
    writer.writerows(all_results)

print("\n========== COMPARISON SUMMARY ==========")

for result in all_results:
    print(
        result["setting"],
        "| Hit rate:", result["hit_rate_percent"], "%",
        "| Average context words:", result["average_context_words"]
    )

print("\nSaved to:", output_file)
