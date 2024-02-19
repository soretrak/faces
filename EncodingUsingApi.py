import requests

api_url = "http://localhost:8080/presence"

response = requests.get(api_url)
result = response.json()
print(result)

# inserting data  using api
data = {"matric": 1001}
response = requests.post(api_url, json=data)
