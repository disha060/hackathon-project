import requests

# Test adaptive assignments
try:
    response = requests.get(
        "http://localhost:8000/student/assignments?student_id=1"
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")