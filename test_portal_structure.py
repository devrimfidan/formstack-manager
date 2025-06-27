#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_portal_structure():
    """Test the actual structure of Portal API responses"""
    try:
        client = FormstackClient()
        print("Testing actual Portal API response structure...")
        print("=" * 60)
        
        # Test portal list endpoint
        print("--- Testing portal list endpoint ---")
        portals_response = client._make_request("GET", "portal")
        print(f"Portal response type: {type(portals_response)}")
        print(f"Portal response: {portals_response}")
        
        if isinstance(portals_response, list):
            print(f"Portal list length: {len(portals_response)}")
            if portals_response:
                portal = portals_response[0]
                portal_id = portal['id']
                print(f"First portal: {portal}")
                
                # Test detailed portal endpoint
                print(f"\n--- Testing detailed portal {portal_id} endpoint ---")
                detailed_response = client._make_request("GET", f"portal/{portal_id}")
                print(f"Detailed response type: {type(detailed_response)}")
                print(f"Portal users count: {len(detailed_response.get('portalUsers', []))}")
                print(f"Portal users: {detailed_response.get('portalUsers', [])}")
                
                # Check for pagination indicators
                pagination_keys = ['total', 'pages', 'current_page', 'per_page', 'count', 'next_page', 'prev_page', 'has_more', 'limit', 'offset']
                found_pagination = {}
                for key in pagination_keys:
                    if key in detailed_response:
                        found_pagination[key] = detailed_response[key]
                
                if found_pagination:
                    print(f"Pagination info found: {found_pagination}")
                else:
                    print("No pagination info found in response")
                    
        elif isinstance(portals_response, dict):
            print(f"Portal response keys: {list(portals_response.keys())}")
            if 'portals' in portals_response:
                portals = portals_response['portals']
                print(f"Portals list length: {len(portals)}")
                if portals:
                    portal_id = portals[0]['id']
                    print(f"First portal ID: {portal_id}")
        
        # Test if we can get user count from account info
        print(f"\n--- Testing account info ---")
        try:
            account_response = client._make_request("GET", "account")
            print(f"Account response keys: {list(account_response.keys())}")
            # Look for user-related info
            for key in account_response:
                if 'user' in key.lower() or 'participant' in key.lower() or 'member' in key.lower():
                    print(f"  {key}: {account_response[key]}")
        except Exception as e:
            print(f"Account endpoint failed: {e}")
        
    except Exception as e:
        print(f"Error during portal structure test: {e}")

if __name__ == "__main__":
    test_portal_structure()
