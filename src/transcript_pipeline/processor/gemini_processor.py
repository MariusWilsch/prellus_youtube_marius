"""
Gemini Processor Module

This module provides a specialized processor for handling transcript processing
using Google's Gemini API. It abstracts the details of interacting with the Gemini
models for text processing.
"""

import os
import logging
import google.generativeai as genai
from typing import Dict, Any, Optional, List
import time
# Replace the circular import with our interface
from .processor_base import TranscriptProcessorInterface

logger = logging.getLogger(__name__)





# Update to implement our interface
class GeminiProcessor(TranscriptProcessorInterface):
    """
    Processor for handling text processing using Google's Gemini API.
    
    This class provides methods for processing text inputs using Google's
    Gemini models, handling API interactions and response processing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Gemini processor.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.model = self.config.get("model", "gemini-2.0-flash-lite")
        self.max_tokens = self.config.get("max_tokens", 8192)
        self.temperature = self.config.get("temperature", 0.7)
        
        # Configure Google GenerativeAI
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            # Try to load from .env file if not in environment
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable must be set")
        
        # Configure Google GenerativeAI
        genai.configure(api_key=api_key)
        self.model_id = f"models/{self.model}" if not self.model.startswith("models/") else self.model
        
        logger.info(f"Initialized GeminiProcessor with model: {self.model_id}")
    
    def _process_with_model(
        self, prompt: str, max_retries: int = 3, safety_settings: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Process text with the Gemini model with retry logic.
        
        Args:
            prompt: The prompt to send to the model
            max_retries: Maximum number of retries on failure
            safety_settings: Optional safety settings to apply
            
        Returns:
            The model's response as a string
        """
        retry_count = 0
        last_error = None
        print("GOING INTO PROCESS MODEL IN GEMINI PROCESSOR")
        while retry_count < max_retries:
            try:
                # Create the Gemini model instance on demand
                model = genai.GenerativeModel(self.model_id, 
                                            generation_config={"temperature": self.temperature, 
                                                             "max_output_tokens": self.max_tokens})
                
                if safety_settings:
                    print(f"\n\nprompt in process_with_model: {prompt}\n\n")
                    response = model.generate_content(
                        prompt,
                        safety_settings=safety_settings
                    )
                else:
                    response = model.generate_content(prompt)
                
                # Check if response contains text
                if not hasattr(response, 'text'):
                    logger.warning(f"Response has no text attribute: {response}")
                    retry_count += 1
                    time.sleep(2 * retry_count)  # Exponential backoff
                    continue
                
                # Check if the response is too short (likely an error)
                response_text = response.text
                print(f"\n\nresponse_text in process_with_model: {response_text}\n\n")
                if len(response_text) < 50:
                    logger.warning(f"Response suspiciously short ({len(response_text)} chars): '{response_text}'")
                    retry_count += 1
                    time.sleep(2 * retry_count)  # Exponential backoff
                    continue
                
                logger.info(f"Received response from Gemini API. Response length: {len(response_text)} characters")
                    
                return response_text
                
            except Exception as e:
                last_error = e
                logger.warning(f"API error on attempt {retry_count + 1}/{max_retries}: {str(e)}")
                retry_count += 1
                
                # Implement exponential backoff
                sleep_time = 2 ** retry_count
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
        
        # If we've exhausted retries, log the error and raise an exception
        logger.error(f"Failed to process with Gemini after {max_retries} attempts. Last error: {last_error}")
        if last_error:
            raise last_error
        else:
            raise Exception(f"Failed to get valid response from Gemini after {max_retries} attempts")
            
    def process_text(self, text: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str:
        """
        Process a text using Gemini API.
        
        Args:
            text: The text to process
            system_prompt: Optional system prompt to guide processing
            model: Optional model name to override default
            
        Returns:
            The processed text
        """
        # Allow model override for specific calls
        print("\n\nprocess text in gemini processor\n\n")
        if model:
            original_model_id = self.model_id
            self.model_id = f"models/{model}" if not model.startswith("models/") else model
            logger.info(f"Temporarily using model: {self.model_id}")
        
        logger.info(f"Processing text with Gemini model: {self.model_id}")
        
        # For Gemini, combine the system prompt and user text
        combined_prompt = f"{system_prompt}\n\n{text}" if system_prompt else text
        logger.info(f"Using combined prompt (total length: {len(combined_prompt)})")
        
        try:
            # Process with retry logic
            result = self._process_with_model(combined_prompt)
        finally:
            # Restore original model if it was temporarily changed
            if model:
                self.model_id = original_model_id
                
        return result
        
    # Remove the process_transcript method that causes circular dependencies
    # It's better to handle transcript processing in the dedicated processor 