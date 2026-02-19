import bentoml
from PIL.Image import Image
import numpy as np
from typing import Dict
from typing import List
from pydantic import Field

MODEL_ID = "openai/clip-vit-base-patch32"

runtime_image = bentoml.images.PythonImage(
    python_version="3.11"
).requirements_file("requirements.txt")


def _resize_img(img: Image):
    return img.resize((224, 224))


@bentoml.service(
    image=runtime_image,
    resources={
        "memory" : "4Gi"
    }
)
class CLIP:

    hf_model = bentoml.models.HuggingFaceModel(MODEL_ID)
    
    def __init__(self) -> None:
        import torch
        from transformers import CLIPModel, CLIPProcessor
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(self.hf_model).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(self.hf_model)
        self.logit_scale = self.model.logit_scale.item() if self.model.logit_scale.item() else 4.60517
        print("Model clip loaded", "device:", self.device)

    @bentoml.api(batchable=True)
    async def encode_image(self, items: List[Image]) -> np.ndarray:
        '''
        generate the 512-d embeddings of the images
        '''
        return await self._encode_image(items)

    async def _encode_image(self, items: List[Image]) -> np.ndarray:
        items = [_resize_img(item) for item in items]
        inputs = self.processor(images=items, return_tensors="pt", padding=True).to(self.device)
        image_embeddings = self.model.get_image_features(**inputs)
        return image_embeddings.cpu().detach().numpy()
    

    @bentoml.api(batchable=True)
    async def encode_text(self, items: List[str]) -> np.ndarray:
        '''
        generate the 512-d embeddings of the texts
        '''
        return await self._encode_text(items)

    async def _encode_text(self, items: List[str]) -> np.ndarray:
        inputs = self.processor(text=items, return_tensors="pt", padding=True).to(self.device)
        text_embeddings = self.model.get_text_features(**inputs)
        return text_embeddings.cpu().detach().numpy()
    
    @bentoml.api
    async def rank(self, queries: List[Image], candidates : List[str] = Field(["picture of a dog", "picture of a cat"], description="list of description candidates")) -> Dict[str, List[List[float]]]:
        '''
        return the similarity between the query images and the candidate texts
        '''

        # Encode embeddings
        query_embeds = await self._encode_image(queries)
        candidate_embeds = await self._encode_text(candidates)

        # Compute cosine similarities
        cosine_similarities = self.cosine_similarity(query_embeds, candidate_embeds)
        logit_scale = np.exp(self.logit_scale)
        # Compute softmax scores
        prob_scores = self.softmax(logit_scale * cosine_similarities)
        return {
            "probabilities": prob_scores.tolist(),
            "cosine_similarities" : cosine_similarities.tolist(),
        }
        
    @staticmethod
    def cosine_similarity(query_embeds, candidates_embeds):
        # Normalize each embedding to a unit vector
        query_embeds /= np.linalg.norm(query_embeds, axis=1, keepdims=True)
        candidates_embeds /= np.linalg.norm(candidates_embeds, axis=1, keepdims=True)

        # Compute cosine similarity
        cosine_similarities = np.matmul(query_embeds, candidates_embeds.T)

        return cosine_similarities
    
    @staticmethod
    def softmax(scores):
        # Compute softmax scores (probabilities)
        exp_scores = np.exp(
            scores - np.max(scores, axis=-1, keepdims=True)
        )  # Subtract max for numerical stability
        return exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)