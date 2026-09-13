import os
from typing import List, Optional

class LLMService:
    def __init__(self, model_name: str = "gemini-2.5-flash", embedding_model: str = "text-embedding-004"):
        self.model_name = model_name
        self.embedding_model = embedding_model
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from google import genai
                from app.config import settings
                api_key = os.environ.get("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", None)
                if api_key:
                    self._client = genai.Client(api_key=api_key)
            except Exception as e:
                print(f"[LLMService] Gemini Client init warning: {e}")
        return self._client

    def generate_completion(self, prompt: str, system_prompt: str = None) -> str:
        client = self._get_client()
        if not client:
            return "Gemini API key is not configured or client failed to initialize."

        try:
            from google.genai import types
            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                temperature=0.3,
            )
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as e:
            # Fallback to older generation call if version differs
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
                )
                return response.text
            except Exception as inner_e:
                return f"Error generating Gemini completion: {inner_e}"

    def generate_embedding(self, text: str) -> List[float]:
        client = self._get_client()
        if not client:
            return [0.0] * 768

        try:
            truncated = text[:8000]
            result = client.models.embed_content(
                model=self.embedding_model,
                contents=truncated,
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"[LLMService] Gemini embedding warning: {e}")
            return [0.0] * 768

llm_service = LLMService()
