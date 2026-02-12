import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def process_pdfs(data_path="data_small/", index_path="index/faiss_store"):
    # 1. Load PDFs
    documents = []
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyMuPDFLoader(os.path.join(data_path, file))
            documents.extend(loader.load())

    # 2. Chunking Strategy

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=60,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = text_splitter.split_documents(documents)

    # 3. Embeddings (Free & Local)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Store in FAISS
    print(f"Generating embeddings for {len(chunks)} chunks... this will take a while.", flush=True)
    vector_db = FAISS.from_documents(chunks, embeddings)
    print("Embeddings generated successfully!", flush=True)
    vector_db.save_local(index_path)
    return f"Ingested {len(chunks)} chunks from {data_path}"