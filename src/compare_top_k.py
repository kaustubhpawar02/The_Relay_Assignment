
import csv
from pathlib import Path

from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever
from evaluation_questions import evaluation_questions

documents = load_papers()

chunks = chunk_documents(
    documents,
    chunk_size=500,
    overlap=100
)

retriever = PaperRetriever(chunks)

top_k_values = [1, 3, 5]

all_results = []

for top_k in top_k_values:
    print(f"\nTesting top_k = {top_k}")

    correct = 0
    total_words = 0
    total_passages = 0

    for item in evaluation_questions:
        retrieved = retriever.search(
            item["question"],
            top_k=top_k
        )

        found = any(
            item["paper"] in result["paper_id"].lower()
            for result in retrieved
        )

        if found:
            correct += 1

        total_passages += len(retrieved)

        total_words += sum(
            len(result["text"].split())
            for result in retrieved
        )

    hit_rate = correct / len(evaluation_questions) * 100
    average_words = total_words / len(evaluation_questions)
    average_passages = total_passages / len(evaluation_questions)

    result = {
        "top_k": top_k,
        "correct_papers": correct,
        "total_questions": len(evaluation_questions),
        "hit_rate_percent": round(hit_rate, 2),
        "average_passages": round(average_passages, 2),
        "average_context_words": round(average_words, 2)
    }

    all_results.append(result)

    print("Correct papers:", correct)
    print("Hit rate:", round(hit_rate, 2), "%")
    print("Average passages:", round(average_passages, 2))
    print("Average context words:", round(average_words, 2))


output_file = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "top_k_comparison.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_results[0].keys())
    writer.writeheader()
    writer.writerows(all_results)

print("\n========== TOP-K COMPARISON ==========")

for result in all_results:
    print(
        "Top-k:", result["top_k"],
        "| Hit rate:", result["hit_rate_percent"], "%",
        "| Average words:", result["average_context_words"]
    )

print("\nSaved to:", output_file)
