#!/usr/bin/env python3
"""
YouTube Transcript Fetcher Script

This script fetches and stores a transcript from a YouTube video URL.
It creates a dedicated directory for the video and saves both raw JSON
and plain text versions of the transcript.

Usage:
    python scripts/fetch_youtube_transcript.py <youtube_url>

Example:
    python scripts/fetch_youtube_transcript.py https://www.youtube.com/watch?v=GBbUmiH23-0
"""

import os
import sys
import logging
import yaml
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.transcript_pipeline.fetcher.fetch_and_store import fetch_transcript

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("transcript_fetcher.log")
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path="config.yaml"):
    """Load configuration from YAML file."""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config.get("transcript", {})
    except Exception as e:
        logger.warning(f"Error loading configuration from {config_path}: {e}")
        return {}

def main():
    """Main function to fetch and store a YouTube transcript."""
    # Check if a YouTube URL was provided
    if len(sys.argv) < 2:
        print("Error: YouTube URL is required")
        print(f"Usage: python {sys.argv[0]} <youtube_url>")
        return 1
    
    youtube_url = sys.argv[1]
    
    try:
        # Load configuration
        config = load_config()
        
        # Fetch and store the transcript
        logger.info(f"Fetching transcript for: {youtube_url}")
        result = fetch_transcript(youtube_url, config)
        
        # Print information about the stored transcript
        print("\nTranscript successfully fetched and stored!")
        print(f"Video ID: {result['video_id']}")
        print(f"Directory: {result['video_dir']}")
        print(f"Raw transcript (JSON): {result['raw_transcript_path']}")
        print(f"Plain text transcript: {result['plain_text_path']}")
        
        # Print a sample of the transcript
        print("\nSample of the transcript:")
        with open(result['plain_text_path'], 'r', encoding='utf-8') as f:
            sample = f.read(500)
            if len(sample) >= 500:
                sample = sample[:497] + "..."
            print(sample)
        
        return 0
    
    except Exception as e:
        logger.exception(f"Error processing transcript: {e}")
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 