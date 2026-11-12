
import time
from standin_model import StandInModel

model = StandInModel()

question = "What is the Transformer architecture?"

start_time = time.perf_counter()

first_token_time = None
answer = ""

try:
    for word in model.generate_stream(question):

        if first_token_time is None:
            first_token_time = time.perf_counter()

        answer += word

    end_time = time.perf_counter()

    ttft = (first_token_time - start_time) * 1000
    total_time = (end_time - start_time) * 1000
    generation_time = total_time - ttft

    print("\nSTAND-IN ANSWER:")
    print(answer)

    print("\nPERFORMANCE METRICS:")
    print("TTFT (ms):", round(ttft, 2))
    print("Total time (ms):", round(total_time, 2))
    print("Generation time (ms):", round(generation_time, 2))

    print("Status: ok")

except Exception as error:
    print("\nERROR:", error)
