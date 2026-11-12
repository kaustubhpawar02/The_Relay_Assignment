from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "reports" / "The_Relay_Report.docx"

doc = Document()

# Page formatting
section = doc.sections[0]
section.top_margin = Inches(0.45)
section.bottom_margin = Inches(0.45)
section.left_margin = Inches(0.55)
section.right_margin = Inches(0.55)

# Default font
styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(8)

for style_name in ["Heading 1", "Heading 2"]:
    styles[style_name].font.name = "Arial"

styles["Heading 1"].font.size = Pt(11)
styles["Heading 2"].font.size = Pt(9)

def heading(text):
    doc.add_heading(text, level=1)

def paragraph(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"

    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = str(header)

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)

    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(0)
                for run in p.runs:
                    run.font.name = "Arial"
                    run.font.size = Pt(7)

    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


# Title
title = doc.add_heading("The Relay: Research Paper Question-Answering Pipeline", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

paragraph("Assignment Report | 12 November 2026")

heading("1. What I built and why")

paragraph(
    "I built a Python research question-answering pipeline using three research "
    "papers. The pipeline loads PDF documents, extracts page-wise text, divides "
    "the text into overlapping chunks, retrieves relevant passages using TF-IDF "
    "and cosine similarity, and sends the retrieved context to a hosted language "
    "model. The model generates answers with paper titles and page citations."
)

paragraph(
    "The pipeline uses separate modules for document loading, chunking, "
    "retrieval, Groq API communication, result logging, and evaluation. "
    "I selected TF-IDF because it is lightweight and suitable for this small "
    "three-paper collection."
)

heading("2. The real service and my stand-in")

paragraph(
    "The real service is Groq, accessed through its Python SDK using the "
    "openai/gpt-oss-20b model. The API key is stored in a local .env file and "
    "excluded from Git using .gitignore."
)

paragraph(
    "I also implemented a Python stand-in model. It simulates response delays, "
    "random service failures, streaming word output, and a rolling rate limit "
    "of three requests per ten seconds. It is a simplified approximation: "
    "its delay is not dynamically increased by actual concurrent load, and "
    "its streaming is word-based rather than genuine model-token streaming."
)

heading("3. Results")

paragraph(
    "The real Groq baseline contained 31 requests. Across these requests, "
    "average time to first token (TTFT) was 1,481.78 ms and average total "
    "response time was 1,623.04 ms. Average input and output usage was "
    "560.68 and 418.42 tokens respectively."
)

add_table(
    ["Metric", "Observed result"],
    [
        ["Real requests", "31"],
        ["Average TTFT", "1,481.78 ms"],
        ["Average total time", "1,623.04 ms"],
        ["Average input tokens", "560.68"],
        ["Average output tokens", "418.42"],
        ["Answer grading", "13 correct, 1 wrong, 1 correctly refused"],
    ]
)

paragraph(
    "The stand-in produced 36 successful responses, 11 rate-limited responses, "
    "and 1 controlled error across 48 requests. In a separate 20-request "
    "random-failure test, zero failures occurred despite a configured "
    "10% failure probability."
)

add_table(
    ["Scenario", "Success", "Rate-limited", "Other error", "Mean successful time"],
    [
        ["Steady", "6", "0", "0", "1,369.16 ms"],
        ["Burst", "3", "2", "0", "1,573.28 ms"],
        ["Sustained overload", "3", "7", "0", "1,350.85 ms"],
        ["Rate-limit test", "4", "2", "0", "1,093.73 ms"],
        ["Random failure test", "20", "0", "0", "1,221.94 ms"],
        ["Controlled failure", "0", "0", "1", "Not applicable"],
    ]
)

paragraph(
    "The answer evaluation used 15 questions, five from each paper. "
    "Thirteen answers were graded correct, one incorrect, and one correctly "
    "refused because the retrieved context did not support an answer. "
    "This gives 86.67% correct answers, or 93.33% when the correct refusal "
    "is also counted as an acceptable outcome."
)

heading("4. Where the time goes")

paragraph(
    "Total response time includes the API request, model processing, and "
    "streaming the generated response. TTFT measures the time until the "
    "first generated content arrives. The measurements show that TTFT accounts "
    "for a substantial part of total response time. Network and provider-side "
    "processing also contribute; this experiment did not separately measure "
    "those components."
)

heading("5. When a limit is hit")

paragraph(
    "The Groq dashboard for the selected model displayed these limits: "
    "30 requests per minute (RPM), 1,000 requests per day (RPD), "
    "8,000 tokens per minute (TPM), and 200,000 tokens per day (TPD). "
    "The displayed concurrent-request fields were not specified."
)

paragraph(
    "The real Groq baseline did not trigger a rate-limit response, so the "
    "provider's actual error response and recovery time were not measured. "
    "The stand-in returned a simulated 429 Rate Limit Exceeded response "
    "when its rolling request limit was reached. A successful request after "
    "waiting for the window to recover was observed."
)

add_table(
    ["Required measurement", "Result"],
    [
        ["Real concurrent-request limit", "Not specified"],
        ["Real 429 response", "Not measured"],
        ["Real recovery time", "Not measured"],
        ["Daily budget exhaustion", "Not measured"],
        ["Halved per-minute limit", "Not measured"],
        ["Timeouts and retries", "Not measured"],
        ["Peak queue and cost per 1,000 answers", "Not measured"],
    ]
)

heading("Retrieval: quality versus cost")

paragraph(
    "On a 15-question retrieval evaluation, chunk sizes of 500, 1,000, and "
    "1,500 words each achieved 14/15 expected-paper hits (93.33%) with "
    "top_k=3. Their average retrieved context sizes were 224.07, 443.67, "
    "and 642.27 words respectively."
)

add_table(
    ["Setting", "Avg input tokens", "Avg output tokens", "Avg TTFT", "Avg total"],
    [
        ["500 / overlap 100", "524.67", "428.33", "1,643.42 ms", "1,856.91 ms"],
        ["1,000 / overlap 200", "825.00", "393.00", "1,470.22 ms", "1,657.10 ms"],
        ["1,500 / overlap 300", "1,215.67", "339.67", "1,394.66 ms", "1,587.66 ms"],
    ]
)

paragraph(
    "The token and latency averages above come from three real API requests "
    "per setting, using the same three questions. The 14/15 retrieval hit "
    "rate comes from a separate 15-question evaluation. These small samples "
    "do not establish that larger chunks are faster. The 500-word setting "
    "is the practical choice because it achieved the same measured retrieval "
    "hit rate with substantially less context."
)

heading("How this library will mislead a naive retriever")

paragraph(
    "TF-IDF relies on word overlap and can retrieve passages containing related "
    "terms without answering the actual question. For example, the question "
    "about the Transformer architecture retrieved passages from other papers "
    "instead of the relevant passage in Attention Is All You Need. This caused "
    "an incorrect answer. Increasing the number of retrieved passages improved "
    "paper-level hit rate from 80% at top_k=1 to 93.33% at top_k=3, but "
    "top_k=5 did not improve it further."
)

heading("Your feedback on Vaani")

paragraph(
    "The assignment helped me understand how retrieval, model calls, latency, "
    "token usage, and rate limits interact in a practical pipeline. A useful "
    "improvement would be clearer guidance on evaluating retrieval quality "
    "and distinguishing retrieval errors from language-model errors."
)

heading("How I worked with the assistant")

paragraph(
    "I used the assistant to understand the assignment, plan the pipeline, "
    "debug Python modules, understand Groq API behavior, design experiments, "
    "and interpret results. I ran the code and experiments locally, inspected "
    "the outputs, and used the measured results in this report."
)

# Save
doc.save(OUTPUT_FILE)

print("Report created successfully:")
print(OUTPUT_FILE)