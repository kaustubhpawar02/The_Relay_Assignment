
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
        model.generate("What is Machine Learning?")
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
        "scenario": "failure_test",
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


print("Starting simulated failure test...")

for i in range(1, 21):
    send_request(i)
    time.sleep(3.5)

print("\nFailure test completed.")
