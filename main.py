# main.py
import pandas as pd
from src.api.formstack_client import FormstackClient
from src.analysis.form_analyzer import FormAnalyzer
import os
from dotenv import load_dotenv

# Load environment variables from .env file.
# This ensures that FORMSTACK_API_KEY is available for the client.
load_dotenv()

def run_command_line_report():
    """
    Runs the Formstack form summary report and prints it to the console.
    This function demonstrates how to use the client and analyzer outside of the Flask app.
    """
    try:
        # Initialize the Formstack client
        client = FormstackClient()

        # Initialize the form analyzer with the client
        analyzer = FormAnalyzer(client)

        # Get the summary data
        print("Generating Formstack form summary report...")
        form_summary = analyzer.get_form_summary_data()

        if form_summary:
            # Create a Pandas DataFrame for easy tabular data presentation and manipulation
            df = pd.DataFrame(form_summary)

            # Sort by creation date for better overview
            # Use na_position='last' to put forms with no creation date at the end
            df = df.sort_values(by='created_at', ascending=False, na_position='last')

            # Format dates for cleaner display in the console
            # .dt.strftime() converts datetime objects to strings
            # .fillna('N/A') handles cases where dates might be None
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
            df['last_submission_at'] = df['last_submission_at'].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('No Submissions')

            print("\n--- Form Summary Table ---")
            # Use df.to_string() to print the entire DataFrame without truncation
            # index=False prevents printing the DataFrame index
            print(df.to_string(index=False))

            # You can add further analysis or decision-making logic here
            # For example, identifying forms that might be candidates for deletion:
            # from datetime import datetime, timedelta
            # current_time = datetime.now()
            # for index, row in df.iterrows():
            #     if row['last_submission_at'] == 'No Submissions' and row['created_at'] != 'N/A':
            #         # Convert 'created_at' back to datetime for comparison if needed
            #         # For simplicity, using string comparison here, but proper date objects are better
            #         created_dt = pd.to_datetime(row['created_at'])
            #         if (current_time - created_dt).days > 365: # Older than 1 year and no submissions
            #             print(f"\nPotential candidate for deletion: Form '{row['name']}' (ID: {row['id']})")
            #             print(f"  Created: {row['created_at']}, No submissions yet.")

        else:
            print("No forms found or unable to retrieve form data.")

    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_command_line_report()

