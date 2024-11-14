import requests
import numpy as np

data = {"inputs" : [[14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0]]}
url = 'http://localhost:8080/invocations'

response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})  # Use 'json=data' for JSON payload
