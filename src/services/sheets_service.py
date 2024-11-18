from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pandas as pd
import os
import json
import logging
from typing import Optional

def connect_google_sheet(sheet_url: str) -> Optional[pd.DataFrame]:
    """
    Connect to Google Sheet and return data as DataFrame
    
    Args:
        sheet_url: URL of the Google Sheet
    
    Returns:
        DataFrame containing sheet data or None if connection fails
    """
    try:
        # Extract sheet ID from URL
        sheet_id = sheet_url.split('/')[5]
        
        # Load credentials
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        if not creds_json:
            logging.error("Google Sheets credentials not found")
            return None
            
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_authorized_user_info(creds_dict)
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        # Get sheet data
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='A1:Z1000'  # Adjust range as needed
        ).execute()
        
        # Convert to DataFrame
        values = result.get('values', [])
        if not values:
            logging.error("No data found in sheet")
            return None
            
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
        
    except Exception as e:
        logging.error(f"Failed to connect to Google Sheet: {str(e)}")
        return None