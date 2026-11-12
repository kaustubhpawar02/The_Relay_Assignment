
import csv
from pathlib import Path

from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever
from evaluation_questions import evaluation_questions

documents = load_papers()
chunks = chunk_documents(documents)

retriever = PaperRetriever(chunks)

results = []

for item in evaluation_questions:
    question = item["question"]
    expected_paper = item["paper"]

    retrieved = retriever.search(question, top_k=3)

    correct_paper_found = any(
        expected_paper in result["paper_id"].lower()
        for result in retrieved
    )

    results.append({
        "question": question,
        "expected_paper": expected_paper,
        "retrieved_papers": " | ".join(
            result["paper_id"] for result in retrieved
        ),
        "retrieved_pages": " | ".join(
            str(result["page"]) for result in retrieved
        ),
        "top_score": round(retrieved[0]["score"], 4) if retrieved else 0,
        "expected_paper_found": correct_paper_found
    })

    print("\nQuestion:", question)
    print("Expected paper:", expected_paper)

    for result in retrieved:
        print(
            "Retrieved:",
            result["paper_id"],
            "| Page:",
            result["page"],
            "| Score:",
            round(result["score"], 4)
        )

    print("Expected paper found:", correct_paper_found)


output_file = Path(__file__).resolve().parent.parent / "results" / "retrieval_evaluation.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

correct = sum(
    result["expected_paper_found"]
    for result in results
)

print("\n========== EVALUATION SUMMARY ==========")
print("Total questions:", len(results))
print("Expected paper found:", correct)
print("Expected paper not found:", len(results) - correct)
print("Paper retrieval hit rate:", round(correct / len(results) * 100, 2), "%")
print("Saved to:", output_file)
