# rag_query.py

import os
import faiss
import joblib
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Constants
INDEX_PATH = Path("rag/app/faiss_index/index.faiss")
KNN_DATA_PATH = Path("rag/app/faiss_index/index.pkl")
TOP_K = 5

# # Load FAISS index and metadata
# index = faiss.read_index(str(INDEX_PATH))
# metadata = joblib.load(KNN_DATA_PATH)

# # Load the same embedding model
# embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load FAISS using LangChain’s loader
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
db = FAISS.load_local("rag/app/faiss_index", embeddings=embedding_model)

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# --- RAG Pipeline ---
def ask_rag_question(query: str):
    # # 1. Embed query
    # query_vec = embedding_model.encode([query]).astype(np.float32)

    # # 2. Search FAISS index
    # distances, indices = index.search(query_vec, TOP_K)

    # # 3. Retrieve top-k documents
    # docs = [metadata[i] for i in indices[0] if i != -1 and i < len(metadata)]
    # if not docs:
    #     raise ValueError("No relevant documents found for the query.")
    # context = "\n\n".join(docs)

    # using langchain's FAISS vector store for simplicity
    docs = db.similarity_search(query, k=TOP_K)
    # Convert docs to text
    context = "\n\n".join([doc.page_content for doc in docs])

    # 4. Ask LLM
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant for product information retrieval.",
        },
        {
            "role": "user",
            "content": f"Answer the question based on the following documents:\n\n{context}\n\nQuestion: {query}",
        },
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

    return response.choices[0].message.content


# --- Entry point ---
if __name__ == "__main__":
    while True:
        user_input = input("🔍 Ask a question about our products (or type 'exit'): ")
        if user_input.strip().lower() == "exit":
            break

        try:
            answer = ask_rag_question(user_input)
            print(f"\n🧠 Answer:\n{answer}\n")
        except Exception as e:
            print(f"❌ Error: {e}")
