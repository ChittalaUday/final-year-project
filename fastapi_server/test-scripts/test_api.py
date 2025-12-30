"""Test script for the Career Recommendation API."""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health_endpoint():
    """Test the health check endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_info_endpoint():
    """Test the info endpoint."""
    print("Testing /api/v1/career/info endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/career/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_prediction_endpoint():
    """Test the prediction endpoint with sample data."""
    print("Testing /api/v1/career/predict endpoint...")
    
    # Test case 1: Female student interested in cloud computing
    test_data_1 = {
        "gender": "Female",
        "interest": "Cloud computing, Technology",
        "skills": "Python, SQL, Java",
        "grades": 85.0
    }
    
    print(f"Test Case 1: {json.dumps(test_data_1, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=test_data_1)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Test case 2: Male student interested in data science
    test_data_2 = {
        "gender": "Male",
        "interest": "Data analytics;Machine Learning;Data scientist",
        "skills": "Python;R;Machine Learning skills;Artificial Intelligence",
        "grades": 78.5
    }
    
    print(f"Test Case 2: {json.dumps(test_data_2, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=test_data_2)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Test case 3: Business/Marketing profile
    test_data_3 = {
        "gender": "Female",
        "interest": "Sales/Marketing, Entrepreneurship, Digital marketing",
        "skills": "Communication skills, Marketing Strategy, Social Media Marketing",
        "grades": 72.0
    }
    
    print(f"Test Case 3: {json.dumps(test_data_3, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=test_data_3)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_invalid_input():
    """Test with invalid input to check validation."""
    print("Testing with invalid input...")
    
    invalid_data = {
        "gender": "Unknown",  # Invalid gender
        "interest": "Test",
        "skills": "Test",
        "grades": 150.0  # Invalid grade
    }
    
    print(f"Invalid Data: {json.dumps(invalid_data, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/v1/career/predict", json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Career Recommendation API - Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_health_endpoint()
        test_info_endpoint()
        test_prediction_endpoint()
        test_invalid_input()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"ERROR: {str(e)}")
