import os
import requests


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "https://ollama.com/api/chat"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama3.2"
)


def ask_llm(messages):

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    result = response.json()

    answer = result["message"]["content"]

    return answer