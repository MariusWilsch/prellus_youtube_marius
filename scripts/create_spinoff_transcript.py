#!/usr/bin/env python3
"""
Create Spinoff Transcript

This script generates a focused spinoff narrative from an existing processed transcript.
It uses the Google GenerativeAI SDK to create a more focused version of the original
transcript based on a specific theme or angle.

Usage:
    python create_spinoff_transcript.py --source-dir=<source_dir> --theme=<theme> --output-dir=<output_dir>

Example:
    python create_spinoff_transcript.py \
        --source-dir=data/transcripts/MiD839yU8vU_20250320_153803 \
        --theme="The Economic Motivations Behind the British Empire" \
        --output-dir=data/transcripts/MiD839yU8vU_20250320_spinoff

The script requires the GOOGLE_API_KEY environment variable to be set for Gemini API access.
"""

import os
import json
import time
import argparse
import logging
import sys
from datetime import datetime
import google.generativeai as genai
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('spinoff_transcript.log')
    ]
)

logger = logging.getLogger(__name__)

# Spinoff generation system prompt
SPINOFF_PROMPT = """
You are a specialized historical narrator focusing on creating spinoff narratives from comprehensive historical content.

TASK DESCRIPTION:
Your task is to transform a comprehensive historical transcript into a more focused narrative that explores a specific theme or aspect of the original content. You should:

1. Create a narrative that focuses exclusively on the theme: "{theme}"
2. Extract relevant information from the original transcript related to this theme
3. Organize this information into a coherent, engaging narrative
4. Add context and analysis specific to this theme
5. Maintain historical accuracy and educational value

INPUT FORMAT:
The input will be a processed historical transcript covering a broad range of topics and events.

OUTPUT GUIDELINES:

Content Selection:
<select>
- Information specifically related to the theme "{theme}"
- Key events, figures, and developments relevant to this theme
- Connections between events that highlight this theme
</select>

Content Organization:
<organize>
- Create a coherent narrative flow focused on the theme
- Provide a clear introduction that establishes the theme
- Develop the theme chronologically or thematically as appropriate
- Conclude with insights about the theme's significance
</organize>

Style and Tone:
<style>
- Maintain an engaging, educational tone
- Use descriptive language to bring historical events to life
- Balance factual information with analysis
- Ensure accessibility to a general audience interested in history
</style>

IMPORTANT RULES:
- Do NOT include information unrelated to the specified theme
- Do NOT contradict historical facts presented in the original
- Do NOT fabricate historical events not mentioned in the original
- Maintain approximately 2,000-3,000 words for the spinoff transcript
- Include a title that clearly indicates the focus of the spinoff

OUTPUT FORMAT:
Your output should be a well-structured historical narrative focusing specifically on the theme "{theme}".
Include a title at the beginning and organize the content with appropriate headings and paragraphs.
"""

def create_spinoff_transcript(
    source_dir: str,
    theme: str,
    output_dir: Optional[str] = None,
    model: str = "models/gemini-2.0-flash-lite"
) -> Dict[str, Any]:
    """
    Creates a spinoff transcript from an existing processed transcript based on a specific theme.
    
    Args:
        source_dir: Directory containing the original processed transcript
        theme: Theme or focus for the spinoff transcript
        output_dir: Directory to save the spinoff transcript (defaults to source_dir + "_spinoff")
        model: Gemini model to use for generating the spinoff
        
    Returns:
        Dict containing metadata about the spinoff generation process
    """
    start_time = time.time()
    logger.info(f"Creating spinoff transcript with theme: '{theme}'")
    
    # Set default output directory if not provided
    if not output_dir:
        output_dir = f"{source_dir}_spinoff"
    
    # Ensure output directory exists
    os.makedirs(os.path.join(output_dir, "processed"), exist_ok=True)
    
    # Check for API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")
    
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # Read the original processed transcript
    original_transcript_path = os.path.join(source_dir, "processed", "narrative_transcript.txt")
    if not os.path.exists(original_transcript_path):
        raise FileNotFoundError(f"Original processed transcript not found at {original_transcript_path}")
    
    with open(original_transcript_path, 'r', encoding='utf-8') as f:
        original_transcript = f.read()
    
    logger.info(f"Read original transcript ({len(original_transcript)} characters)")
    
    # Prepare the prompt with the specific theme
    prompt = SPINOFF_PROMPT.format(theme=theme)
    
    # Generate the spinoff transcript
    try:
        logger.info(f"Generating spinoff transcript using model: {model}")
        
        # Initialize the model
        gen_model = genai.GenerativeModel(model)
        
        # Generate content
        response = gen_model.generate_content(
            f"{prompt}\n\nORIGINAL TRANSCRIPT:\n\n{original_transcript}",
            generation_config={
                "max_output_tokens": 4096,
                "temperature": 0.7
            }
        )
        
        spinoff_transcript = response.text
        logger.info(f"Successfully generated spinoff transcript ({len(spinoff_transcript)} characters)")
        
    except Exception as e:
        logger.error(f"Error generating spinoff transcript: {str(e)}")
        raise
    
    # Save the spinoff transcript
    spinoff_path = os.path.join(output_dir, "processed", "spinoff_transcript.txt")
    with open(spinoff_path, 'w', encoding='utf-8') as f:
        f.write(spinoff_transcript)
    
    # Create metadata
    processing_time = time.time() - start_time
    metadata = {
        "original_transcript_dir": source_dir,
        "theme": theme,
        "model": model,
        "processing_time_seconds": processing_time,
        "original_length": len(original_transcript),
        "spinoff_length": len(spinoff_transcript),
        "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save metadata
    metadata_path = os.path.join(output_dir, "processed", "spinoff_metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Copy original metadata file if it exists
    original_metadata_path = os.path.join(source_dir, "metadata.json")
    if os.path.exists(original_metadata_path):
        with open(original_metadata_path, 'r', encoding='utf-8') as f:
            original_metadata = json.load(f)
        
        # Add spinoff info to metadata
        original_metadata["spinoff_info"] = {
            "theme": theme,
            "creation_date": metadata["creation_date"]
        }
        
        # Save updated metadata
        with open(os.path.join(output_dir, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(original_metadata, f, indent=2)
    
    logger.info(f"Spinoff transcript saved to {spinoff_path}")
    logger.info(f"Metadata saved to {metadata_path}")
    
    return metadata

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Create a spinoff transcript from an existing processed transcript.")
    parser.add_argument(
        "--source-dir", 
        required=True, 
        help="Directory containing the original processed transcript"
    )
    parser.add_argument(
        "--theme", 
        required=True, 
        help="Theme or focus for the spinoff transcript"
    )
    parser.add_argument(
        "--output-dir", 
        help="Directory to save the spinoff transcript (defaults to source_dir + '_spinoff')"
    )
    parser.add_argument(
        "--model", 
        default="models/gemini-2.0-flash-lite",
        help="Gemini model to use (default: models/gemini-2.0-flash-lite)"
    )
    
    args = parser.parse_args()
    
    try:
        metadata = create_spinoff_transcript(
            source_dir=args.source_dir,
            theme=args.theme,
            output_dir=args.output_dir,
            model=args.model
        )
        
        # Print summary
        print("\nSpinoff transcript creation completed:")
        print(f"  Theme: {metadata['theme']}")
        print(f"  Original length: {metadata['original_length']} characters")
        print(f"  Spinoff length: {metadata['spinoff_length']} characters")
        print(f"  Processing time: {metadata['processing_time_seconds']:.2f} seconds")
        print(f"  Model used: {metadata['model']}")
        
    except Exception as e:
        logger.error(f"Failed to create spinoff transcript: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 