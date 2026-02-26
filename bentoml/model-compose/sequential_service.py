import bentoml
from bentoml.models import HuggingFaceModel
from transformers import pipeline
from typing import Dict, Any

"""
Sequential: You can let models work in a sequence, where the output of one model 
becomes the input for another. This is useful for creating pipelines where data 
needs to be preprocessed before being used for predictions.
"""

@bentoml.service(resources={"cpu": "2", "memory": "2Gi"})
class PreprocessingService:
    model_a_path = HuggingFaceModel("distilbert/distilbert-base-uncased")

    def __init__(self) -> None:
        # Initialize pipeline for model A
        self.pipeline_a = pipeline(task="text-classification", model=self.model_a_path)

    @bentoml.api
    def preprocess(self, input_data: str) -> Dict[str, Any]:
        # Dummy preprocessing steps
        return self.pipeline_a(input_data)[0]


@bentoml.service(resources={"gpu": 1, "memory": "4Gi"})
class InferenceService:
    model_b_path = HuggingFaceModel("distilbert/distilroberta-base")
    preprocessing_service = bentoml.depends(PreprocessingService)

    def __init__(self) -> None:
        # Initialize pipeline for model B
        self.pipeline_b = pipeline(task="text-classification", model=self.model_b_path)

    @bentoml.api
    async def predict(self, input_data: str) -> Dict[str, Any]:
        # Dummy inference on preprocessed data
        # Implement your custom logic here
        preprocessed_data = await self.preprocessing_service.to_async.preprocess(input_data)
        final_result = self.pipeline_b(input_data)[0]
        return {
            "preprocessing_result": preprocessed_data,
            "final_result": final_result
        }
    