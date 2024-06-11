import json
from typing import Any

import requests
from dspy import LM


class CustomLMClient(LM):
    def __init__(self, model: str, **kwargs):
        """
        Custom LM client initializer extending LM interface using openrouter
        parameters are set to default values
        """
        with open("secrets.json", encoding="utf-8") as f:
            secrets = json.load(f)
            api_key = secrets["OPENROUTER_API_KEY"]
        self.model: str = (model,)
        self.model_type: str = ("text",)
        self.api_key: str = api_key
        self.provider: str = "default"
        self.history: list[dict[str, Any]] = []
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.kwargs: dict[str, Any] = {
            "temperature": 0.0,
            "max_tokens": 5000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "n": 1,
            **kwargs,
        }

    def basic_request(self, prompt: str, **kwargs):
        raw_kwargs = kwargs

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "content-type": "application.json",
        }

        data = {
            **kwargs,
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(self.base_url, headers=headers, json=data, timeout=10)
        response = response.json()

        history = {
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs,
            "raw_kwargs": raw_kwargs,
        }
        self.history.append(history)
        return response

    def __call__(self, prompt: str, only_completed=True, return_sorted=False, **kwargs):
        response = self.request(prompt, **kwargs)
        completions = [result["message"]["content"] for result in response["choices"]]
        return completions
