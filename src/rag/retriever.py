from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache


CHROMA_DIR = Path("data/db/chroma")
COLLECTION_NAME = "climate_energy_docs"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
    )

    return vector_store

def retrieve_documents(query: str, k: int = 5):
    vector_store = load_vector_store()

    results = vector_store.similarity_search(query, k=k)

    return results


if __name__ == "__main__":
    test_query = "What are the EU climate neutrality targets?"

    docs = retrieve_documents(test_query, k=5)

    for i, doc in enumerate(docs, start=1):
        print(f"\n--- RESULT {i} ---")
        print(doc.page_content[:800])
        print("\nMetadata:")
        print(doc.metadata)