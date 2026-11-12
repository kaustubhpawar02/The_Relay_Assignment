
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE = BASE_DIR / "results" / "results.csv"

df = pd.read_csv(FILE)

print("\n========== REQUEST SUMMARY ==========")
print("Total requests:", len(df))

print("\nBy source:")
print(df["source"].value_counts())

print("\nBy scenario and status:")
print(pd.crosstab(df["scenario"], df["status"]))

print("\n========== GROQ LATENCY ==========")

real = df[df["source"] == "real"]

print("Real requests:", len(real))
print("Average TTFT:", round(real["first_token_ms"].mean(), 2), "ms")
print("Average total time:", round(real["total_ms"].mean(), 2), "ms")
print("Average input tokens:", round(real["tokens_in"].mean(), 2))
print("Average output tokens:", round(real["tokens_out"].mean(), 2))

print("\n========== STAND-IN RESULTS ==========")

standin = df[df["source"] == "stand-in"]

print("Stand-in requests:", len(standin))
print("\nStand-in outcomes:")
print(standin["status"].value_counts())

print("\n========== ANSWER GRADES ==========")

graded = real[real["answer_grade"].notna() & (real["answer_grade"] != "")]

print("Graded requests:", len(graded))
print(graded["answer_grade"].value_counts())

print("\n========== SCENARIO LATENCY ==========")

successful = df[df["status"] == "ok"]

print(
    successful.groupby(["source", "scenario"])["total_ms"]
    .agg(["count", "mean", "min", "max"])
    .round(2)
)

print("\nAnalysis completed.")
