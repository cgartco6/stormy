import json
import requests
import subprocess
from typing import Optional
from .config import LLM_MODE, LOCAL_LLM_URL, CLOUD_LLM_API_KEY

class Brain:
    def __init__(self, personality):
        self.personality = personality
        self.mode = LLM_MODE  # 'local' or 'cloud'
        self.local_url = LOCAL_LLM_URL or "http://localhost:11434/api/generate"
        self.cloud_api_key = CLOUD_LLM_API_KEY

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        system_prompt = self.personality.get_system_prompt()
        full_prompt = f"{system_prompt}\n\nContext: {context}\nUser: {prompt}\nAssistant:"
        if self.mode == 'local':
            return self._local_generate(full_prompt)
        else:
            return self._cloud_generate(full_prompt)

    def _local_generate(self, prompt):
        payload = {
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        }
        resp = requests.post(self.local_url, json=payload)
        return resp.json()["response"]

    def _cloud_generate(self, prompt):
        # Example using Hugging Face free inference
        headers = {"Authorization": f"Bearer {self.cloud_api_key}"}
        payload = {"inputs": prompt}
        resp = requests.post("https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B", headers=headers, json=payload)
        return resp.json()[0]["generated_text"]
