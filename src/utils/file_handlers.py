import pandas as pd
from typing import Optional
import io
import logging
from pathlib import Path

def process_uploaded_file(file: io.BytesIO) -> Optional[pd.DataFrame]:
    """
    Process uploaded CSV file and return as DataFrame
    
    Args:
        file: Uploaded file object
    Returns:
        DataFrame or None if processing fails
    """
    try:
        df = pd.read_csv(file)
        # Basic validation
        if df.empty:
            logging.error("Uploaded file is empty")
            return None
        
        # Remove any completely empty columns or rows
        df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
        
        return df
    
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return None

def save_results_to_csv(results: dict, filename: str) -> Path:
    """
    Save extraction results to CSV file
    
    Args:
        results: Dictionary of extraction results
        filename: Output filename
    Returns:
        Path to saved file
    """
    try:
        df = pd.DataFrame.from_dict(results, orient='index', columns=['extracted_info'])
        output_path = Path('outputs') / filename
        output_path.parent.mkdir(exist_ok=True)
        df.to_csv(output_path)
        return output_path
    
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")
        raise