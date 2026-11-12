
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is missing")

if not MODEL:
    raise ValueError("GROQ_MODEL is missing")

client = Groq(api_key=API_KEY)


def generate_answer(question, passages):

    context = ""

    for passage in passages:
        context += (
            f"\nPaper: {passage['title']}"
            f"\nPage: {passage['page']}"
            f"\nText: {passage['text']}\n"
        )

    prompt = f"""
You are a research paper question-answering assistant.

Answer using ONLY the provided research passages.

Rules:
1. Do not use outside knowledge.
2. If the answer is unavailable, say so.
3. Cite the paper title and page number.
4. Never invent citations.

Research passages:
{context}

Question:
{question}

Answer:
"""

    start_time = time.perf_counter()

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=700,
        stream=True
    )

    answer = ""
    first_token_time = None

    for chunk in stream:

        content = chunk.choices[0].delta.content

        if content:
            if first_token_time is None:
                first_token_time = time.perf_counter()

            answer += content

    end_time = time.perf_counter()

    total_time = (end_time - start_time) * 1000

    ttft = None
    if first_token_time is not None:
        ttft = (first_token_time - start_time) * 1000

    generation_time = (
        total_time - ttft if ttft is not None else None
    )

    return {
        "answer": answer,
        "ttft_ms": round(ttft, 2) if ttft is not None else None,
        "total_time_ms": round(total_time, 2),
        "generation_time_ms": round(generation_time, 2) if generation_time is not None else None,
        "tokens_in": chunk.x_groq.usage.prompt_tokens if chunk.x_groq and chunk.x_groq.usage else None,
        "tokens_out": chunk.x_groq.usage.completion_tokens if chunk.x_groq and chunk.x_groq.usage else None
    }
