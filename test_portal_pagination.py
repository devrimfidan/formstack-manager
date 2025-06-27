#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_portal_pagination():
    """Test Portal API with pagination parameters to ensure we get all users"""
    try:
        client = FormstackClient()
        print("Testing Portal API with pagination parameters...")
        print("=" * 60)
        
        # Test different pagination parameters
        pagination_params = [
            {},  # No params
            {"page": 1},
            {"page": 1, "per_page": 100},
            {"page": 1, "limit": 100},
            {"offset": 0, "limit": 100},
            {"per_page": 100},
            {"limit": 100}
        ]
        
        for i, params in enumerate(pagination_params):
            print(f"\n--- Test {i+1}: params = {params} ---")
            try:
                # Test portal list endpoint
                print("Testing portal list with params:")
                portals_response = client._make_request("GET", "portal", params=params)
                print(f"Portals found: {len(portals_response.get('portals', portals_response))}")
                
                # If we have portals, test the detailed portal endpoint
                if 'portals' in portals_response and portals_response['portals']:
                    portal_id = portals_response['portals'][0]['id']
                    print(f"Testing detailed portal {portal_id} with params:")
                    detailed_response = client._make_request("GET", f"portal/{portal_id}", params=params)
                    users_count = len(detailed_response.get('portalUsers', []))
                    print(f"Users found in portal: {users_count}")
                    
                    # Show pagination info if present
                    for key in ['total', 'pages', 'current_page', 'per_page', 'count', 'next_page', 'prev_page']:
                        if key in detailed_response:
                            print(f"  {key}: {detailed_response[key]}")
                
            except Exception as e:
                print(f"❌ Failed with params {params}: {e}")
        
        # Test if there's a general users endpoint
        print(f"\n--- Testing general user endpoints ---")
        user_endpoints = [
            "user",
            "users", 
            "account/user",
            "account/users"
        ]
        
        for endpoint in user_endpoints:
            try:
                print(f"Testing {endpoint}:")
                response = client._make_request("GET", endpoint)
                print(f"✅ Success! Type: {type(response)}")
                if isinstance(response, dict):
                    print(f"  Keys: {list(response.keys())}")
                elif isinstance(response, list):
                    print(f"  Count: {len(response)}")
            except Exception as e:
                print(f"❌ Failed: {e}")
        
    except Exception as e:
        print(f"Error during portal pagination test: {e}")

if __name__ == "__main__":
    test_portal_pagination()
