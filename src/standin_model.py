
import time
import random


class StandInModel:

    def __init__(self):
        self.failure_probability = 0.1
        self.minimum_delay = 0.5
        self.maximum_delay = 2.0

        self.max_requests = 3
        self.time_window = 10
        self.request_times = []

    def check_rate_limit(self):

        current_time = time.time()

        self.request_times = [
            request_time
            for request_time in self.request_times
            if current_time - request_time < self.time_window
        ]

        if len(self.request_times) >= self.max_requests:
            raise Exception("429 Rate Limit Exceeded")

        self.request_times.append(current_time)

    def generate(self, question):

        self.check_rate_limit()

        delay = random.uniform(
            self.minimum_delay,
            self.maximum_delay
        )

        time.sleep(delay)

        if random.random() < self.failure_probability:
            raise Exception("Simulated model service failure")

        answer = (
            "This is a simulated response from the stand-in model. "
            f"The received question was: {question}"
        )

        return {
            "answer": answer,
            "total_time_ms": round(delay * 1000, 2),
            "status": "ok"
        }

    def generate_stream(self, question):

        self.check_rate_limit()

        answer = (
            "This is a simulated response from the stand-in model. "
            f"The received question was: {question}"
        )

        initial_delay = random.uniform(
            self.minimum_delay,
            self.maximum_delay
        )

        time.sleep(initial_delay)

        if random.random() < self.failure_probability:
            raise Exception("Simulated model service failure")

        words = answer.split()

        for word in words:
            yield word + " "
            time.sleep(0.05)
