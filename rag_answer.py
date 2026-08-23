from llm.ollama_client import ask_llm


# ============================================================
# GENERATE ANSWER FROM RETRIEVED DOCUMENTS
# ============================================================

def generate_rag_answer(
    question,
    retrieved_documents
):

    # --------------------------------------------------------
    # Create context from retrieved documents
    # --------------------------------------------------------

    context_parts = []

    for document in retrieved_documents:

        context_parts.append(
            f"Source: {document['filename']}\n"
            f"{document['text']}"
        )

    context = "\n\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI Business Intelligence assistant.

Answer the user's question using ONLY the
information provided in the company documents.

If the answer is not present in the documents,
say that the information is not available in
the provided documents.

Do not make up information.

Company documents:

{context}

User question:

{question}

Give a clear and concise answer.
"""

    # --------------------------------------------------------
    # Ask Ollama
    # --------------------------------------------------------

    response = ask_llm(
        [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.strip()