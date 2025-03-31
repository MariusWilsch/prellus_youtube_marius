#!/usr/bin/env python3
"""
Audio Generation Script

This script converts processed transcripts to audio using the Kokoro TTS engine.
It takes a transcript directory or video ID as input and produces an audio file.

Usage:
    python scripts/generate_audio.py [options]
    
Example:
    python scripts/generate_audio.py --video-id=GBbUmiH23-0
    python scripts/generate_audio.py --transcript-dir=data/transcripts/GBbUmiH23-0_20250320_141333
"""

import os
import sys
import logging
import argparse
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.transcript_pipeline.tts.tts_generator import generate_audio_from_transcript

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("tts_generator.log")
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path="config/config.yaml"):
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.warning(f"Error loading configuration from {config_path}: {e}")
        return {}

def get_newest_transcript_dir(video_id: str, base_dir: str = "data/transcripts") -> str:
    """
    Find the most recently created transcript directory for a given video ID.
    
    Args:
        video_id: The YouTube video ID to find transcripts for
        base_dir: The base directory where transcripts are stored
        
    Returns:
        The path to the most recent transcript directory
    """
    video_dirs = [d for d in os.listdir(base_dir) if d.startswith(video_id)]
    if not video_dirs:
        raise FileNotFoundError(f"No transcript directory found for video ID: {video_id}")
    
    # Sort by timestamp (newest first)
    video_dirs.sort(reverse=True)
    
    # Return the newest directory
    newest_dir = os.path.join(base_dir, video_dirs[0])
    return newest_dir

def main():
    """Main function to parse arguments and generate audio from transcripts."""
    parser = argparse.ArgumentParser(description="Generate audio from processed transcript")
    parser.add_argument("--video-id", help="YouTube video ID to process")
    parser.add_argument("--transcript-dir", help="Path to the transcript directory")
    parser.add_argument("--config", default="config/config.yaml", help="Path to the configuration file")
    parser.add_argument("--voice-pack", help="Name of the Kokoro voice pack to use")
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
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
    
    # Override voice pack if specified
    if args.voice_pack:
        if "tts" not in config:
            config["tts"] = {}
        config["tts"]["voice_pack"] = args.voice_pack
    
    try:
        # Generate audio
        logger.info(f"Generating audio for transcript in: {transcript_dir}")
        result = generate_audio_from_transcript(transcript_dir, config)
        
        # Print results
        print(f"\nAudio generation completed:")
        print(f"  Output: {result['output_path']}")
        print(f"  Duration: {result['audio_duration_seconds']:.2f} seconds")
        print(f"  Processing time: {result['processing_time_seconds']:.2f} seconds")
        print(f"  Chunks processed: {result['chunks_processed']}")
        
        # Play a preview if on a system with audio playback capabilities
        try:
            import platform
            if platform.system() == "Darwin":  # macOS
                print("\nPlaying audio preview (first 5 seconds)...")
                os.system(f"afplay -t 5 {result['output_path']}")
            elif platform.system() == "Linux":
                print("\nTo play the audio, run:")
                print(f"  aplay {result['output_path']}")
            elif platform.system() == "Windows":
                print("\nTo play the audio, run:")
                print(f"  start {result['output_path']}")
        except Exception as e:
            logger.warning(f"Could not provide playback command: {e}")
        
        return 0
    
    except Exception as e:
        logger.exception(f"Error generating audio: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 