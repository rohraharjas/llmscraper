import os
from typing import Dict, List
import logging

def perform_web_search(entity: str, prompt: str, client) -> List[Dict]:
    """
    Perform web search for given entity using SerpAPI
    
    Args:
        entity: The entity to search for
        prompt: The search prompt template
    
    Returns:
        List of search results with urls and snippets
    """
    search_query = prompt.replace("{entity}", entity)
    
    try:
        
        results = client.search(q=search_query)
        if "organic_results" not in results:
            return results
        return [
            {
                "url": result.get("link"),
                "snippet": result.get("snippet", "")
            }
            for result in results["organic_results"]
        ]
    
    except Exception as e:
        logging.error(f"Search failed for {entity}: {str(e)}")
        return []