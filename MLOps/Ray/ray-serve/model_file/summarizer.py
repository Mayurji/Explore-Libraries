# File name: summary_model.py
from transformers import pipeline


class Summarizer:
    def __init__(self):
        # Load model
        self.model = pipeline("summarization", model="t5-small", device='cuda')

    def summarize(self, text: str) -> str:
        # Run inference
        model_output = self.model(text, min_length=5, max_length=15)

        # Post-process output to return only the summary text
        summary = model_output[0]["summary_text"]

        return summary


summarizer = Summarizer()

summary = summarizer.summarize(
    "It was the best of times, it was the worst of times, it was the age "
    "of wisdom, it was the age of foolishness, it was the epoch of belief"
)
print(summary)