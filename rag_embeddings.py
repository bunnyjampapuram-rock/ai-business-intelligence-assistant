import requests


OLLAMA_URL = "http://localhost:11434/api/embeddings"

EMBEDDING_MODEL = "nomic-embed-text"


def create_embedding(text):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "prompt": text
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]


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