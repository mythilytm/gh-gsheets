import os
import json
import sys
import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

def main():
    try:
        # Load credentials from the environment variable
        credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        if not credentials_json:
            raise ValueError("No credentials found in environment variable.")

        credentials_data = json.loads(credentials_json)

        # Define the scope and credentials
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_info(credentials_data, scopes=scopes)

        # Initialize the client
        client = gspread.authorize(credentials)

        # Open the Google Sheet by name
        sheet = client.open("Product Matrices").worksheet("Deployment Matrix")

        # Update the sheets
        update_response = sheet.update('B2', 'Hello, sheet!')

        # Verify update response
        if not update_response:
            raise RuntimeError("Failed to update the Google Sheet.")

        print("Google Sheet updated successfully.")

    except (GoogleAuthError, ValueError, RuntimeError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
