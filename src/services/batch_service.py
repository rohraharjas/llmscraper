from typing import List, Dict
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .search_service import perform_web_search
from .llm_service import process_with_llm

class BatchProcessor:
    """Handle batch processing of entities"""
    
    def __init__(self, max_workers: int = 3, batch_size: int = 10):
        self.max_workers = max_workers
        self.batch_size = batch_size
    
    def process_batch(
        self,
        entities: List[str],
        prompt: str,
        callback = None
    ) -> Dict[str, str]:
        """
        Process a batch of entities
        
        Args:
            entities: List of entities to process
            prompt: Prompt template
            callback: Optional progress callback function
        Returns:
            Dictionary of results
        """
        results = {}
        total = len(entities)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_entity = {
                executor.submit(self._process_entity, entity, prompt): entity
                for entity in entities
            }
            
            for i, future in enumerate(as_completed(future_to_entity)):
                entity = future_to_entity[future]
                try:
                    result = future.result()
                    results[entity] = result
                    
                    if callback:
                        callback((i + 1) / total)
                        
                except Exception as e:
                    logging.error(f"Error processing {entity}: {str(e)}")
                    results[entity] = f"Error: {str(e)}"
        
        return results
    
    def _process_entity(self, entity: str, prompt: str) -> str:
        """Process single entity"""
        search_results = perform_web_search(entity, prompt)
        return process_with_llm(search_results, prompt, entity)