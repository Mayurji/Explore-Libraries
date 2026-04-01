"""
Testing LiteLLM with Ollama using Curl requests


curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tier-1-fast",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
  }'
"""

import requests

url = "http://localhost:4000/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "tier-1-fast",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
}
response = requests.post(url, headers=headers, json=data)
print("Basic Routing", response.json())
