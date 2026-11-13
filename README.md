\# The Relay Assignment – Research Paper Retrieval Pipeline



\## Project Overview



The Relay Assignment is a Python-based research paper retrieval and evaluation pipeline. It retrieves relevant information from three research papers and uses a hosted Large Language Model (LLM) through the Groq API to generate answers.



The project also implements a stand-in model to simulate delay, failures, streaming responses, and rate limits. This allows comparison of real model behaviour with controlled simulated behaviour.



\## Objectives



\- Load and process research papers in PDF format.

\- Split documents into smaller, overlapping text chunks.

\- Retrieve relevant passages using TF-IDF and cosine similarity.

\- Generate answers using a hosted Groq LLM.

\- Simulate model delays, failures, streaming, and rate limits.

\- Evaluate retrieval quality, answer correctness, and performance.

\- Record request-level measurements in CSV files.



\## Research Papers



The pipeline uses these three research papers:



1\. \[Attention Is All You Need](https://arxiv.org/abs/1706.03762)

2\. \[Moshi: a speech-text foundation model for real-time dialogue](https://arxiv.org/abs/2410.00037)

3\. \[Dynamic Chunking for End-to-End Hierarchical Sequence Modeling](https://arxiv.org/abs/2507.07955)



\## Project Structure



```text

The\_Relay\_Assignment/

│

├── papers/                 # Research paper PDFs

├── src/                    # Python implementation

│   ├── document\_loader.py

│   ├── chunking.py

│   ├── retriever.py

│   ├── llm\_client.py

│   ├── standin\_model.py

│   ├── results\_logger.py

│   ├── evaluate\_retrieval.py

│   ├── evaluate\_answers.py

│   └── Other testing and evaluation scripts

│

├── tests/                  # Test documentation

├── results/                # CSV evaluation results

├── reports/                # Final project report

├── .env                    # API configuration (not committed)

└── .gitignore

```



\## Technologies Used



\- Python

\- Groq API

\- Large Language Models (LLMs)

\- TF-IDF

\- Cosine Similarity

\- Scikit-learn

\- Pandas and NumPy

\- PyPDF

\- CSV-based result logging

\- Git and GitHub



\## Pipeline Architecture



The project follows these major stages:



1\. \*\*Document Loading:\*\* Extract text and page information from PDF research papers.

2\. \*\*Text Chunking:\*\* Divide extracted text into smaller chunks with overlapping content.

3\. \*\*Retrieval:\*\* Convert text into TF-IDF vectors and retrieve relevant passages using cosine similarity.

4\. \*\*LLM Generation:\*\* Send the retrieved context and user question to the Groq-hosted model.

5\. \*\*Stand-in Simulation:\*\* Simulate delays, failures, rate limits, and streaming behaviour.

6\. \*\*Evaluation:\*\* Measure retrieval quality, answer correctness, and performance.

7\. \*\*Result Logging:\*\* Store request-level measurements and evaluation results in CSV files.



\## Setup and Installation



\### 1. Clone the repository



```bash

git clone https://github.com/kaustubhpawar02/The\_Relay\_Assignment.git

cd The\_Relay\_Assignment

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows:



```cmd

.venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install groq python-dotenv pypdf scikit-learn pandas numpy matplotlib python-docx

```



\### 4. Configure the Groq API



Create a `.env` file in the project root:



```env

GROQ\_API\_KEY=your\_groq\_api\_key

GROQ\_MODEL=openai/gpt-oss-20b

```



Replace the placeholder with your own Groq API key.



\*\*Security:\*\* Never commit your `.env` file or expose your API key publicly.



\## Running the Project



Run commands from the project root directory.



Examples:



```bash

python src/test\_groq.py

```



```bash

python src/test\_standin.py

```



```bash

python src/test\_rate\_limit.py

```



Other scripts in `src/` perform retrieval experiments, answer evaluation, concurrency testing, failure testing, and result analysis.



\## Evaluation Results



The evaluation used 15 questions across the three research papers.



| Metric | Result |

|---|---:|

| Retrieval expected-paper hit rate | 14/15 (93.33%) |

| Correct answers | 13/15 (86.67%) |

| Correct answers + justified refusal | 14/15 (93.33%) |

| Best tested top-k setting | 3 |

| Selected chunk configuration | 500 characters / 100 overlap |



The selected chunk configuration achieved the same retrieval hit rate as the other tested chunk configurations while using less context.



These results are based on the project's evaluation questions and experiments, not a general benchmark.



\## Reliability Experiments



The stand-in model was used to test:



\- Simulated response delays

\- Random failures

\- Rate limiting

\- Streaming responses

\- Concurrent requests

\- Sustained request load

\- Recovery after simulated rate limits



The real Groq API was also tested. Actual Groq rate-limit recovery and several other production-level reliability measurements were not established by the experiments.



\## Limitations



\- Evaluation uses a limited set of 15 questions.

\- Retrieval and answer quality depend on the questions and source documents.

\- Real API measurements use a small sample and should not be treated as production benchmarks.

\- The stand-in model simulates selected behaviours and does not reproduce every aspect of a real hosted LLM service.

\- Some production reliability characteristics were not measured.



\## Author



\*\*Kaustubh Pawar\*\*



Computer Engineering Student



GitHub: \[kaustubhpawar02](https://github.com/kaustubhpawar02)

