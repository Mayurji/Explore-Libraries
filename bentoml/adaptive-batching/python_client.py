import requests
import json

url = "http://localhost:3000/rank"

# Open your images in binary mode
files = [
    ("queries", open("dog.png", "rb")),
    ("queries", open("cat.png", "rb")),
]

# The 'candidates' list needs to be sent as a string if using form-data
data = {
    "candidates": json.dumps(["a happy dog", "a grumpy cat"])
}

response = requests.post(url, files=files, data=data)

print(json.dumps(response.json(), indent=2))