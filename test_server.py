#!/usr/bin/env python3
"""
Test script for the tee time booking web server

This script tests the Flask web server endpoints locally before deploying to the cloud.
"""

import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, expected_status=200, method='GET'):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🧪 Testing {method} {endpoint}")

    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, timeout=10)

        print(f"   Status: {response.status_code}")

        if response.status_code == expected_status:
            print(f"   ✅ Success!")
        else:
            print(f"   ❌ Expected {expected_status}, got {response.status_code}")

        # Try to parse JSON response
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        except:
            print(f"   Response: {response.text[:200]}...")

        return response.status_code == expected_status

    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Web Server Tests")
    print("=" * 50)

    print("\n📋 Make sure to start the web server first:")
    print("   python web_server.py")
    print("\n⏳ Waiting 3 seconds for you to start the server...")
    time.sleep(3)

    tests = [
        ("/", 200, 'GET'),
        ("/health", 200, 'GET'),
        ("/status", 200, 'GET'),
        ("/run?test=true", 200, 'GET'),  # Test mode
    ]

    passed = 0
    total = len(tests)

    for endpoint, expected_status, method in tests:
        if test_endpoint(endpoint, expected_status, method):
            passed += 1

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your web server is ready for deployment.")
        print("\n🔗 Next steps:")
        print("   1. Deploy to Replit or your preferred cloud platform")
        print("   2. Set up cron job at cron-job.org")
        print("   3. Test the live deployment")
    else:
        print("⚠️  Some tests failed. Check the web server setup.")

    print(f"\n🌐 When deployed, your cron job URL will be:")
    print(f"   https://your-repl-name.username.repl.co/run")

if __name__ == "__main__":
    main()
