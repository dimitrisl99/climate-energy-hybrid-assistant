from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.pdf_loader import load_all_pdfs


def chunk_documents():
    documents = load_all_pdfs()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":
    chunks = chunk_documents()

    print(f"Total chunks: {len(chunks)}")

    print("\nSample chunk:")
    print(chunks[0].page_content[:1000])

    print("\nSample metadata:")
    print(chunks[0].metadata)