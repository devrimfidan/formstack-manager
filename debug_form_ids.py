#!/usr/bin/env python3
"""
Test script to check forms by ID range and see if there are forms beyond what the list API returns.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_form_ids():
    """Test accessing forms by ID to see if there are forms not returned by the list API."""
    
    api_key = os.getenv("FORMSTACK_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    base_url = "https://www.formstack.com/api/v2"
    
    # We know the list API returns forms up to 6233112, let's test some IDs beyond that
    test_ids = [
        6233111,  # We know this exists
        6233112,  # This is the highest ID from the list
        6233113, 6233114, 6233115, 6233120, 6233130, 6233150,  # Test some higher IDs
        6240000, 6250000, 6300000, 6500000,  # Test much higher IDs
        7000000, 7500000, 8000000  # Test very high IDs to see if they exist
    ]
    
    existing_forms = []
    
    print("Testing individual form IDs to see if there are forms beyond the list API...")
    
    for form_id in test_ids:
        try:
            url = f"{base_url}/form/{form_id}.json"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                form_data = response.json()
                existing_forms.append({
                    'id': form_id,
                    'name': form_data.get('name', 'Unknown'),
                    'created': form_data.get('created', 'Unknown'),
                    'inactive': form_data.get('inactive', False)
                })
                print(f"✅ Form {form_id}: EXISTS - {form_data.get('name', 'Unknown')} (created: {form_data.get('created', 'Unknown')}, inactive: {form_data.get('inactive', False)})")
            elif response.status_code == 404:
                print(f"❌ Form {form_id}: NOT FOUND")
            else:
                print(f"⚠️  Form {form_id}: ERROR {response.status_code}")
                
        except Exception as e:
            print(f"⚠️  Form {form_id}: ERROR - {e}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Found {len(existing_forms)} existing forms by direct ID access")
    
    if existing_forms:
        print(f"ID range: {min(f['id'] for f in existing_forms)} to {max(f['id'] for f in existing_forms)}")
        inactive_count = sum(1 for f in existing_forms if f['inactive'])
        print(f"Inactive forms found: {inactive_count}")
        
        print(f"\nExisting forms:")
        for form in existing_forms:
            print(f"  ID {form['id']}: {form['name']} (inactive: {form['inactive']})")

if __name__ == "__main__":
    test_form_ids()
