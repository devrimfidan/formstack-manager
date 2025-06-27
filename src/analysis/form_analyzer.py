# src/analysis/form_analyzer.py
from datetime import datetime
import pandas as pd # Used for robust date parsing and DataFrame creation

class FormAnalyzer:
    """
    Analyzes Formstack form data, extracting key information like
    creation dates, last submission dates, associated folder names,
    and additional form metrics.
    """
    def __init__(self, formstack_client):
        """
        Initializes the FormAnalyzer with a FormstackClient instance.

        Args:
            formstack_client: An instance of FormstackClient to make API calls.
        """
        self.client = formstack_client

    def _parse_formstack_date(self, date_string):
        """
        Parses a Formstack API date string (e.g., "YYYY-MM-DD HH:MM:SS") into a datetime object.
        Uses pandas.to_datetime for robustness.

        Args:
            date_string (str): The date string from Formstack API.

        Returns:
            datetime.datetime or pd.NaT: The parsed datetime object, or pd.NaT if parsing fails.
        """
        if not date_string:
            return pd.NaT # Use Pandas Not a Time for null dates
        try:
            # pandas.to_datetime is robust and can often infer the format.
            # If not, you might specify format='%Y-%m-%d %H:%M:%S'
            return pd.to_datetime(date_string, errors='coerce')
        except Exception as e:
            print(f"Warning: Could not parse date string '{date_string}': {e}")
            return pd.NaT

    def get_form_summary_data(self):
        """
        Fetches all forms and folders, then extracts creation date,
        latest submission date, associated folder name, and other metrics
        for each form.

        Returns:
            list: A list of dictionaries, where each dictionary contains
                  summary information for a form (id, name, created_at,
                  last_submission_at, folder_name, submissions_count,
                  submissions_unread_count, views_count, form_url, is_inactive).
                  Dates are datetime objects (or pd.NaT).
        """
        all_forms_summary = []
        
        # 1. Fetch all forms
        forms = self.client.get_all_forms() 
        if not forms:
            print("No forms found to analyze.")
            return []

        # 2. Fetch all folders and create a lookup map
        folders = self.client.get_all_folders()
        # Create a dictionary mapping folder ID to folder name for quick lookup
        folder_map = {folder.get('id'): folder.get('name', 'Unknown Folder') for folder in folders}

        # 3. Process each form
        for form in forms:
            form_id = form.get('id')
            form_name = form.get('name', 'Untitled Form') # Provide a default name
            
            # Retrieve basic dates and IDs
            form_created_at_str = form.get('created') 
            last_submission_time_str = form.get('last_submission_time')
            folder_id = form.get('folder')

            # Retrieve new fields
            submissions_count = int(form.get('submissions', 0)) # Convert to int, default to 0
            submissions_unread_count = int(form.get('submissions_unread', 0)) # Convert to int, default to 0
            views_count = int(form.get('views', 0)) # Convert to int, default to 0
            form_url = form.get('url', '') # Get form URL
            is_inactive = bool(form.get('inactive', False)) # Convert to boolean

            # Look up folder name
            folder_name = folder_map.get(folder_id, 'Uncategorized Forms') 

            # Parse dates
            form_created_at = self._parse_formstack_date(form_created_at_str)
            last_submission_date = self._parse_formstack_date(last_submission_time_str)

            all_forms_summary.append({
                'id': form_id,
                'name': form_name,
                'folder_name': folder_name, 
                'created_at': form_created_at, 
                'last_submission_at': last_submission_date,
                'submissions_count': submissions_count, # New field
                'submissions_unread_count': submissions_unread_count, # New field
                'views_count': views_count, # New field
                'form_url': form_url, # New field
                'is_inactive': is_inactive # New field
            })
        
        return all_forms_summary

# Example Usage (for testing purposes when running this file directly)
if __name__ == "__main__":
    from src.api.formstack_client import FormstackClient
    try:
        # Ensure your .env is set up for the client
        client = FormstackClient() 
        analyzer = FormAnalyzer(client)
        
        print("Starting form analysis...")
        summary_data = analyzer.get_form_summary_data()

        if summary_data:
            df = pd.DataFrame(summary_data)
            # Format dates for display
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
            df['last_submission_at'] = df['last_submission_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('No Submissions')
            
            # Convert boolean to a more readable string
            df['is_inactive'] = df['is_inactive'].apply(lambda x: 'Yes' if x else 'No')

            # Sort for better readability (e.g., by folder then creation date)
            df_sorted = df.sort_values(by=['folder_name', 'created_at'], ascending=[True, False])
            
            print("\n--- Form Summary Report (with More Details) ---")
            print(df_sorted.to_string(index=False)) # Print full DataFrame
        else:
            print("No form summary data generated.")

    except ValueError as ve:
        print(f"Configuration error during analyzer test: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred during analyzer test: {e}")
