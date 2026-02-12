import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Load environment variables from your .env file
load_dotenv()

# 2. Safely retrieve the API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found. Please ensure it is set in your .env file.")

# 3. Initialize the LLM with a supported 2026 model
model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

llm = ChatGroq(
    temperature=0, 
    model_name=model_name, 
    groq_api_key=groq_api_key
)

# 4. System Prompt for Hallucination Control
SYSTEM_PROMPT = """
You are an Aviation AI Assistant. Use ONLY the provided context to answer the question.
Hard Rule: If the answer is not in the context, respond EXACTLY with:
"This information is not available in the provided document(s)."

Context:
{context}

Question: {question}
"""

def get_answer(query: str, debug: bool = False):
    # Initialize the same embedding model used during ingestion
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load the FAISS index locally
    vector_db = FAISS.load_local(
        "index/faiss_store", 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # 5. Retrieval: Fetch top 3 relevant chunks
    docs = vector_db.similarity_search(query, k=3)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 6. Chain generation
    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    chain = prompt | llm
    response = chain.invoke({"context": context_text, "question": query})
    
    # 7. Format Citations from metadata
    citations = [
        {
            "source": d.metadata.get("source", "Unknown Document"), 
            "page": d.metadata.get("page", 0) + 1
        } for d in docs
    ]
    
    return {
        "answer": response.content,
        "citations": citations,
        "debug_chunks": [d.page_content for d in docs] if debug else None
    }