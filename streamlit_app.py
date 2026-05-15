import streamlit as st
from src.ingestion.pipeline import build_documents

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Dubai Business AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Dubai Business Setup AI Assistant")
st.caption("RAG-powered chatbot for Dubai business consultancy")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return build_documents(
        "data/pdf/FederalDecree.pdf",
        "data/xlsx/WebsiteFAQ.xlsx"
    )

docs = load_data()

faq_docs = [d for d in docs if d["source"] == "faq"]
pdf_docs = [d for d in docs if d["source"] == "pdf"]

# -----------------------------
# SIMPLE RETRIEVAL LOGIC
# -----------------------------
def find_answer(query):
    query = query.lower()

    for doc in faq_docs:
        if query in doc["question"].lower():
            return doc["question"], doc["content"]

    return None, "I couldn't find an exact match yet. (Vector DB coming next 🚀)"

# -----------------------------
# WELCOME MESSAGE
# -----------------------------
welcome_message = """
Marhaba! Welcome to Dubai Business Setup Consultancy 🇦🇪

I'm your AI assistant here to help you with:

• Company setup (Free Zone / Mainland / Offshore)
• Licensing requirements
• Visa options
• Costs & timelines
• General business setup guidance

Ask me anything to get started 👇
"""

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_message}
    ]

# -----------------------------
# CLEAN WHATSAPP-STYLE RENDERER
# -----------------------------
def render_message(role, message):

    if role == "user":
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:flex-end;
                margin:8px 0;
            ">
                <div style="
                    background-color:#DCF8C6;
                    color:#000;
                    padding:10px 14px;
                    border-radius:15px 15px 0px 15px;
                    max-width:75%;
                    font-size:15px;
                    line-height:1.4;
                ">
                    {message}
                </div>
                <div style="margin-left:8px; font-size:22px;">👤</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:flex-start;
                margin:8px 0;
            ">
                <div style="margin-right:8px; font-size:22px;">🤖</div>
                <div style="
                    background-color:#F1F0F0;
                    color:#000;
                    padding:10px 14px;
                    border-radius:15px 15px 15px 0px;
                    max-width:75%;
                    font-size:15px;
                    line-height:1.4;
                ">
                    {message}
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Ask about business setup in Dubai...")

if user_input:

    # store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    render_message("user", user_input)

    # get response
    _, answer = find_answer(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    render_message("assistant", answer)