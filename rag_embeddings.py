import os
import requests


# ============================================================
# OLLAMA CLOUD CONFIGURATION
# ============================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_EMBED_URL",
    "https://ollama.com/api/embed"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

OLLAMA_API_KEY = os.getenv(
    "OLLAMA_API_KEY"
)


# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    if not OLLAMA_API_KEY:
        raise ValueError(
            "OLLAMA_API_KEY is not configured."
        )

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": text
        },
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}"
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    # Ollama Cloud /api/embed returns embeddings
    # inside the "embeddings" field.

    embeddings = data.get("embeddings")

    if not embeddings:
        raise ValueError(
            f"No embeddings returned by Ollama: {data}"
        )

    return embeddings[0]


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