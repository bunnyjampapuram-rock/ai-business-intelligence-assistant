def chunk_documents(documents, chunk_size=500):

    chunks = []

    for document in documents:

        text = document["text"]
        filename = document["filename"]

        start = 0

        while start < len(text):

            chunk = text[
                start:start + chunk_size
            ]

            chunks.append(
                {
                    "filename": filename,
                    "text": chunk
                }
            )

            start += chunk_size

    return chunks