#!/usr/bin/env python3
"""
Example script demonstrating how to use the Transcript AI Processor API programmatically.

This script shows how to:
1. Process a transcript using the API
2. Access the processed transcript information
3. Use the mock mode for testing without API access

Usage:
    python examples/use_transcript_processor.py
"""

import os
import sys
import logging
from pathlib import Path
import json

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.transcript_pipeline.processor.ai_processor import process_transcript

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Example usage of the transcript processor API."""
    
    # Enable mock mode for testing without API access
    os.environ["MOCK_LLM_API"] = "true"
    
    # Find the most recent transcript directory
    import glob
    from datetime import datetime
    
    transcript_dirs = glob.glob(os.path.join(project_root, "data", "transcripts", "*_*"))
    if not transcript_dirs:
        print("No transcript directories found.")
        return 1
        
    # Sort by creation time (newest first)
    transcript_dirs.sort(key=lambda x: os.path.getctime(x), reverse=True)
    most_recent_dir = transcript_dirs[0]
    
    # Example 1: Process the most recent transcript
    print(f"\n--- Example 1: Process the most recent transcript ({os.path.basename(most_recent_dir)}) ---")
    result = process_transcript(most_recent_dir)
    
    # Access information about the processed transcript
    print(f"Directory: {result['video_dir']}")
    print(f"Processed text file: {result['processed_text_path']}")
    print(f"Processed JSON file: {result['processed_json_path']}")
    print(f"Model used: {result['processing_info']['model']}")
    print(f"Processed at: {result['processing_info']['processed_at']}")
    
    # Load the JSON file to access metadata
    with open(result['processed_json_path'], 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        
    # Display metadata
    print(f"Video ID: {json_data['metadata'].get('video_id', 'Unknown')}")
    print(f"Video URL: {json_data['metadata'].get('video_url', 'Unknown')}")
    
    # Example 2: Process a specific transcript with custom settings
    print("\n--- Example 2: Process with custom settings ---")
    # Specify the transcript directory and model
    transcript_dir = result['video_dir']  # Reuse the directory from previous example
    config = {
        "ai": {
            "model": "gemini-pro-flash-1",
            "temperature": 0.5
        }
    }
    
    # Process with custom settings
    custom_result = process_transcript(transcript_dir, config)
    print(f"Processed with custom model: {custom_result['processing_info']['model']}")
    print(f"Temperature: {custom_result['processing_info']['temperature']}")
    
    # Example 3: Print a sample of the processed text
    print("\n--- Example 3: Sample of processed text ---")
    with open(custom_result['processed_text_path'], 'r', encoding='utf-8') as f:
        sample = f.read(300)
        print(f"Sample:\n{sample}...")
    
    # Example 4: Show how to process multiple transcripts
    print("\n--- Example 4: Processing multiple transcripts ---")
    # In a real scenario, you would discover transcript directories 
    # and process them in a loop
    print("Demonstration of how to process multiple transcripts:")
    
    # Pseudo-code for batch processing:
    """
    import glob
    transcript_dirs = glob.glob(os.path.join(project_root, "data", "transcripts", "*_*"))
    
    for transcript_dir in transcript_dirs:
        print(f"Processing {transcript_dir}...")
        try:
            result = process_transcript(transcript_dir)
            print(f"Successfully processed {result['metadata']['video_id']}")
        except Exception as e:
            print(f"Error processing {transcript_dir}: {e}")
    """
    
    print("For batch processing, discover transcript directories and process them in a loop")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 