import asyncio
import bentoml
from bentoml.models import HuggingFaceModel
from transformers import pipeline
from typing import Dict, Any, List

"""
Concurrent
You can run multiple independent models at the same time and then combine their results. 
This is useful for ensemble models where you want to aggregate predictions from different models to improve accuracy.
"""

@bentoml.service(resources={"gpu": 1, "memory": "4Gi"})
class ModelAService:
    model_a_path = HuggingFaceModel("FacebookAI/roberta-large-mnli")

    def __init__(self) -> None:
        # Initialize pipeline for model A
        self.pipeline_a = pipeline(task="zero-shot-classification", model=self.model_a_path, hypothesis_template="This text is about {}")

    @bentoml.api
    def predict(self, input_data: str, labels: List[str] = ["positive", "negative", "neutral"]) -> Dict[str, Any]:
        # Dummy preprocessing steps
        return self.pipeline_a(input_data, labels)

@bentoml.service(resources={"gpu": 1, "memory": "4Gi"})
class ModelBService:
    model_b_path = HuggingFaceModel("distilbert/distilbert-base-uncased")

    def __init__(self) -> None:
        # Initialize pipeline for model B
        self.pipeline_b = pipeline(task="sentiment-analysis", model=self.model_b_path)

    @bentoml.api
    def predict(self, input_data: str) -> Dict[str, Any]:
        # Dummy preprocessing steps
        return self.pipeline_b(input_data)[0]

@bentoml.service(resources={"cpu": "4", "memory": "8Gi"})
class EnsembleService:
    service_a = bentoml.depends(ModelAService)
    service_b = bentoml.depends(ModelBService)

    @bentoml.api
    async def ensemble_predict(self, input_data: str, labels: List[str] = ["positive", "negative", "neutral"]) -> Dict[str, Any]:
        result_a, result_b = await asyncio.gather(
            self.service_a.to_async.predict(input_data, labels),
            self.service_b.to_async.predict(input_data)
        )
        # Dummy aggregation
        return {
            "zero_shot_classification": result_a,
            "sentiment_analysis": result_b
        }