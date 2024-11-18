from typing import Dict, List, Optional
import re
import logging

class DataValidator:
    """Validate input data and extraction results"""
    
    def __init__(self):
        self.email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        self.phone_pattern = re.compile(r'^\+?[\d\s-]{10,}$')
    
    def validate_input_data(
        self,
        df,
        required_columns: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Validate input DataFrame
        
        Args:
            df: Input DataFrame
            required_columns: List of required column names
        Returns:
            Dictionary of validation results
        """
        results = {
            'empty': not df.empty,
            'has_required_columns': True,
            'no_null_values': True
        }
        
        if required_columns:
            results['has_required_columns'] = all(
                col in df.columns for col in required_columns
            )
        
        if results['has_required_columns'] and required_columns:
            results['no_null_values'] = not df[required_columns].isnull().any().any()
        
        return results
    
    def validate_extracted_info(
        self,
        info: str,
        info_type: str
    ) -> bool:
        """
        Validate extracted information based on type
        
        Args:
            info: Extracted information string
            info_type: Type of information ('email', 'phone', 'text')
        Returns:
            True if valid, False otherwise
        """
        if not info:
            return False
            
        if info_type == 'email':
            return bool(self.email_pattern.match(info))
            
        elif info_type == 'phone':
            return bool(self.phone_pattern.match(info))
            
        elif info_type == 'text':
            return len(info.strip()) > 0
            
        else:
            logging.warning(f"Unknown info type: {info_type}")
            return True  # Default to true for unknown types