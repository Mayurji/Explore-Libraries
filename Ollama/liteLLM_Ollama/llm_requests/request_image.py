import requests
import base64
import os

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

url = "http://0.0.0.0:4000/chat/completions"
headers = {
    "Authorization": "Bearer sk-1234", 
    "Content-Type": "application/json"
}

image_path = "image.png"
base64_image = encode_image(image_path)
# Detect extension for the data URI
ext = os.path.splitext(image_path)[1].lower().replace('.', '') or "png"

payload = {
    "model": "semantic-hub",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is described in this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{ext};base64,{base64_image}"}
                }
            ]
        }
    ]
}

print(f"Sending request to {url} (routing via semantic-hub)...")
response = requests.post(url, headers=headers, json=payload)
res_data = response.json()

if "error" in res_data:
    print("Error from Proxy:", res_data["error"]["message"])
else:
    print("Routing to Image Model Successful!")
    print("Response:", res_data['choices'][0]['message']['content'])
