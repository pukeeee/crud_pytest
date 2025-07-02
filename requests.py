import requests

url = "http://localhost:8000/users"
data = {
    "user_name": "Test",
    "email": "test@mail.com",
    "password": "Password123/"
}
response = requests.post(url, json = data)
print(response.status_code)
print(response.text)