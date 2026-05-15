import streamlit as st
from src.ingestion.pipeline import build_documents

# simple keyword match (temporary, before embeddings)
def find_answer(query, docs):
    query = query.lower()

    for doc in docs:
        if doc.get("source") == "faq":
            if query in doc["question"].lower():
                return doc["question"], doc["content"]

    return None, "No match found. (This will improve once we add vector DB)"


st.title("Marhaba! Welcome to Dubai Business Setup Consultancy")

# load data once
@st.cache_data
def load_data():
    return build_documents(
        "data/pdf/FederalDecree.pdf",
        "data/xlsx/WebsiteFAQ.xlsx"
    )

docs = load_data()

faq_docs = [d for d in docs if d["source"] == "faq"]
pdf_docs = [d for d in docs if d["source"] == "pdf"]

st.subheader("Dataset Stats")
st.write("FAQ chunks:", len(faq_docs))
st.write("PDF chunks:", len(pdf_docs))

st.subheader("Ask a Question")

query = st.text_input("Enter your question")

if query:
    question, answer = find_answer(query, faq_docs)

    st.markdown("### Question")
    st.write(question)

    st.markdown("### Answer")
    st.write(answer)