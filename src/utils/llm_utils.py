from typing import Dict, List, Optional
import json
import logging

def format_prompt_template(template: str, entity: str, context: Optional[str] = None) -> str:
    """
    Format prompt template with entity and optional context
    
    Args:
        template: Prompt template string
        entity: Entity to extract information for
        context: Optional context to include
    Returns:
        Formatted prompt
    """
    prompt = template.replace("{entity}", entity)
    
    if context:
        prompt = f"{prompt}\n\nContext:\n{context}"
    
    return prompt

def parse_llm_response(response: str) -> Dict:
    """
    Parse LLM response into structured format
    
    Args:
        response: Raw LLM response
    Returns:
        Structured response dictionary
    """
    try:
        # Check if response is JSON
        if response.strip().startswith('{') and response.strip().endswith('}'):
            return json.loads(response)
        
        # If not JSON, return as simple text
        return {"text": response.strip()}
    
    except json.JSONDecodeError:
        return {"text": response.strip()}
    
    except Exception as e:
        logging.error(f"Error parsing LLM response: {str(e)}")
        return {"error": "Failed to parse response"}

def validate_extraction(extracted_info: Dict) -> bool:
    """
    Validate extracted information
    
    Args:
        extracted_info: Dictionary of extracted information
    Returns:
        True if valid, False otherwise
    """
    if not extracted_info:
        return False
    
    if "error" in extracted_info:
        return False
    
    # Check if we have any actual content
    if "text" in extracted_info and not extracted_info["text"]:
        return False
    
    return True