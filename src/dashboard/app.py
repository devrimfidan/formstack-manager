# src/dashboard/app.py
from flask import Flask, render_template, request
from src.api.formstack_client import FormstackClient
from src.analysis.form_analyzer import FormAnalyzer
from src.analysis.folder_analyzer import FolderAnalyzer
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This ensures that FORMSTACK_API_KEY is available when FormstackClient is instantiated.
load_dotenv()

# Initialize Flask app
# template_folder specifies where Flask should look for HTML templates.
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    """
    Renders the main dashboard page, displaying a summary of Formstack forms.
    Fetches data from Formstack API, analyzes it, and passes it to the HTML template.
    """
    forms_for_template = []
    error_message = None

    try:
        # Initialize Formstack client and analyzer
        client = FormstackClient()
        analyzer = FormAnalyzer(client)
        
        # Get the summary data from the analyzer
        form_summary_data = analyzer.get_form_summary_data()

        if form_summary_data:
            # Create a Pandas DataFrame for easier manipulation and formatting
            df = pd.DataFrame(form_summary_data)
            
            # Sort the DataFrame by creation date in descending order
            if 'created_at' in df.columns and not df['created_at'].empty:
                df = df.sort_values(by='created_at', ascending=False, na_position='last')
            
            # Keep the full dataset for dashboard stats calculation
            full_forms_data = df.copy()
            
            # Limit to top 5 forms only for the home page display
            df = df.head(5)
            
            # Format datetime columns to readable strings for the template
            # .dt.strftime() works on datetime columns, .fillna() handles NaT (Not a Time) values
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
            df['last_submission_at'] = df['last_submission_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('No Submissions')
            
            # Format datetime columns for the full dataset as well (for stats calculation)
            full_forms_data['created_at'] = full_forms_data['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
            full_forms_data['last_submission_at'] = full_forms_data['last_submission_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('No Submissions')
            
            # Convert DataFrame to a list of dictionaries, suitable for Jinja2 template iteration
            forms_for_template = df.to_dict(orient='records')
            # Convert full dataset to list for stats calculation
            full_forms_for_template = full_forms_data.to_dict(orient='records')
        else:
            error_message = "No forms found or unable to retrieve form data from Formstack."

    except ValueError as ve:
        # Catch configuration errors (e.g., missing API key)
        error_message = f"Configuration Error: {ve}"
        print(f"Dashboard Configuration Error: {ve}") # Log the error
    except Exception as e:
        # Catch any other unexpected errors during data fetching or processing
        error_message = f"An unexpected error occurred: {e}"
        print(f"Dashboard Runtime Error: {e}") # Log the error

    # Render the index.html template, passing the processed data and any error message
    return render_template('index.html', forms=forms_for_template, all_forms=full_forms_for_template if 'full_forms_for_template' in locals() else forms_for_template, error=error_message)

@app.route('/folders')
def folders():
    """
    Renders the folders page, displaying a summary of Formstack folders.
    Fetches folder data from Formstack API, analyzes it, and passes it to the HTML template.
    """
    folders_for_template = []
    folder_stats = {}
    error_message = None

    try:
        # Initialize Formstack client and folder analyzer
        client = FormstackClient()
        folder_analyzer = FolderAnalyzer(client)
        
        # Get the folder summary data from the analyzer
        folder_summary_data = folder_analyzer.get_folder_summary_data()
        folder_stats = folder_analyzer.get_folder_stats()

        if folder_summary_data:
            # Create a Pandas DataFrame for easier manipulation and formatting
            df = pd.DataFrame(folder_summary_data)
            
            # Sort the DataFrame by folder path for logical hierarchy display
            if 'folder_path' in df.columns and not df['folder_path'].empty:
                df = df.sort_values(by='folder_path', ascending=True, na_position='last')
            
            # Format datetime columns to readable strings for the template
            if 'created_at' in df.columns and not df.empty:
                # Ensure created_at is datetime, then format it
                df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
                # Only apply strftime if there are actual datetime values
                if df['created_at'].notna().any():
                    df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
                else:
                    df['created_at'] = 'N/A'
            
            # Convert DataFrame to a list of dictionaries, suitable for Jinja2 template iteration
            folders_for_template = df.to_dict(orient='records')
        else:
            error_message = "No folders found or unable to retrieve folder data from Formstack."

    except ValueError as ve:
        # Catch configuration errors (e.g., missing API key)
        error_message = f"Configuration Error: {ve}"
        print(f"Folders Dashboard Configuration Error: {ve}") # Log the error
    except Exception as e:
        # Catch any other unexpected errors during data fetching or processing
        error_message = f"An unexpected error occurred: {e}"
        print(f"Folders Dashboard Runtime Error: {e}") # Log the error
        import traceback
        print(f"Full traceback: {traceback.format_exc()}") # Print full stack trace

    # Render the folders.html template, passing the processed data and any error message
    return render_template('folders.html', folders=folders_for_template, folder_stats=folder_stats, error=error_message)

@app.route('/form-details')
@app.route('/form-details/<form_id>')
def form_details(form_id=None):
    """
    Renders the form details page, displaying detailed information about a specific form.
    If form_id is provided, fetches and displays that form's details.
    If no form_id is provided, shows a form to enter the ID.
    """
    form_data = None
    partial_submissions = []
    confirmations = []
    notifications = []
    webhooks = []
    integrations = []
    fields = []
    error_message = None

    if form_id:
        try:
            # Initialize Formstack client
            client = FormstackClient()
            
            # Get the specific form details
            form_data = client.get_form_details(form_id)
            
            if form_data:
                # Fetch additional form-related data
                partial_submissions = client.get_form_partial_submissions(form_id)
                confirmations = client.get_form_confirmations(form_id)
                notifications = client.get_form_notifications(form_id)
                webhooks = client.get_form_webhooks(form_id)
                integrations = client.get_form_integrations(form_id)
                fields = client.get_form_fields(form_id)
            else:
                error_message = f"Form with ID {form_id} not found or could not be retrieved."

        except ValueError as ve:
            # Catch configuration errors (e.g., missing API key)
            error_message = f"Configuration Error: {ve}"
            print(f"Form Details Configuration Error: {ve}") # Log the error
        except Exception as e:
            # Catch any other unexpected errors during data fetching or processing
            error_message = f"An unexpected error occurred: {e}"
            print(f"Form Details Runtime Error: {e}") # Log the error

    # Render the form-details.html template, passing all the data
    return render_template('form-details.html', 
                         form_data=form_data, 
                         form_id=form_id, 
                         error=error_message,
                         partial_submissions=partial_submissions,
                         confirmations=confirmations,
                         notifications=notifications,
                         webhooks=webhooks,
                         integrations=integrations,
                         fields=fields)

@app.route('/advanced-search')
def advanced_search():
    """
    Renders the advanced search page where users can search forms based on
    specific configurations like webhooks, confirmations, notifications, etc.
    """
    forms_data = []
    error_message = None

    try:
        # Initialize Formstack client and analyzer
        client = FormstackClient()
        analyzer = FormAnalyzer(client)
        
        # Get all forms data
        form_summary_data = analyzer.get_form_summary_data()

        if form_summary_data:
            # Create a DataFrame for easier manipulation
            df = pd.DataFrame(form_summary_data)
            
            # Sort by creation date in descending order
            if 'created_at' in df.columns and not df['created_at'].empty:
                df = df.sort_values(by='created_at', ascending=False, na_position='last')
            
            # Format datetime columns
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
            df['last_submission_at'] = df['last_submission_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('No Submissions')
            
            # Convert to list of dictionaries
            forms_data = df.to_dict(orient='records')
        else:
            error_message = "No forms were retrieved from the Formstack API."

    except ValueError as ve:
        error_message = f"Configuration Error: {ve}"
        print(f"Advanced Search Configuration Error: {ve}")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"Advanced Search Runtime Error: {e}")

    return render_template('advanced-search.html', forms=forms_data, error=error_message)

@app.route('/api/advanced-search', methods=['POST'])
def api_advanced_search():
    """
    API endpoint for advanced search functionality.
    Returns forms with their configuration details (webhooks, confirmations, etc.)
    """
    try:
        # Get search parameters from request
        search_params = request.get_json()
        
        # Initialize Formstack client and analyzer
        client = FormstackClient()
        analyzer = FormAnalyzer(client)
        
        # Get all forms data
        form_summary_data = analyzer.get_form_summary_data()
        
        if not form_summary_data:
            return {'error': 'No forms found'}, 404
            
        # Create DataFrame for easier manipulation
        df = pd.DataFrame(form_summary_data)
        
        # Format datetime columns
        df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
        df['last_submission_at'] = df['last_submission_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('No Submissions')
        
        # Replace NaN and NaT values with JSON-serializable defaults
        df = df.fillna({
            'submissions_count': 0,
            'submissions_unread_count': 0,
            'views_count': 0,
            'form_url': '',
            'folder_name': 'Uncategorized',
            'name': 'Untitled Form'
        })
        
        # Convert to native Python types to avoid JSON serialization issues
        df['submissions_count'] = df['submissions_count'].astype(int)
        df['submissions_unread_count'] = df['submissions_unread_count'].astype(int)
        df['views_count'] = df['views_count'].astype(int)
        df['is_inactive'] = df['is_inactive'].astype(bool)
        
        forms_with_config = []
        
        # For each form, fetch configuration details if needed
        for _, form in df.iterrows():
            form_data = form.to_dict()
            
            # Check if we need configuration details
            need_config = (search_params.get('webhook_filter') or 
                          search_params.get('confirmation_filter') or 
                          search_params.get('notification_filter') or 
                          search_params.get('partial_filter'))
            
            if need_config:
                form_id = form_data['id']
                
                # Fetch configuration details
                webhooks = client.get_form_webhooks(form_id)
                confirmations = client.get_form_confirmations(form_id)
                notifications = client.get_form_notifications(form_id)
                partial_submissions = client.get_form_partial_submissions(form_id)
                
                # Add configuration flags
                form_data['has_webhooks'] = len(webhooks) > 0
                form_data['has_confirmations'] = len(confirmations) > 0
                form_data['has_notifications'] = len(notifications) > 0
                form_data['has_partial_submissions'] = len(partial_submissions) > 0
                form_data['webhook_count'] = len(webhooks)
                form_data['confirmation_count'] = len(confirmations)
                form_data['notification_count'] = len(notifications)
                form_data['partial_submission_count'] = len(partial_submissions)
            else:
                # Set default values if not needed
                form_data['has_webhooks'] = False
                form_data['has_confirmations'] = False
                form_data['has_notifications'] = False
                form_data['has_partial_submissions'] = False
                form_data['webhook_count'] = 0
                form_data['confirmation_count'] = 0
                form_data['notification_count'] = 0
                form_data['partial_submission_count'] = 0
            
            forms_with_config.append(form_data)
        
        return {'forms': forms_with_config}, 200
        
    except Exception as e:
        print(f"Advanced Search API Error: {e}")
        return {'error': str(e)}, 500

@app.route('/audit')
def audit():
    """
    Renders the Form Audit page, providing predefined filters for form analysis.
    """
    return render_template('audit.html')

@app.route('/smartlists')
def smartlists():
    """
    Renders the SmartLists page, displaying all SmartLists from Formstack.
    """
    smartlists_data = []
    error_message = None

    try:
        # Initialize Formstack client
        client = FormstackClient()
        
        # Get all SmartLists
        smartlists = client.get_all_smartlists()
        
        if smartlists:
            # Process SmartLists data for template
            smartlists_data = smartlists
        else:
            print("No SmartLists found or retrieved.")

    except ValueError as ve:
        error_message = f"Configuration error: {ve}"
        print(f"Configuration error in SmartLists route: {ve}")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"An unexpected error occurred in SmartLists route: {e}")

    return render_template('smartlists.html', smartlists=smartlists_data, error=error_message)

@app.route('/smartlist-details/<smartlist_id>')
def smartlist_details(smartlist_id):
    """
    Renders the SmartList details page for a specific SmartList.
    """
    smartlist_data = {}
    error_message = None

    try:
        # Initialize Formstack client
        client = FormstackClient()
        
        # Get SmartList details
        smartlist_data = client.get_smartlist_details(smartlist_id)
        
        if not smartlist_data:
            error_message = f"SmartList with ID {smartlist_id} not found."

    except ValueError as ve:
        error_message = f"Configuration error: {ve}"
        print(f"Configuration error in SmartList details route: {ve}")
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(f"An unexpected error occurred in SmartList details route: {e}")

    return render_template('smartlist-details.html', smartlist=smartlist_data, error=error_message)

if __name__ == '__main__':
    # Run the Flask development server
    # debug=True enables debug mode, which provides an interactive debugger
    # and automatically reloads the server on code changes.
    app.run(debug=True, port=5006)

