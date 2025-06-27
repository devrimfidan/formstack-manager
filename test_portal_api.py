#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_portal_api():
    """Test the Portal API endpoints to debug the data structure"""
    try:
        client = FormstackClient()
        print("Testing Portal API endpoints...")
        print("=" * 50)
        
        # Test portal info endpoint
        print("\n1. Testing portal info endpoint:")
        print("-" * 30)
        portal_info = client.get_portal_info()
        print(f"Portal info type: {type(portal_info)}")
        print(f"Portal info keys: {list(portal_info.keys()) if isinstance(portal_info, dict) else 'Not a dict'}")
        print(f"Portal info content: {portal_info}")
        
        # Test portal users extraction
        print("\n2. Testing portal users extraction:")
        print("-" * 30)
        users = client.get_portal_users()
        print(f"Users type: {type(users)}")
        print(f"Users count: {len(users) if isinstance(users, list) else 'Not a list'}")
        if users:
            print(f"First user: {users[0]}")
        else:
            print("No users found")
        
        # Test raw API call
        print("\n3. Testing raw API call:")
        print("-" * 30)
        try:
            raw_response = client._make_request("GET", "portal")
            print(f"Raw response type: {type(raw_response)}")
            print(f"Raw response keys: {list(raw_response.keys()) if isinstance(raw_response, dict) else 'Not a dict'}")
            print(f"Raw response: {raw_response}")
        except Exception as e:
            print(f"Raw API call error: {e}")
            print(f"Error type: {type(e)}")
            
    except Exception as e:
        print(f"Test failed with error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_portal_api()
