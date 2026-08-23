import os


# ============================================================
# RAG DOCUMENT FOLDER
# ============================================================

DOCUMENT_FOLDER = "rag_documents"


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():

    documents = []

    
    # Check folder
    

    if not os.path.exists(DOCUMENT_FOLDER):

        raise FileNotFoundError(
            f"Document folder not found: {DOCUMENT_FOLDER}"
        )

    # --------------------------------------------------------
    # Read files
    # --------------------------------------------------------

    for filename in os.listdir(DOCUMENT_FOLDER):

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

       
        # Only read text files for now
       

        if filename.lower().endswith(".txt"):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            documents.append(
                {
                    "filename": filename,
                    "text": text
                }
            )

    return documents