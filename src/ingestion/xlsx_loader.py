import pandas as pd


def load_xlsx(file_path: str):
    df = pd.read_excel(file_path, header=None)

    documents = []

    current_question = None
    current_answer = []

    for i in range(len(df)):

        row = df.iloc[i].tolist()
        row = [str(x).strip() if pd.notna(x) else "" for x in row]

        sn = row[1] if len(row) > 1 else ""

        if sn.isdigit():

            # save previous Q/A
            if current_question and current_answer:
                documents.append({
                    "source": "faq",
                    "question": current_question,
                    "content": " ".join(current_answer).strip()
                })

            # question is in column 2
            current_question = row[2] if len(row) > 2 else None
            current_answer = []

        else:
            
            for cell in row:
                if cell and not cell.isdigit() and len(cell) > 3:
                    current_answer.append(cell)

    # flush last record
    if current_question and current_answer:
        documents.append({
            "source": "faq",
            "question": current_question,
            "content": " ".join(current_answer).strip()
        })

    return documents