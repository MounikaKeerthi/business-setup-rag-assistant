from src.ingestion.pipeline import build_documents
from src.chunking import chunk_pdf_document, chunk_faq_document

def run_pipeline():
    docs = build_documents(
         "data/pdf/FederalDecree.pdf",
        "data/xlsx/WebsiteFAQ.xlsx"
    )

    pdf_chunks = []
    faq_chunks = []

    for doc in docs:
        if doc["source"] == "pdf":
            pdf_chunks.extend(chunk_pdf_document(doc))
        else:
            faq_chunks.extend(chunk_faq_document(doc))

    print("\n===== PIPELINE OUTPUT =====")
    print("Total raw docs:", len(docs))
    print("PDF chunks:", len(pdf_chunks))
    print("FAQ chunks:", len(faq_chunks))

    print("\nSample PDF chunk:\n", pdf_chunks[0][:300] if pdf_chunks else "None")
    print("\nSample FAQ chunk:\n", faq_chunks[0] if faq_chunks else "None")


if __name__ == "__main__":
    run_pipeline()