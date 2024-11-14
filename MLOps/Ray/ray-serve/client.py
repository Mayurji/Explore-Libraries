# File name: model_client.py
import requests

#english_text = "Hello world!"
summary_text = "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief"

response = requests.post("http://127.0.0.1:8000/summarize_translate", json=summary_text)
french_text = response.text

print(french_text)