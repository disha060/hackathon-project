import requests

# Test AI assignment generation
try:
    response = requests.get(
        "http://localhost:8000/teacher/ai/assignments?concept_id=1"
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")