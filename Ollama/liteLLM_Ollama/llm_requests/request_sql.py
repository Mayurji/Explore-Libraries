import requests

url = "http://0.0.0.0:4000/chat/completions"
headers = {
    "Authorization": "Bearer sk-1234",
    "Content-Type": "application/json"
}

payload = {
    "model": "semantic-hub",
    "messages": [
        {
            "role": "user", 
            "content": "Create a SQL query to find the top 5 customers by total spend."
        }
    ],
    "temperature": 0.2
}

response = requests.post(url, headers=headers, json=payload)
print("Routing to SQL/Code Model:")
print(response.json()['choices'][0]['message']['content'])