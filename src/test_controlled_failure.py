
import time
from datetime import datetime, timezone

from standin_model import StandInModel
from results_logger import log_result

model = StandInModel()

# Force the next request to fail
model.failure_probability = 1.0

start_time = time.perf_counter()
start_timestamp = datetime.now(timezone.utc).isoformat()

try:
    model.generate("Test a controlled service failure")

except Exception as error:
    total_time = (time.perf_counter() - start_time) * 1000

    print("Expected failure:", error)

    log_result({
        "request_id": "controlled_failure_001",
        "scenario": "controlled_failure",
        "source": "stand-in",
        "start_time": start_timestamp,
        "first_token_ms": None,
        "total_ms": round(total_time, 2),
        "status": "error",
        "retries": 0,
        "tokens_in": None,
        "tokens_out": None,
        "retrieval_setting": "not_applicable",
        "answer_grade": "not_applicable"
    })

    print("Failure recorded in results.csv")
