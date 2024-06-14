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
            "temperature": 0.0,  # not recommended to set top_p and temperature at the same time
            "max_tokens": 5000,
            # "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "response_format": {"type": "json_object"},
            "n": 1,
            "seed": 1,
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
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "parse_address_output",
                        "desciption": "Extract information as seperate JSON objects for each address in the array",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "addresses": {
                                    "type": "object",
                                    "properties": {
                                        "Eng3dAddress": {
                                            "type": "object",
                                            "properties": {
                                                "EngFloor": {
                                                    "type": "object",
                                                    "properties": {
                                                        "FloorNum": {"type": "string"},
                                                        "FloorDescription": {
                                                            "type": "string"
                                                        },
                                                    },
                                                },
                                                "EngUnit": {
                                                    "type": "object",
                                                    "properties": {
                                                        "UnitDescriptor": {
                                                            "type": "string"
                                                        },
                                                        "UnitNo": {"type": "string"},
                                                        "UnitPortion": {
                                                            "type": "string"
                                                        },
                                                    },
                                                },
                                                "EngBlock": {
                                                    "type": "object",
                                                    "properties": {
                                                        "BlockDescriptor": {
                                                            "type": "string"
                                                        },
                                                        "BlockNo": {"type": "string"},
                                                    },
                                                },
                                                "BuildingName": {"type": "string"},
                                                "EngEstate": {
                                                    "type": "object",
                                                    "properties": {
                                                        "EstateName": {"type": "string"}
                                                    },
                                                },
                                                "EngPhase": {
                                                    "type": "object",
                                                    "properties": {
                                                        "PhaseName": {"type": "string"},
                                                        "PhaseNo": {"type": "string"},
                                                    },
                                                },
                                                "EngVillage": {
                                                    "type": "object",
                                                    "properties": {
                                                        "LocationName": {
                                                            "type": "string"
                                                        },
                                                        "VillageName": {
                                                            "type": "string"
                                                        },
                                                        "BuildingNoFrom": {
                                                            "type": "string"
                                                        },
                                                        "BuildingNoTo": {
                                                            "type": "string"
                                                        },
                                                    },
                                                },
                                                "EngStreet": {
                                                    "type": "object",
                                                    "properties": {
                                                        "LocationName": {
                                                            "type": "string"
                                                        },
                                                        "StreetName": {
                                                            "type": "string"
                                                        },
                                                        "BuildingNoFrom": {
                                                            "type": "string"
                                                        },
                                                        "BuildingNoTo": {
                                                            "type": "string"
                                                        },
                                                    },
                                                },
                                                "EngDistrict": {
                                                    "type": "object",
                                                    "properties": {
                                                        "DcDistrict": {
                                                            "type": "string"
                                                        },
                                                        "Region": {
                                                            "type": "string",
                                                            "enum": [
                                                                "HK",
                                                                "KLN",
                                                                "NT",
                                                            ],
                                                        },
                                                    },
                                                },
                                                "county": {"type": "string"},
                                                "city": {"type": "string"},
                                                "state": {"type": "string"},
                                                "province": {"type": "string"},
                                                "postalCode": {"type": "string"},
                                                "country": {"type": "string"},
                                                "countryCode": {"type": "string"},
                                                "poBox": {"type": "string"},
                                                "attentionLine": {"type": "string"},
                                                "careOfLine": {"type": "string"},
                                                "confidenceScore": {"type": "string"},
                                                "issues": {"type": "string"},
                                            },
                                        }
                                    },
                                    "required": ["confidenceScore", "issues"],
                                }
                            },
                        },
                    },
                }
            ],
            "tool_choice": "auto",
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
        # completions = [result["message"]["content"] for result in response["choices"]]
        completions = [
            addr["function"]["arguments"]
            for addr in response["choices"][0]["message"]["tool_calls"]
        ]
        return completions
