#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_portal_users_api():
    """Test different Portal API endpoints to find the correct way to get users"""
    try:
        client = FormstackClient()
        print("Testing Portal User API endpoints...")
        print("=" * 50)
        
        # First get the portals
        portals = client._make_request("GET", "portal")
        print(f"Found {len(portals)} portal(s)")
        
        if portals:
            portal = portals[0]
            portal_id = portal['id']
            print(f"Testing with portal ID: {portal_id}")
            print(f"Portal name: {portal['name']}")
            print(f"Participant count: {portal['participantCount']}")
            
            # Try different endpoints for getting portal users
            endpoints_to_try = [
                f"portal/{portal_id}",
                f"portal/{portal_id}/user",
                f"portal/{portal_id}/users", 
                "portal/user",
                "portal/users",
                f"portal/{portal_id}/participant",
                f"portal/{portal_id}/participants"
            ]
            
            for endpoint in endpoints_to_try:
                print(f"\n--- Testing endpoint: {endpoint} ---")
                try:
                    response = client._make_request("GET", endpoint)
                    print(f"✅ Success! Response type: {type(response)}")
                    if isinstance(response, dict):
                        print(f"Keys: {list(response.keys())}")
                    elif isinstance(response, list):
                        print(f"List length: {len(response)}")
                        if response:
                            print(f"First item keys: {list(response[0].keys()) if isinstance(response[0], dict) else 'Not a dict'}")
                    print(f"Response: {response}")
                except Exception as e:
                    print(f"❌ Failed: {e}")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_portal_users_api()
