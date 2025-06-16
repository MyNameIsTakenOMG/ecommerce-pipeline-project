# rag/app/prepare_embeddings.py

import os
from pathlib import Path
import joblib
import faiss
import numpy as np
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Load the markdown file
doc_path = Path("product_knowledge.md")
loader = TextLoader(str(doc_path))
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# Generate embeddings (you can change the model name)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print(f"🔍 First chunk preview:\n{chunks[0].page_content}\n")
print(f"✅ Total chunks generated: {len(chunks)}")


# Create FAISS index
db = FAISS.from_documents(chunks, embedding_model)

# Save FAISS index
db.save_local("rag/app/faiss_index")

# # manually save the index and metadata as string
# texts = [doc.page_content for doc in chunks]
# joblib.dump(texts, "rag/app/faiss_index/index.pkl")


print(f"✅ Generated {len(chunks)} chunks and saved FAISS index to rag/app/faiss_index")
