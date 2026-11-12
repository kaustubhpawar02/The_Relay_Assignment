
import csv
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever
from llm_client import generate_answer
from results_logger import log_result

BASE_DIR = Path(__file__).resolve().parent.parent

settings = [
    {"name": "small", "chunk_size": 500, "overlap": 100, "top_k": 3},
    {"name": "medium", "chunk_size": 1000, "overlap": 200, "top_k": 3},
    {"name": "large", "chunk_size": 1500, "overlap": 300, "top_k": 3}
]

questions = [
    {
        "paper": "attention",
        "question": "How does scaled dot-product attention work?"
    },
    {
        "paper": "moshi",
        "question": "What is the role of the Mimi audio codec in Moshi?"
    },
    {
        "paper": "dynamic_chunking",
        "question": "What is dynamic chunking in sequence modeling?"
    }
]

output_file = BASE_DIR / "results" / "retrieval_real_comparison.csv"

documents = load_papers()

columns = [
    "setting",
    "chunk_size",
    "overlap",
    "top_k",
    "question",
    "expected_paper",
    "retrieved_papers",
    "paper_hit",
    "context_words",
    "tokens_in",
    "tokens_out",
    "ttft_ms",
    "total_ms",
    "status"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()

    for setting in settings:

        print("\n========== SETTING:", setting["name"], "==========")

        chunks = chunk_documents(
            documents,
            chunk_size=setting["chunk_size"],
            overlap=setting["overlap"]
        )

        retriever = PaperRetriever(chunks)

        for item in questions:

            question = item["question"]
            expected_paper = item["paper"]

            passages = retriever.search(
                question,
                top_k=setting["top_k"]
            )

            retrieved_papers = list(dict.fromkeys(
                passage["paper_id"] for passage in passages
            ))

            paper_hit = any(
                expected_paper in paper.lower()
                for paper in retrieved_papers
            )

            context_words = sum(
                len(passage["text"].split())
                for passage in passages
            )

            request_id = str(uuid.uuid4())
            start_time = datetime.now(timezone.utc).isoformat()

            print("\nQuestion:", question)
            print("Context words:", context_words)
            print("Expected paper found:", paper_hit)

            try:
                result = generate_answer(question, passages)

                status = "ok"

                print("TTFT:", result["ttft_ms"], "ms")
                print("Total time:", result["total_time_ms"], "ms")
                print("Input tokens:", result["tokens_in"])
                print("Output tokens:", result["tokens_out"])

                log_result({
                    "request_id": request_id,
                    "scenario": "retrieval_comparison",
                    "source": "real",
                    "start_time": start_time,
                    "first_token_ms": result["ttft_ms"],
                    "total_ms": result["total_time_ms"],
                    "status": status,
                    "retries": 0,
                    "tokens_in": result["tokens_in"],
                    "tokens_out": result["tokens_out"],
                    "retrieval_setting": setting["name"],
                    "answer_grade": ""
                })

                row = {
                    "setting": setting["name"],
                    "chunk_size": setting["chunk_size"],
                    "overlap": setting["overlap"],
                    "top_k": setting["top_k"],
                    "question": question,
                    "expected_paper": expected_paper,
                    "retrieved_papers": ", ".join(retrieved_papers),
                    "paper_hit": paper_hit,
                    "context_words": context_words,
                    "tokens_in": result["tokens_in"],
                    "tokens_out": result["tokens_out"],
                    "ttft_ms": result["ttft_ms"],
                    "total_ms": result["total_time_ms"],
                    "status": status
                }

            except Exception as error:

                error_text = str(error)

                if "429" in error_text or "rate limit" in error_text.lower():
                    status = "rate_limited"
                else:
                    status = "error"

                print("Request failed:", error_text)

                log_result({
                    "request_id": request_id,
                    "scenario": "retrieval_comparison",
                    "source": "real",
                    "start_time": start_time,
                    "first_token_ms": "",
                    "total_ms": "",
                    "status": status,
                    "retries": 0,
                    "tokens_in": "",
                    "tokens_out": "",
                    "retrieval_setting": setting["name"],
                    "answer_grade": ""
                })

                row = {
                    "setting": setting["name"],
                    "chunk_size": setting["chunk_size"],
                    "overlap": setting["overlap"],
                    "top_k": setting["top_k"],
                    "question": question,
                    "expected_paper": expected_paper,
                    "retrieved_papers": ", ".join(retrieved_papers),
                    "paper_hit": paper_hit,
                    "context_words": context_words,
                    "tokens_in": "",
                    "tokens_out": "",
                    "ttft_ms": "",
                    "total_ms": "",
                    "status": status
                }

            writer.writerow(row)
            file.flush()

            time.sleep(10)

print("\nComparison completed.")
print("Detailed results saved to:", output_file)
print("Request log updated: results/results.csv")
