from fastapi.testclient import TestClient
from app.app import app

# Initialize the TestClient
client = TestClient(app)

response = client.put("/smrt-link/projects/1")  # Simulate a GET request to the endpoint
print(response.json())
