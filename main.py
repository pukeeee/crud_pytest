import requests

url = "http://localhost:8000/users"
data = {
    "user_name": "Alice",
    "email": "alice@mail.com",
    "password": "Password123/"
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.text)