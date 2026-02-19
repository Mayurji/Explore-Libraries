import bentoml
from bentoml.models import HuggingFaceModel
from transformers import pipeline
from typing import List

# Run two models in the same Service on the same hardware device
@bentoml.service(
    resources={"gpu": 1, "memory": "4GiB"},
    traffic={"timeout": 20},
)
class MultiModelService:
    # Retrieve model references from HF by specifying its HF ID
    model_a_path = HuggingFaceModel("FacebookAI/roberta-large-mnli")
    model_b_path = HuggingFaceModel("distilbert/distilbert-base-uncased")

    def __init__(self) -> None:
        # Initialize pipelines for each model
        self.pipeline_a = pipeline(task="zero-shot-classification", model=self.model_a_path, hypothesis_template="This text is about {}")
        self.pipeline_b = pipeline(task="sentiment-analysis", model=self.model_b_path)

    # Define an API for data processing with model A
    @bentoml.api
    def process_a(self, input_data: str, labels: List[str] = ["positive", "negative", "neutral"]) -> dict:
        return self.pipeline_a(input_data, labels)

    # Define an API for data processing with model B
    @bentoml.api
    def process_b(self, input_data: str) -> dict:
        return self.pipeline_b(input_data)[0]

    # Define an API endpoint that combines the processing of both models
    @bentoml.api
    def combined_process(self, input_data: str, labels: List[str] = ["positive", "negative", "neutral"]) -> dict:
        classification = self.pipeline_a(input_data, labels)
        sentiment = self.pipeline_b(input_data)[0]
        return {
            "classification": classification,
            "sentiment": sentiment
        }