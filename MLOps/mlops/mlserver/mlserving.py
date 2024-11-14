import os
import requests

url = "http://0.0.0.0:9001/v2/models/randomforestreg/infer"

# Example data (replace with the actual model's input)
payload = {
    "inputs": [
        {
            "name": "input",
            "shape": [1, 4],   # Update the input shape as per your model
            "datatype": "FP64",  # Update the datatype based on your model
            "data": [[5.1, 3.5, 1.4, 0.2]]   # Example input data
        }
    ]
}

# Set headers
headers = {"Content-Type": "application/json"}

# Send the POST request to the MLServer
response = requests.post(url, json=payload, headers=headers)

# Print the response
print(response.json())
