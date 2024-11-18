from typing import List, Dict
import re
import logging
from urllib.parse import urlparse

def validate_search_results(results: List[Dict]) -> List[Dict]:
    """
    Validate and clean search results
    
    Args:
        results: List of search results
    Returns:
        Cleaned and validated results
    """
    cleaned_results = []
    
    for result in results:
        # Validate URL
        if 'url' in result and is_valid_url(result['url']):
            # Clean snippet text
            if 'snippet' in result:
                result['snippet'] = clean_text(result['snippet'])
            cleaned_results.append(result)
    
    return cleaned_results

def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove special characters and normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text