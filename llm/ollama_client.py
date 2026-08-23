import os
import requests


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
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


    response = requests.post(
        OLLAMA_URL,
        json=payload
    )


    response.raise_for_status()


    result = response.json()


    answer = result["message"]["content"]


    return answer