
import uuid
from datetime import datetime, timezone

from document_loader import load_papers
from chunking import chunk_documents
from retriever import PaperRetriever
from llm_client import generate_answer
from results_logger import log_result

documents = load_papers()
chunks = chunk_documents(documents)

retriever = PaperRetriever(chunks)

question = "What is the Transformer architecture?"

top_k = 3
passages = retriever.search(question, top_k=top_k)

request_id = str(uuid.uuid4())
start_time = datetime.now(timezone.utc).isoformat()

try:
    result = generate_answer(question, passages)

    print("\nQUESTION:")
    print(question)

    print("\nGROQ ANSWER:")
    print(result["answer"])

    print("\nPERFORMANCE METRICS:")
    print("TTFT (ms):", result["ttft_ms"])
    print("Total time (ms):", result["total_time_ms"])
    print("Generation time (ms):", result["generation_time_ms"])
    print("Input tokens:", result["tokens_in"])
    print("Output tokens:", result["tokens_out"])

    log_result({
        "request_id": request_id,
        "scenario": "initial_test",
        "source": "real",
        "start_time": start_time,
        "first_token_ms": result["ttft_ms"],
        "total_ms": result["total_time_ms"],
        "status": "ok",
        "retries": 0,
        "tokens_in": result["tokens_in"],
        "tokens_out": result["tokens_out"],
        "retrieval_setting": f"top_k={top_k}",
        "answer_grade": ""
    })

    print("\nResult successfully saved to results/results.csv")

except Exception as error:
    log_result({
        "request_id": request_id,
        "scenario": "initial_test",
        "source": "real",
        "start_time": start_time,
        "first_token_ms": "",
        "total_ms": "",
        "status": "error",
        "retries": 0,
        "tokens_in": "",
        "tokens_out": "",
        "retrieval_setting": f"top_k={top_k}",
        "answer_grade": ""
    })

    print("\nRequest failed:", error)
