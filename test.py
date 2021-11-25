import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(f"{BASE}video/1", {"likes": 10, "name": "Name", "views": 10})
print(response.json())


response = requests.get(f"{BASE}video/2")
print(response.json())