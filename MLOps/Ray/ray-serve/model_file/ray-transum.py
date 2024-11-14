from starlette.requests import Request
from typing import Dict

import ray
from ray import serve
from ray.serve.handle import DeploymentHandle

from transformers import pipeline

@serve.deployment
class Translator:
    def __init__(self):
        self.language = 'french'
        self.model = pipeline("translation_en_to_fr", model="t5-small", framework="pt")

    def translate(self, text: str) -> str:
        model_output = self.model(text)
        translation = model_output[0]["translation_text"]
        
        return translation
    
    def reconfigure(self, config: Dict):
        self.language = config.get("language", "french")
        if self.language.lower() == "french":
            self.model = pipeline("translation_en_to_fr", model="t5-small", framework="pt")
        elif self.language.lower() == "german":
            self.model = pipeline("translation_en_to_de", model="t5-small", framework="pt")
        elif self.language.lower() == "romanian":
            self.model = pipeline("translation_en_to_ro", model="t5-small", framework="pt")
        else:
            pass


@serve.deployment
class Summarizer:
    def __init__(self, translator: DeploymentHandle):
        
        self.translator = translator
        
        self.model = pipeline("summarization", model="t5-small", framework="pt")
        self.min_length = 5
        self.max_length = 15

    def summarize(self, text: str) -> str:
        
        model_output = self.model(text, min_length=self.min_length, max_length=self.max_length)

        # Post-process output to return only the summary text
        summary = model_output[0]["summary_text"]

        return summary

    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        summary = self.summarize(english_text)

        translation = await self.translator.translate.remote(summary)
        return translation

    def reconfigure(self, config: Dict):
        self.min_length = config.get('min_length', 5)
        self.max_length = config.get('max_length', 15)

app = Summarizer.bind(Translator.bind())