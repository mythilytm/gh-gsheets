import os
import json
import sys
import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError
from datetime import datetime
import getpass
import subprocess

def main():
    try:
        # Load credentials from the environment variable
        credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        sheet_id = os.getenv('GOOGLE_SHEET_ID')
        if not credentials_json:
            raise ValueError("Credentials JSON not found in environment variable.")
        if not sheet_id:
            raise ValueError("Sheet ID not found in environment variable.")

        credentials_data = json.loads(credentials_json)
        print("Credentials loaded successfully.")

        # Define the scope and credentials
        scopes = [
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.file'
        ]
        credentials = Credentials.from_service_account_info(credentials_data, scopes=scopes)
        print("Credentials initialized successfully.")

        # Initialize the client
        client = gspread.authorize(credentials)
        print("Google Sheets client authorized successfully.")

        # Open the Google Sheet by name'
        sheet = client.open_by_key(sheet_id).worksheet("DeploymentMatrix")
        print("Google Sheet opened successfully.")

        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        deployer_name = getpass.getuser()
        try:
          commit_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        except subprocess.CalledProcessError:
          commit_sha = "N/A"
        
        try:
          # Get the current Git branch name
          current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        except subprocess.CalledProcessError:
          current_branch = "N/A"

        try:
          # Get the tag that exactly matches the current commit
          current_tag = subprocess.check_output(["git", "describe", "--tags", "--exact-match"]).decode().strip()
        except subprocess.CalledProcessError:
          current_tag = "N/A"

        new_row_data = [current_date_time, "flex-plugins", "AS_development", "", deployer_name, current_branch, commit_sha, current_tag]  
        update_response = sheet.append_row(new_row_data)
        print("Sheet update response")

        # Verify update response
        if not update_response:
            raise RuntimeError("Failed to update the Google Sheet.")

        print("Google Sheet updated successfully.")

    except (GoogleAuthError, ValueError, RuntimeError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
