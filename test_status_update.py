#!/usr/bin/env python3
"""
Test script for the form status update API endpoint.
This script tests the new /api/update-form-status endpoint.
"""

import requests
import json

def test_update_form_status():
    """Test the update form status API endpoint."""
    
    # Test data - using form ID 6233111 which exists in the account
    test_form_id = "6233111"
    
    url = "http://127.0.0.1:5006/api/update-form-status"
    
    # Test data for making form inactive
    test_data = {
        "form_id": test_form_id,
        "active": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing form status update for form ID: {test_form_id}")
    print(f"Setting form to: {'Active' if test_data['active'] else 'Inactive'}")
    print(f"Making POST request to: {url}")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.content:
            try:
                response_json = response.json()
                print(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response Text: {response.text}")
        else:
            print("No response content")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the Flask server.")
        print("Make sure the Flask app is running on http://127.0.0.1:5006")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_update_form_status()
