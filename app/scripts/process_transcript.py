#!/usr/bin/env python3
"""
Transcript Processing Script

This script processes YouTube transcripts using the AI Processor. It transforms
fetched transcripts into engaging narratives while preserving the educational content.
By default, it uses the cost-efficient gemini-2.0-flash-lite model.

Usage:
    python process_transcript.py [options]

Example:
    python process_transcript.py --video-id=GBbUmiH23-0
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add the parent directory to the Python path to import the package
sys.path.append(str(Path(__file__).parent.parent))

from src.transcript_pipeline.processor.ai_processor import process_transcript
from src.transcript_pipeline.utils.config import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_newest_transcript_dir(video_id: str, base_dir: str = "data/transcripts") -> str:
    """
    Find the most recently created transcript directory for a given video ID.

    Args:
        video_id: The YouTube video ID to find transcripts for
        base_dir: The base directory where transcripts are stored

    Returns:
        The path to the most recent transcript directory
    """
    video_dir = os.path.join(base_dir, video_id)
    if not os.path.exists(video_dir):
        raise FileNotFoundError(
            f"No transcript directory found for video ID: {video_id}"
        )

    # Get all timestamp-based directories and sort by name (which is timestamp)
    timestamp_dirs = [
        d for d in os.listdir(video_dir) if os.path.isdir(os.path.join(video_dir, d))
    ]
    if not timestamp_dirs:
        raise FileNotFoundError(f"No transcript directories found in {video_dir}")

    # Sort by timestamp (newest first)
    timestamp_dirs.sort(reverse=True)

    # Return the newest directory
    newest_dir = os.path.join(video_dir, timestamp_dirs[0])
    return newest_dir


def main():
    """Main function to parse arguments and process the transcript."""
    parser = argparse.ArgumentParser(
        description="Process a YouTube transcript using AI"
    )
    parser.add_argument("--video-id", help="YouTube video ID to process")
    parser.add_argument("--transcript-dir", help="Path to the transcript directory")
    parser.add_argument(
        "--config",
        default="app/config/config.yaml",
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.0-flash-lite",
        help="Override the model specified in the config (default: gemini-2.0-flash-lite)",
    )
    parser.add_argument(
        "--mock", action="store_true", help="Run in mock mode without making API calls"
    )
    args = parser.parse_args()

    # Check for the presence of the mock mode environment variable
    mock_mode = args.mock or os.environ.get("MOCK_LLM_API") == "true"

    # Load configuration
    config = load_config(args.config)

    # Override model if specified or use default
    if args.model:
        config["ai"]["model"] = args.model
    else:
        # Ensure we're using the cheapest model by default
        config["ai"]["model"] = "gemini-2.0-flash-lite"

    # Determine the transcript directory
    if args.transcript_dir:
        transcript_dir = args.transcript_dir
    elif args.video_id:
        try:
            transcript_dir = get_newest_transcript_dir(args.video_id)
        except FileNotFoundError as e:
            logger.error(str(e))
            return 1
    else:
        logger.error("Either --video-id or --transcript-dir must be specified")
        return 1

    try:
        # Process the transcript
        logger.info(f"Processing transcript using model: {config['ai']['model']}")
        result = process_transcript(transcript_dir, config, mock_mode=mock_mode)

        # Print processing results
        print(f"\nProcessing completed:")
        print(f"  Model used: {config['ai']['model']}")
        print(f"  Original length: {result['original_length']} characters")
        print(f"  Processed length: {result['processed_length']} characters")
        print(f"  Processing time: {result['processing_time_seconds']:.2f} seconds")
        print(
            f"  Is large transcript: {'Yes' if result.get('large_transcript', False) else 'No'}"
        )
        print(f"  Processing method: {result.get('processing_method', 'standard')}")

        # Print file paths
        processed_file = os.path.join(
            transcript_dir, "processed", "narrative_transcript.txt"
        )
        print(f"\nProcessed transcript saved to:")
        print(f"  {processed_file}")

        # Print sample of the processed text
        with open(processed_file, "r", encoding="utf-8") as f:
            sample_text = f.read(500)

        print("\nSample of processed transcript:")
        print("=" * 80)
        print(sample_text + "...")
        print("=" * 80)

        return 0

    except Exception as e:
        logger.exception(f"Error processing transcript: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
