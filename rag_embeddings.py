import os

from google import genai


# ============================================================
# GEMINI EMBEDDING CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = "gemini-embedding-001"


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    if not response.embeddings:
        raise ValueError(
            "No embedding returned by Gemini."
        )

    return response.embeddings[0].values


# ============================================================
# EMBED DOCUMENTS
# ============================================================

def embed_documents(chunks):

    embedded_chunks = []

    for chunk in chunks:

        embedding = create_embedding(
            chunk["text"]
        )

        embedded_chunks.append(
            {
                "filename": chunk["filename"],
                "text": chunk["text"],
                "embedding": embedding
            }
        )

    return embedded_chunks