
import time
import uuid
from datetime import datetime, timezone

from standin_model import StandInModel
from results_logger import log_result

model = StandInModel()


def send_request(request_number):

    request_id = str(uuid.uuid4())
    start_time = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()

    status = "ok"

    try:
        result = model.generate("What is Machine Learning?")
        print("Status:", result["status"])

    except Exception as error:
        print("Error:", error)

        if "429" in str(error):
            status = "rate_limited"
        else:
            status = "error"

    total_time = (time.perf_counter() - start) * 1000

    log_result({
        "request_id": request_id,
        "scenario": "rate_limit_test",
        "source": "stand-in",
        "start_time": start_time,
        "first_token_ms": "",
        "total_ms": round(total_time, 2),
        "status": status,
        "retries": 0,
        "tokens_in": "",
        "tokens_out": "",
        "retrieval_setting": "not_applicable",
        "answer_grade": ""
    })


for i in range(1, 6):

    print(f"\nRequest {i}:")
    send_request(i)

print("\nWaiting 10 seconds for recovery...")
time.sleep(10)

print("\nRequest 6 after recovery:")
send_request(6)

print("\nAll results saved to results/results.csv")
