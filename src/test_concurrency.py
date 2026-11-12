
import time
import uuid
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        print(f"Request {request_number}: Successful")

    except Exception as error:
        print(f"Request {request_number}: {error}")

        if "429" in str(error):
            status = "rate_limited"
        else:
            status = "error"

    total_time = (time.perf_counter() - start) * 1000

    log_result({
        "request_id": request_id,
        "scenario": "burst",
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

    return status


print("Starting 5 concurrent requests...")

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(send_request, i)
        for i in range(1, 6)
    ]

    for future in as_completed(futures):
        future.result()

print("\nConcurrent test completed.")
