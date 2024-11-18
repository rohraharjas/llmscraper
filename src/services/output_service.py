from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
import json
import logging

class OutputHandler:
    """Handle different output formats and destinations"""
    
    def __init__(self):
        self.sheets_service = None
    
    def initialize_sheets(self, credentials_json: str):
        """Initialize Google Sheets service"""
        try:
            creds_dict = json.loads(credentials_json)
            creds = Credentials.from_authorized_user_info(creds_dict)
            self.sheets_service = build('sheets', 'v4', credentials=creds)
        except Exception as e:
            logging.error(f"Failed to initialize Sheets service: {str(e)}")
            raise
    
    def save_to_sheets(
        self,
        results: Dict,
        spreadsheet_id: str,
        range_name: str
    ) -> bool:
        """
        Save results to Google Sheets
        
        Args:
            results: Results dictionary
            spreadsheet_id: Target spreadsheet ID
            range_name: Target range (e.g., 'Sheet1!A1')
        Returns:
            True if successful, False otherwise
        """
        if not self.sheets_service:
            raise ValueError("Sheets service not initialized")
        
        try:
            # Convert results to 2D array
            data = [["Entity", "Extracted Information"]]
            for entity, info in results.items():
                data.append([entity, info])
            
            body = {
                'values': data
            }
            
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to save to sheets: {str(e)}")
            return False
    
    def format_results(
        self,
        results: Dict,
        output_format: str = 'csv'
    ) -> Optional[str]:
        """
        Format results in specified format
        
        Args:
            results: Results dictionary
            output_format: Desired output format ('csv' or 'json')
        Returns:
            Formatted string or None if format not supported
        """
        try:
            if output_format == 'csv':
                df = pd.DataFrame.from_dict(
                    results,
                    orient='index',
                    columns=['Extracted Information']
                )
                return df.to_csv()
                
            elif output_format == 'json':
                return json.dumps(results, indent=2)
                
            else:
                logging.warning(f"Unsupported output format: {output_format}")
                return None
                
        except Exception as e:
            logging.error(f"Error formatting results: {str(e)}")
            return None
