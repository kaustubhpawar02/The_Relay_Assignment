
import csv
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone

from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever
from evaluation_questions import evaluation_questions
from llm_client import generate_answer
from results_logger import log_result

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "results" / "answer_evaluation.csv"

documents = load_papers()

chunks = chunk_documents(
    documents,
    chunk_size=500,
    overlap=100
)

retriever = PaperRetriever(chunks)

answer_results = []

for number, item in enumerate(evaluation_questions, start=1):

    question = item["question"]
    expected_paper = item["paper"]

    request_id = str(uuid.uuid4())
    start_time = datetime.now(timezone.utc).isoformat()

    retrieved = retriever.search(question, top_k=3)

    print("\n" + "=" * 60)
    print(f"Question {number}/15: {question}")
    print("=" * 60)

    status = "ok"
    answer = ""
    ttft = ""
    total_time = ""
    tokens_in = ""
    tokens_out = ""

    start = time.perf_counter()

    try:
        result = generate_answer(question, retrieved)

        answer = result["answer"]
        ttft = result["ttft_ms"]
        total_time = result["total_time_ms"]
        tokens_in = result["tokens_in"]
        tokens_out = result["tokens_out"]

        print("\nAnswer:\n", answer)
        print("\nTTFT:", ttft, "ms")
        print("Total time:", total_time, "ms")
        print("Input tokens:", tokens_in)
        print("Output tokens:", tokens_out)

    except Exception as error:
        status = "error"
        total_time = round(
            (time.perf_counter() - start) * 1000, 2
        )
        answer = str(error)

        print("Request failed:", error)

    log_result({
        "request_id": request_id,
        "scenario": "answer_evaluation",
        "source": "real",
        "start_time": start_time,
        "first_token_ms": ttft,
        "total_ms": total_time,
        "status": status,
        "retries": 0,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "retrieval_setting": "chunk=500,overlap=100,top_k=3",
        "answer_grade": ""
    })

    answer_results.append({
        "request_id": request_id,
        "question": question,
        "expected_paper": expected_paper,
        "retrieved_pages": " | ".join(
            f"{p['paper_id']} p.{p['page']}" for p in retrieved
        ),
        "answer": answer,
        "ttft_ms": ttft,
        "total_ms": total_time,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "status": status,
        "answer_grade": ""
    })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=answer_results[0].keys()
        )
        writer.writeheader()
        writer.writerows(answer_results)

    print("\nSaved answer evaluation progress.")

    if number < len(evaluation_questions):
        print("Waiting 6 seconds before the next request...")
        time.sleep(6)

print("\n========== ANSWER EVALUATION COMPLETED ==========")
print("Total questions:", len(answer_results))
print("Successful:", sum(r["status"] == "ok" for r in answer_results))
print("Failed:", sum(r["status"] != "ok" for r in answer_results))
print("Saved to:", OUTPUT_FILE)
