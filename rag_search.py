import numpy as np

from rag_embeddings import create_embedding


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)

    vector_b = np.array(vector_b)

    similarity = np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    return similarity


# ============================================================
# SEARCH RELEVANT CHUNK
# ============================================================

def search_documents(
    question,
    embedded_chunks,
    top_k=1
):

    # --------------------------------------------------------
    # Create embedding for user question
    # --------------------------------------------------------

    question_embedding = create_embedding(
        question
    )

    # --------------------------------------------------------
    # Compare question with every document chunk
    # --------------------------------------------------------

    results = []

    for chunk in embedded_chunks:

        similarity = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        results.append(
            {
                "filename": chunk["filename"],
                "text": chunk["text"],
                "similarity": similarity
            }
        )

    # --------------------------------------------------------
    # Sort by similarity
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    # --------------------------------------------------------
    # Return best chunks
    # --------------------------------------------------------

    return results[:top_k]