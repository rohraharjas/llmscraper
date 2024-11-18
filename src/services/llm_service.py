from typing import Dict, List
import os
import groq
from langchain.prompts import PromptTemplate
import logging

def process_with_llm(search_results: List[Dict], prompt: str, entity: str, client) -> str:
    """
    Process search results with Groq LLM to extract required information
    
    Args:
        search_results: List of search results (urls and snippets)
        prompt: Original prompt template
        entity: Entity being processed
    
    Returns:
        Extracted information as string
    """
    # Combine all snippets
    context = "\n".join([result["snippet"] for result in search_results])
    
    # Create LLM prompt
    extraction_prompt = PromptTemplate(
        input_variables=["context", "entity", "task"],
        template="""
        Based on the following context, {task} for {entity}.
        Give the shortest reply possible.
        If the information is not found, respond with "Information not found".
        Please answer the following question concisely, providing only the necessary information. Avoid unnecessary details, explanations, or elaborations. Your response should be direct and to the point.
        
        Context:
        {context}
        """
    )
    
    try:
        
        # Format the prompt
        formatted_prompt = extraction_prompt.format(
            context=context,
            entity=entity,
            task=prompt.replace("{entity}", entity)
        )
        
        # Call Groq API
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": formatted_prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=10
        )
        print("success")
        return completion.choices[0].message.content
        
    except Exception as e:
        logging.error(f"LLM processing failed for {entity}: {str(e)}")
        return "Error during processing"