import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")


def chunk_text(text: str, max_tokens: int = 300, overlap: int = 50):
    """
    Generic token-based chunking for long text (PDF content)
    """
    if not text:
        return []

    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = tokens[start:end]
        chunks.append(encoding.decode(chunk))

        start = end - overlap if end - overlap > start else end

    return chunks


def chunk_pdf_document(doc: dict):
    """
    Chunk unstructured PDF text
    """
    text = doc.get("content", "")
    return chunk_text(text)


def chunk_faq_document(doc: dict):
    """
    Keep Q&A together (DO NOT split)
    """
    question = doc.get("question", "")
    answer = doc.get("content", "")

    if not question and not answer:
        return []

    return [
        f"Question: {question}\nAnswer: {answer}"
    ]