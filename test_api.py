#!/usr/bin/env python3

# Test script to check API endpoints for a specific form
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.formstack_client import FormstackClient

def test_form_endpoints():
    try:
        client = FormstackClient()
        form_id = "6186472"
        
        print(f"Testing API endpoints for Form ID: {form_id}")
        print("=" * 50)
        
        # Test form details
        print("1. Testing get_form_details...")
        form_data = client.get_form_details(form_id)
        if form_data:
            print(f"✅ Form details retrieved: {form_data.get('name', 'Unknown')}")
        else:
            print("❌ No form details found")
        
        # Test webhooks
        print("\n2. Testing get_form_webhooks...")
        webhooks = client.get_form_webhooks(form_id)
        print(f"   Webhooks count: {len(webhooks)}")
        if webhooks:
            print(f"   First webhook: {webhooks[0]}")
        
        # Test integrations
        print("\n3. Testing get_form_integrations...")
        integrations = client.get_form_integrations(form_id)
        print(f"   Integrations count: {len(integrations)}")
        if integrations:
            print(f"   First integration: {integrations[0]}")
        
        # Test fields
        print("\n4. Testing get_form_fields...")
        fields = client.get_form_fields(form_id)
        print(f"   Fields count: {len(fields)}")
        if fields:
            print(f"   First field: {fields[0]}")
        
        # Test confirmations
        print("\n5. Testing get_form_confirmations...")
        confirmations = client.get_form_confirmations(form_id)
        print(f"   Confirmations count: {len(confirmations)}")
        if confirmations:
            print(f"   First confirmation: {confirmations[0]}")
        
        # Test notifications
        print("\n6. Testing get_form_notifications...")
        notifications = client.get_form_notifications(form_id)
        print(f"   Notifications count: {len(notifications)}")
        if notifications:
            print(f"   First notification: {notifications[0]}")
            
        # Test partial submissions
        print("\n7. Testing get_form_partial_submissions...")
        partial_submissions = client.get_form_partial_submissions(form_id)
        print(f"   Partial submissions count: {len(partial_submissions)}")
        if partial_submissions:
            print(f"   First partial submission: {partial_submissions[0]}")
            
    except Exception as e:
        print(f"Error during API testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_form_endpoints()
