from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


PDF_DIR = Path("data/raw/pdfs")


def load_all_pdfs():
    documents = []

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files")

    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        pdf_docs = loader.load()

        documents.extend(pdf_docs)

    return documents


if __name__ == "__main__":
    docs = load_all_pdfs()

    print(f"\nLoaded {len(docs)} pages")

    print("\nSample document:")
    print(docs[0].page_content[:1000])