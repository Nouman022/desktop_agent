import requests
from config import OLLAMA_MODEL, OLLAMA_URL


class OllamaClient:
    def __init__(self, model=OLLAMA_MODEL):
        self.model = model

    def generate(self, prompt: str):
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data["response"]