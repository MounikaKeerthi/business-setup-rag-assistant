from src.ingestion.pdf_loader import load_pdf
from src.ingestion.xlsx_loader import load_xlsx

def build_documents(pdf_path: str, xlsx_path: str):
    documents = []

    # PDF
    pdf_text = load_pdf(pdf_path)
    documents.append({
        "source": "pdf",
        "content": pdf_text
    })

    # XLSX (IMPORTANT CHANGE)
    faq_docs = load_xlsx(xlsx_path)

    for doc in faq_docs:
        documents.append({
            "source": doc["source"],
            "question": doc["question"],
            "content": doc["content"]
        })

    return documents


if __name__ == "__main__":
    docs = build_documents(
        "data/pdf/FederalDecree.pdf",
        "data/xlsx/WebsiteFAQ.xlsx"
    )

    print("Total docs:", len(docs))
    print("Sample:", docs[0])