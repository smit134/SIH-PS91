import ollama
from typing import List

class LLMService:
    def __init__(self, model_name: str = "gemma:2b", embedding_model: str = "nomic-embed-text"):
        self.model_name = model_name
        self.embedding_model = embedding_model

    def generate_completion(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(model=self.model_name, messages=messages)
        return response['message']['content']

    def generate_embedding(self, text: str) -> List[float]:
        response = ollama.embeddings(model=self.embedding_model, prompt=text)
        return response['embedding']

llm_service = LLMService()
