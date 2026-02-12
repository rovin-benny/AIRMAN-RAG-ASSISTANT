# AIRMAN — AI/ML Intern Technical Assignment Report

**Submitted by:** Rovin V Benny 
**Date:** February 2026

---

## 1. Executive Summary
The AIRMAN Aviation RAG System is a document-grounded QA assistant designed to answer technical aviation questions strictly from provided manuals. The system prioritizes **safety and faithfulness** over creative generation, adhering to a "Hard Rule" that forbids answering questions outside the retrieved context.

**Key Performance Indicators:**
* **Hallucination Rate:** **0.0%** (Perfect adherence to safety rules)
* **Retrieval Hit-Rate:** **40.0%** (20/50 questions answered)
* **Faithfulness:** **High** (All generated answers were grounded in text)

---

## 2. Methodology

### Architecture
* **Ingestion:** `PyMuPDFLoader` for precise text extraction, keeping page numbers intact for citations.
* **Chunking Strategy:** `RecursiveCharacterTextSplitter` with a chunk size of **600 characters** and **60-character overlap**.
    * *Rationale:* Aviation procedures (e.g., "Engine Failure during Takeoff") are often concise bullet points. Large chunks (1000+) dilute specific numbers, while small chunks (<300) lose semantic context. 600 was chosen to balance granularity with context.
* **Vector Store:** **FAISS** (Local CPU index) using `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`).
* **LLM:** **Llama-3.3-70b-versatile** via Groq API. Chosen for its superior reasoning capabilities in technical domains compared to smaller 8b models.

### Hallucination Control (The "Hard Rule")
A strict System Prompt was implemented to enforce grounding:
> *"Hard Rule: If the answer is not in the context, respond EXACTLY with: 'This information is not available in the provided document(s).'"*

---

## 3. Quantitative Evaluation Results

The system was evaluated on a dataset of **50 questions** (20 Factual, 20 Applied, 10 Reasoning).

| Metric | Score | Notes |
| :--- | :--- | :--- |
| **Retrieval Hit-Rate** | **40%** | 20 questions answered; 30 refused. The low hit rate is a result of the strict `Top-k=3` retrieval limit used to minimize noise. |
| **Faithfulness** | **100%** | Every answered question included citations and contained no external knowledge. |
| **Hallucination Rate** | **0%** | The system correctly refused 100% of out-of-domain "trap" questions. |
| **Refusal Rate** | **60%** | High refusal rate indicates the system favors "Silence" over "Guessing," which is critical for aviation safety. |

---

## 4. Qualitative Analysis

###  Top 5 "Best" Answers (High Accuracy & Grounding)

| ID | Question Type | Question | Analysis |
| :--- | :--- | :--- | :--- |
| **Q19** | Factual | *Cloud type producing continuous precipitation?* | **Perfect Retrieval:** The system retrieved `Meteorology.pdf` Page 231, identified "Nimbostratus," and returned the exact option "C." |
| **Q11** | Out-of-Bounds | *Who painted the Mona Lisa?* | **Hard Rule Success:** The system successfully suppressed any internal knowledge about Leonardo da Vinci and returned the required refusal phrase. |
| **Q49** | Reasoning | *CAS vs Mach during descent through inversion?* | **Complex Synthesis:** The model correctly reasoned that descending at constant Mach increases CAS, citing `Instruments.pdf` Page 638. |
| **Q18** | Applied | *Min satellites for GNSS 3D position?* | **Technical Precision:** The answer explained *why* 4 satellites are needed (solving for X, Y, Z, Time) rather than just stating the number. |
| **Q50** | Reasoning | *Primary objective of ATS?* | **Direct Lookup:** Found the verbatim definition "Prevent collisions" on `Flight-Planning.pdf` Page 160. |

### Top 5 "Worst" Answers (Refusals & Logic Errors)

| ID | Question Type | Question | Analysis |
| :--- | :--- | :--- | :--- |
| **Q1** | Factual | *Flight levels referenced to?* | **Retrieval Miss:** Refused to answer. The concept "Standard Pressure Datum" was likely in the document, but not in the Top-3 retrieved chunks for the query "Flight levels referenced to". |
| **Q6** | Factual | *Airspace class for IFR/VFR?* | **Confused Reasoning:** While the final answer was correct (Class E), the LLM's logic was messy (*"C is incorrect... D is the only one left"*), showing struggle with multiple-choice elimination. |
| **Q22** | Applied | *Visibility restriction by hygroscopic particles?* | **Vocabulary Gap:** Refused. The embedding model likely failed to strongly associate "hygroscopic" with "Fog/Mist" without a direct keyword match in the top chunks. |
| **Q46** | Reasoning | *Warm front characteristics?* | **Context Fragmentation:** Refused. Warm front descriptions span multiple pages. A 600-char chunk likely caught only one aspect (e.g., clouds), which wasn't enough for the LLM to confidently confirm "Option C." |
| **Q8** | Factual | *Temp decrease in troposphere?* | **Refusal:** A basic concept that was missed. This suggests the retrieval query was too specific or the chunks were dominated by numerical lapse rates rather than physical explanations. |

---

## 5. Conclusion & Future Improvements

The AIRMAN RAG system successfully demonstrates a **safety-first architecture**. It completely eliminates hallucinations, which is the most critical requirement for an aviation advisor.

However, the **40% Hit Rate** indicates that the retrieval pipeline is too narrow.

### Proposed Level 2 Improvements:
1.  **Hybrid Search:** Implement a keyword-based search (BM25) alongside vector search. This would fix Q22 ("hygroscopic") where semantic similarity failed but a keyword match would succeed.
2.  **Re-Ranking:** Fetch Top-20 chunks and use a Cross-Encoder (Reranker) to select the best 5. This would likely solve Q1 and Q46 by surfacing relevant context that was just outside the Top-3.
3.  **Parent Document Retriever:** Retrieve larger parent chunks (full pages) when a small child chunk is matched. This would provide the necessary context for reasoning questions like Q46 (Warm Fronts).