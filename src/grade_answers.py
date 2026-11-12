
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

answer_file = BASE_DIR / "results" / "answer_evaluation.csv"
results_file = BASE_DIR / "results" / "results.csv"

grades = {
    1: "wrong",
    12: "refused_correctly"
}

with open(answer_file, "r", newline="", encoding="utf-8-sig") as file:
    answers = list(csv.DictReader(file))

for number, row in enumerate(answers, start=1):
    row["answer_grade"] = grades.get(number, "correct")

with open(answer_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=answers[0].keys())
    writer.writeheader()
    writer.writerows(answers)

grade_by_id = {
    row["request_id"]: row["answer_grade"]
    for row in answers
}

with open(results_file, "r", newline="", encoding="utf-8-sig") as file:
    results = list(csv.DictReader(file))
    columns = list(results[0].keys())

updated = 0

for row in results:
    request_id = row["request_id"]

    if request_id in grade_by_id:
        row["answer_grade"] = grade_by_id[request_id]
        updated += 1

with open(results_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(results)

print("Answer grading completed.")
print("Correct:", sum(r["answer_grade"] == "correct" for r in answers))
print("Wrong:", sum(r["answer_grade"] == "wrong" for r in answers))
print("Refused correctly:", sum(r["answer_grade"] == "refused_correctly" for r in answers))
print("Updated rows in results.csv:", updated)
