import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Load credentials from the environment variable
credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
credentials_data = json.loads(credentials_json)

# Define the scope and credentials

credentials = Credentials.from_service_account_info(credentials_data, 'https://www.googleapis.com/auth/spreadsheets')

# Initialize the client
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open("Product Matrices").worksheet("Deployment Matrix")

# Update the sheet
sheet.update('B2', 'Hello, sheet!')

print('Sheet updated successfully!')