#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_smartlists_api():
    """Test SmartLists API endpoints to understand the issue"""
    try:
        client = FormstackClient()
        print("Testing SmartLists API endpoints...")
        print("=" * 50)
        
        # Test different SmartList endpoints
        endpoints_to_try = [
            "smartlist",
            "smartlists", 
            "smartlist.json",
            "smartlists.json"
        ]
        
        for endpoint in endpoints_to_try:
            print(f"\n--- Testing endpoint: {endpoint} ---")
            try:
                response = client._make_request("GET", endpoint)
                print(f"✅ Success! Response type: {type(response)}")
                print(f"Response: {response}")
                
                if isinstance(response, dict):
                    print(f"Keys: {list(response.keys())}")
                    if 'smartlists' in response:
                        smartlists = response['smartlists']
                        print(f"SmartLists count: {len(smartlists)}")
                        if smartlists:
                            print(f"First SmartList: {smartlists[0]}")
                elif isinstance(response, list):
                    print(f"Direct list length: {len(response)}")
                    if response:
                        print(f"First item: {response[0]}")
                        
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        # Test if SmartLists are available in account
        print(f"\n--- Testing account capabilities ---")
        try:
            # Check if we can get any account info that mentions smartlists
            endpoints_to_check = ["account", "account.json", "user/account"]
            for endpoint in endpoints_to_check:
                try:
                    response = client._make_request("GET", endpoint)
                    print(f"✅ {endpoint} success: {type(response)}")
                    if isinstance(response, dict):
                        # Look for smartlist-related keys
                        for key in response.keys():
                            if 'smart' in key.lower() or 'list' in key.lower():
                                print(f"  Found key: {key} = {response[key]}")
                except Exception as e:
                    print(f"❌ {endpoint} failed: {e}")
        except Exception as e:
            print(f"Account check failed: {e}")
            
    except Exception as e:
        print(f"Error during SmartLists API test: {e}")

if __name__ == "__main__":
    test_smartlists_api()
