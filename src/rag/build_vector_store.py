from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.rag.chunk_documents import chunk_documents


CHROMA_DIR = Path("data/db/chroma")
COLLECTION_NAME = "climate_energy_docs"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store():
    print("Loading and chunking documents...")
    chunks = chunk_documents()

    print(f"Total chunks to index: {len(chunks)}")

    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Building Chroma vector store...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"Vector store created successfully at: {CHROMA_DIR}")

    return vector_store


if __name__ == "__main__":
    build_vector_store()