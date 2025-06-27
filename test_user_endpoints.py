#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_user_endpoints():
    """Test various user-related endpoints in Formstack API"""
    try:
        client = FormstackClient()
        print("Testing user-related endpoints in Formstack API...")
        print("=" * 60)
        
        # List of potential user endpoints to test
        endpoints_to_test = [
            "user",
            "team",
            "team/member", 
            "team/members",
            "account/team",
            "account/members",
            "member",
            "members",
            "participant",
            "participants",
            "collaborator",
            "collaborators",
            "share",
            "shared",
            "workspace/member",
            "workspace/members"
        ]
        
        for endpoint in endpoints_to_test:
            print(f"\n--- Testing {endpoint} ---")
            try:
                response = client._make_request("GET", endpoint)
                print(f"✅ Success! Type: {type(response)}")
                
                if isinstance(response, dict):
                    print(f"  Keys: {list(response.keys())}")
                    # Look for user-like data
                    for key in response.keys():
                        if any(term in key.lower() for term in ['user', 'member', 'participant', 'email', 'name']):
                            value = response[key]
                            if isinstance(value, list):
                                print(f"    {key}: list with {len(value)} items")
                                if value and isinstance(value[0], dict):
                                    print(f"      First item keys: {list(value[0].keys())}")
                            else:
                                print(f"    {key}: {value}")
                                
                elif isinstance(response, list):
                    print(f"  List length: {len(response)}")
                    if response and isinstance(response[0], dict):
                        print(f"  First item keys: {list(response[0].keys())}")
                        # Check if it looks like user data
                        first_item = response[0]
                        user_indicators = ['email', 'name', 'user', 'member', 'participant']
                        if any(indicator in str(first_item.keys()).lower() for indicator in user_indicators):
                            print(f"  ⭐ Looks like user data: {first_item}")
                            
            except Exception as e:
                print(f"❌ Failed: {str(e)[:100]}...")
        
        # Also check if there are other portal-related endpoints
        print(f"\n{'='*60}")
        print("Testing additional portal endpoints...")
        
        portal_endpoints = [
            "portal/participant",
            "portal/participants", 
            "portal/member",
            "portal/members",
            "portal/all",
            "portals"
        ]
        
        for endpoint in portal_endpoints:
            print(f"\n--- Testing {endpoint} ---")
            try:
                response = client._make_request("GET", endpoint)
                print(f"✅ Success! Type: {type(response)}")
                if isinstance(response, (list, dict)):
                    print(f"  Content preview: {str(response)[:200]}...")
            except Exception as e:
                print(f"❌ Failed: {str(e)[:100]}...")
        
    except Exception as e:
        print(f"Error during user endpoints test: {e}")

if __name__ == "__main__":
    test_user_endpoints()
