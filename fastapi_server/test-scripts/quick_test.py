"""Quick API test script."""
import requests
import json

BASE_URL = "http://localhost:8000"

print("="*60)
print("FastAPI Server - API Tests")
print("="*60)

# Test 1: Root endpoint
print("\n1. Testing root endpoint (GET /)...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Health check
print("\n2. Testing health endpoint (GET /health)...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Career info
print("\n3. Testing career info (GET /api/v1/career/info)...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/career/info")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 4: Career prediction - Tech profile
print("\n4. Testing career prediction - Tech profile...")
tech_data = {
    "gender": "Female",
    "interest": "Cloud computing, Technology, Data analytics",
    "skills": "Python, SQL, Java, Machine learning skills",
    "grades": 85.0
}
try:
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=tech_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 5: Career prediction - Business profile
print("\n5. Testing career prediction - Business profile...")
business_data = {
    "gender": "Male",
    "interest": "Sales/Marketing, Entrepreneurship, Digital marketing",
    "skills": "Communication skills, Marketing Strategy, Leadership",
    "grades": 78.0
}
try:
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=business_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 6: Invalid input validation
print("\n6. Testing input validation (invalid gender)...")
invalid_data = {
    "gender": "Unknown",
    "interest": "Test",
    "skills": "Test",
    "grades": 150.0  # Also invalid
}
try:
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=invalid_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*60)
print("All tests completed!")
print("="*60)
