# AIRMAN: Aviation RAG Assistant ✈️

## 📌 Project Overview
AIRMAN is a specialized AI assistant designed to answer pilot queries strictly based on provided PDF manuals (e.g., Flight Planning, Meteorology). It prioritizes **grounding** and **safety** over creativity.

**Key Features:**
* **Zero Hallucination:** "Hard Rule" prompt engineering ensures the AI refuses to answer out-of-bounds questions (e.g., "Who painted the Mona Lisa?").
* **Traceable Citations:** Every answer includes the source document and page number.
* **Local Processing:** Ingestion and Vector Search (FAISS) run entirely locally.
* **Containerized:** Fully Dockerized for consistent deployment.

---

## 🚀 Quick Start (Local)

### Prerequisites
* Python 3.10+
* [Groq API Key](https://console.groq.com/) (Free)

### 1. Clone & Setup

git clone [https://github.com/rovin-benny/AIRMAN-RAG-ASSISTANT.git](https://github.com/rovin-benny/AIRMAN-RAG-ASSISTANT.git)
cd AIRMAN-RAG-ASSISTANT

# Create virtual env
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt


### 2. Configure Environment
Create a .env file from the example and add your API key:

Bash
# Linux/Mac
cp .env.example .env

# Windows (Command Prompt)
copy .env.example .env
Open the .env file in your text editor and paste your Groq API Key (it starts with gsk_).

## 3. Ingest Data
Place your aviation PDF manuals in the data/ folder..

Run the ingestion script to process the PDFs and build the vector database:

Bash
python src/ingest.py
You will see a progress bar as it chunks the text and saves the index to index/faiss_store.

## 4. Run the Application
Start the FastAPI server:

Bash
uvicorn src.main:app --reload
The server will start at http://127.0.0.1:8000.

## How to Use
Open Swagger UI: Go to http://127.0.0.1:8000/docs in your browser.

Test Health: Click GET /health -> Try it out -> Execute to confirm the system is running.

Ask a Question:

Click POST /ask.

Click Try it out.

Enter a JSON payload:

JSON
{
  "question": "What is the primary objective of ATS?",
  "debug": true
}
Click Execute.

View Response: Scroll down to see the answer and the exact citations (source file & page number).
## 5.Evaluation & Testing
To verify reliability, run the automated evaluation script (tests 50 questions):

Bash
python evaluate.py
This generates a report in tests/eval_report.json showing the Hit Rate, Faithfulness, and Hallucination Rate.



```bash
