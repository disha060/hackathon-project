import requests
import json

# Test student signup
signup_data = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass",
    "role": "student"
}

try:
    response = requests.post(
        "http://localhost:8000/student/signup",
        headers={"Content-Type": "application/json"},
        data=json.dumps(signup_data)
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")