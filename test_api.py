"""
Test script for the Security Testing API.

This script tests the API endpoints by making requests to the running server.
"""
import os
import json
import zipfile
import tempfile
import requests
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_security_testing_endpoint():
    """Test the security testing endpoint with a sample ZIP file."""
    print("\n=== Testing Security Testing Endpoint ===")
    
    # Create a temporary ZIP file with sample content
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
        temp_zip_path = temp_file.name
    
    try:
        # Create a ZIP file with sample files
        with zipfile.ZipFile(temp_zip_path, 'w') as zip_file:
            # Add a Python file
            zip_file.writestr('main.py', 'print("Hello, World!")\n# TODO: Remove hardcoded password\npassword = "secret123"')
            
            # Add a JSON file
            zip_file.writestr('config.json', '{"api_key": "1234567890", "debug": true}')
            
            # Add a JavaScript file
            zip_file.writestr('app.js', 'console.log("Hello, World!");')
        
        # Make request to security testing endpoint
        with open(temp_zip_path, 'rb') as zip_file:
            files = {'file': ('test.zip', zip_file, 'application/zip')}
            response = requests.post(f"{BASE_URL}/api/v1/security-testing", files=files)
        
        # Print response status and data
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
            print("✅ Security testing endpoint test passed!")
        else:
            print(f"❌ Error: {response.text}")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_zip_path):
            os.unlink(temp_zip_path)


def main():
    """Run all tests."""
    print(f"Testing Security API at {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test root endpoint to check if server is running
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print(f"✅ Server is running! Response: {response.json()}")
        else:
            print(f"❌ Server returned unexpected status: {response.status_code}")
            return
        
        # Run tests
        test_security_testing_endpoint()
        
        print("\n✅ All tests completed!")
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server. Make sure the API is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
