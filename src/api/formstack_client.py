# src/api/formstack_client.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file.
# This ensures that the API_KEY is available when
# FormstackClient is instantiated.
load_dotenv()

class FormstackClient:
    """
    A client for interacting with the Formstack API.
    Handles authentication and making HTTP requests.
    """
    # Base URL for Formstack API v2
    BASE_URL = "https://www.formstack.com/api/v2"
    
    # Retrieve the API key from environment variables
    API_KEY = os.getenv("FORMSTACK_API_KEY")

    def __init__(self):
        """
        Initializes the FormstackClient.
        Raises ValueError if FORMSTACK_API_KEY is not set.
        """
        if not self.API_KEY:
            raise ValueError(
                "FORMSTACK_API_KEY not found in environment variables. "
                "Please set it in your .env file in the project root."
            )
        # Headers required for authentication and content type
        self.headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method, endpoint, params=None):
        """
        Internal method to make an HTTP request to the Formstack API.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            endpoint (str): The API endpoint (e.g., "form", "form/123/submission").
            params (dict, optional): Dictionary of parameters for the request.
                                     For GET, these are query parameters.
                                     For POST/PUT, these are JSON body. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: For any HTTP or connection errors.
            ValueError: If the response is not valid JSON.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        print(f"Making {method} request to: {url}") # Log the request URL

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=params)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=params)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Raise an HTTPError for bad responses (4xx or 5xx status codes)
            response.raise_for_status()
            
            # Check if response content exists before trying to parse JSON
            if response.content:
                return response.json()
            else:
                # Some successful API calls (e.g., DELETE) might return no content
                return {} 

        except requests.exceptions.HTTPError as e:
            # Detailed error message for HTTP errors
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: Could not connect to Formstack API: {e}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: Request to Formstack API timed out: {e}")
            raise
        except requests.exceptions.RequestException as e:
            # Catch all other requests-related exceptions
            print(f"An unexpected request error occurred: {e}")
            raise
        except ValueError as e:
            print(f"JSON decoding error: {e}. Response content: {response.text}")
            raise

    def get_all_forms(self):
        """
        Fetches all forms from the Formstack account, including creation and
        last submission times directly from the form object.

        Returns:
            list: A list of dictionaries, where each dictionary represents a form.
                  Returns an empty list if no forms are found or an error occurs.
        """
        print("Fetching all forms...")
        try:
            # The Formstack API's GET /form endpoint returns a dictionary
            # with a 'forms' key containing the list of forms.
            # We are also adding 'folders=false' to the URL to explicitly get forms without nesting.
            response_data = self._make_request("GET", "form.json", params={"folders": "false"})
            
            if isinstance(response_data, dict) and 'forms' in response_data and isinstance(response_data['forms'], list):
                return response_data['forms']
            else:
                # Handle unexpected response structure
                print(f"Unexpected response format for GET /form: {response_data}")
                return []
        except Exception as e:
            print(f"Error fetching all forms: {e}")
            return []

    def get_folder_details(self, folder_id):
        """
        Fetches detailed information for a specific folder.

        Args:
            folder_id (str or int): The ID of the folder to fetch.

        Returns:
            dict: The folder details or None if error occurs.
        """
        print(f"Fetching folder details for ID: {folder_id}")
        try:
            response_data = self._make_request("GET", f"folder/{folder_id}.json")
            return response_data
        except Exception as e:
            print(f"Error fetching folder {folder_id}: {e}")
            return None

    def get_all_folders(self):
        """
        Fetches all folders from the Formstack account (only top-level folders).
        This is the basic folder list endpoint.

        Returns:
            list: A list of dictionaries, where each dictionary represents a folder.
                  Returns an empty list if no folders are found or an error occurs.
        """
        print("Fetching all folders...")
        try:
            # The Formstack API's GET /folder endpoint returns a dictionary
            # with a 'folders' key containing the list of folders.
            response_data = self._make_request("GET", "folder.json")
            
            if isinstance(response_data, dict) and 'folders' in response_data and isinstance(response_data['folders'], list):
                return response_data['folders']
            else:
                # Handle unexpected response structure
                print(f"Unexpected response format for GET /folder: {response_data}")
                return []
        except Exception as e:
            print(f"Error fetching all folders: {e}")
            return []

    def get_form_details(self, form_id):
        """
        Fetches detailed information for a specific form.

        Args:
            form_id (str or int): The ID of the form to fetch.

        Returns:
            dict: The form details or None if error occurs.
        """
        print(f"Fetching form details for ID: {form_id}")
        try:
            response_data = self._make_request("GET", f"form/{form_id}.json")
            return response_data
        except Exception as e:
            print(f"Error fetching form {form_id}: {e}")
            return None

    def get_complete_folder_hierarchy(self):
        """
        Fetches the complete folder hierarchy by first getting all top-level folders,
        then recursively discovering subfolders and fetching detailed information.

        Returns:
            list: A list of dictionaries with complete folder hierarchy information.
                  Returns an empty list if no folders are found or an error occurs.
        """
        print("Fetching complete folder hierarchy...")
        try:
            # First, get the basic folder list (top-level folders)
            basic_folders = self.get_all_folders()
            if not basic_folders:
                print("No basic folders found")
                return []

            # Extract all folder IDs from basic folders
            discovered_folder_ids = set(folder.get('id') for folder in basic_folders if folder.get('id'))
            print(f"Found {len(discovered_folder_ids)} top-level folder IDs: {list(discovered_folder_ids)}")

            # Also check all forms to find folder IDs that might reference subfolders
            print("Checking forms for additional folder references...")
            forms_data = self.get_all_forms()
            form_folder_ids = set()
            for form in forms_data:
                folder_id = form.get('folder')
                if folder_id and folder_id != '0':  # Exclude '0' which means no folder
                    form_folder_ids.add(folder_id)
            
            # Find folder IDs that are referenced by forms but not in our basic folder list
            additional_folder_ids = form_folder_ids - discovered_folder_ids
            print(f"Found {len(additional_folder_ids)} additional folder IDs from forms: {list(additional_folder_ids)}")
            
            # Add these to our discovery list
            discovered_folder_ids.update(additional_folder_ids)

            # Fetch detailed information for each discovered folder
            detailed_folders = []
            for folder_id in discovered_folder_ids:
                folder_details = self.get_folder_details(folder_id)
                if folder_details:
                    detailed_folders.append(folder_details)

            print(f"Successfully fetched details for {len(detailed_folders)} folders")
            return detailed_folders

        except Exception as e:
            print(f"Error fetching complete folder hierarchy: {e}")
            return []

    def get_form_partial_submissions(self, form_id):
        """
        Fetches partial submissions for a specific form.

        Args:
            form_id (str or int): The ID of the form to get partial submissions for.

        Returns:
            list: A list of partial submission data, or an empty list if none found.
        """
        try:
            response_data = self._make_request("GET", f"form/{form_id}/partialsubmission.json")
            return response_data.get('partialsubmissions', []) if response_data else []
        except Exception as e:
            print(f"Error fetching partial submissions for form {form_id}: {e}")
            return []

    def get_form_confirmations(self, form_id):
        """
        Fetches confirmation settings for a specific form.

        Args:
            form_id (str or int): The ID of the form to get confirmations for.

        Returns:
            list: A list of confirmation data, or an empty list if none found.
        """
        try:
            response_data = self._make_request("GET", f"form/{form_id}/confirmation.json")
            return response_data.get('confirmations', []) if response_data else []
        except Exception as e:
            print(f"Error fetching confirmations for form {form_id}: {e}")
            return []

    def get_form_notifications(self, form_id):
        """
        Fetches notification settings for a specific form.

        Args:
            form_id (str or int): The ID of the form to get notifications for.

        Returns:
            list: A list of notification data, or an empty list if none found.
        """
        try:
            response_data = self._make_request("GET", f"form/{form_id}/notification.json")
            return response_data.get('notifications', []) if response_data else []
        except Exception as e:
            print(f"Error fetching notifications for form {form_id}: {e}")
            return []

    def get_form_webhooks(self, form_id):
        """
        Fetches webhook settings for a specific form.

        Args:
            form_id (str or int): The ID of the form to get webhooks for.

        Returns:
            list: A list of webhook data, or an empty list if none found.
        """
        try:
            response_data = self._make_request("GET", f"form/{form_id}/webhook.json")
            return response_data.get('webhooks', []) if response_data else []
        except Exception as e:
            print(f"Error fetching webhooks for form {form_id}: {e}")
            return []

    def get_form_integrations(self, form_id):
        """
        Fetches integration settings for a specific form.
        Note: The integration endpoint may not be available in all Formstack API versions.
        This method attempts different approaches to detect integrations.

        Args:
            form_id (str or int): The ID of the form to get integrations for.

        Returns:
            list: A list of integration data, or an empty list if none found.
        """
        try:
            # Try the integrations endpoint first
            response_data = self._make_request("GET", f"form/{form_id}/integration.json")
            return response_data.get('integrations', []) if response_data else []
        except Exception as e:
            # If integration endpoint fails, try to detect integrations from form fields
            print(f"Integration endpoint not available for form {form_id}, trying alternative detection: {e}")
            try:
                # Get form fields and look for integration-related fields
                fields = self.get_form_fields(form_id)
                integrations = []
                
                # Look for common integration field types or names
                integration_indicators = [
                    'salesforce', 'hubspot', 'mailchimp', 'zapier', 'webhook',
                    'crm', 'email_marketing', 'payment', 'stripe', 'paypal'
                ]
                
                for field in fields:
                    field_name = str(field.get('name', '')).lower()
                    field_type = str(field.get('type', '')).lower()
                    
                    for indicator in integration_indicators:
                        if indicator in field_name or indicator in field_type:
                            integrations.append({
                                'type': indicator,
                                'field_id': field.get('id'),
                                'field_name': field.get('name'),
                                'detected_from': 'field_analysis'
                            })
                            break
                
                return integrations
            except Exception as inner_e:
                print(f"Alternative integration detection failed for form {form_id}: {inner_e}")
                return []

    def get_form_fields(self, form_id):
        """
        Fetches field details for a specific form.
        This can help identify integration-related fields.

        Args:
            form_id (str or int): The ID of the form to get fields for.

        Returns:
            list: A list of field data, or an empty list if none found.
        """
        try:
            response_data = self._make_request("GET", f"form/{form_id}/field.json")
            # Handle both dict and list responses
            if isinstance(response_data, list):
                return response_data
            elif isinstance(response_data, dict):
                return response_data.get('fields', response_data.get('data', []))
            else:
                return []
        except Exception as e:
            print(f"Error fetching fields for form {form_id}: {e}")
            return []

    def get_all_smartlists(self):
        """
        Fetches all SmartLists from the Formstack API.
        
        Returns:
            list: A list of SmartList dictionaries containing SmartList information.
        """
        try:
            response = self._make_request("GET", "smartlist")
            # The API returns results in a 'results' array, not 'smartlists'
            smartlists = response.get("results", [])
            
            print(f"Found {len(smartlists)} SmartLists in API response")
            
            # Process each smartlist to ensure consistent data structure
            processed_smartlists = []
            for smartlist in smartlists:
                processed_smartlist = {
                    'id': smartlist.get('id'),
                    'name': smartlist.get('name', 'Unnamed SmartList'),
                    'description': smartlist.get('description', ''),
                    'created': smartlist.get('created'),
                    'updated': smartlist.get('updated'),
                    'items_count': smartlist.get('items_count', 0),
                    'is_active': smartlist.get('is_active', True),
                    'folder': smartlist.get('folder'),
                    'sharing': smartlist.get('sharing', {}),
                    'fields': smartlist.get('fields', []),
                    'useImages': smartlist.get('useImages', False),
                    'useSeparateValues': smartlist.get('useSeparateValues', False)
                }
                processed_smartlists.append(processed_smartlist)
            
            return processed_smartlists
            
        except Exception as e:
            print(f"Error fetching SmartLists: {e}")
            return []

    def get_smartlist_details(self, smartlist_id):
        """
        Fetches detailed information for a specific SmartList.
        
        Args:
            smartlist_id (str): The ID of the SmartList to fetch details for.
            
        Returns:
            dict: SmartList details including fields, items, and settings.
        """
        try:
            response = self._make_request("GET", f"smartlist/{smartlist_id}")
            return response
        except Exception as e:
            print(f"Error fetching SmartList details for ID {smartlist_id}: {e}")
            return {}


# Example Usage (for testing purposes when running this file directly)
if __name__ == "__main__":
    try:
        client = FormstackClient()
        
        # Test fetching all forms
        forms = client.get_all_forms()
        print(f"\nFound {len(forms)} forms.")
        if forms:
            print("First form details:")
            print(forms[0]) # Print details of the first form for inspection
            # Expected to see 'created' and 'last_submission_time' here
        else:
            print("No forms found.")

        # Test fetching all folders
        folders = client.get_all_folders()
        print(f"\nFound {len(folders)} basic folders.")
        if folders:
            print("First basic folder details:")
            print(folders[0]) # Print details of the first folder for inspection

        # Test fetching complete folder hierarchy
        complete_folders = client.get_complete_folder_hierarchy()
        print(f"\nFound {len(complete_folders)} folders with complete hierarchy.")
        if complete_folders:
            print("First complete folder details:")
            print(complete_folders[0]) # Print details of the first folder for inspection
        else:
            print("No complete folder hierarchy found.")

        # Test fetching all smartlists
        smartlists = client.get_all_smartlists()
        print(f"\nFound {len(smartlists)} SmartLists.")
        if smartlists:
            print("First SmartList details:")
            print(smartlists[0]) # Print details of the first smartlist for inspection
        else:
            print("No SmartLists found.")

    except ValueError as ve:
        print(f"Configuration error during client test: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred during client test: {e}")

