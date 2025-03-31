#!/usr/bin/env python3
"""
Test script for Kokoro TTS implementation

This script tests the Kokoro TTS implementation by generating audio from the
test_tss.txt file. It directly uses the TTSGenerator class to convert the text
to speech and saves the output to an audio file.
"""

import os
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import the TTSGenerator class
from src.transcript_pipeline.tts.tts_generator import TTSGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def main():
    """
    Main function to test Kokoro TTS with test_tss.txt
    """
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent
    
    # Path to test file
    test_file_path = project_root / "test_tss.txt"
    
    # Output directory for audio files
    output_dir = project_root / "outputs" / "test_audio"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output audio file path
    output_path = output_dir / "test_tss_output.wav"
    
    print(f"Reading test text from: {test_file_path}")
    
    # Read test text
    with open(test_file_path, 'r', encoding='utf-8') as f:
        test_text = f.read()
    
    print(f"Test text length: {len(test_text)} characters")
    
    # Configure TTS
    config = {
        "language": "en-US",       # American English language code
        "voice_pack": "af_bella", # American female voice
        "speed": 1.0,
        "max_chunk_length": 500,
        "pause_between_chunks": 0.5
    }
    
    print(f"Initializing TTSGenerator with language: {config['language']} (American English), voice: {config['voice_pack']}")
    
    # Initialize TTSGenerator
    tts_generator = TTSGenerator(config)
    
    # Generate audio
    print(f"Generating audio from test text...")
    try:
        result = tts_generator.generate_audio(test_text, str(output_path))
        
        print("\nAudio generation completed successfully!")
        print(f"Output file: {output_path}")
        print(f"Audio duration: {result['audio_duration_seconds']:.2f} seconds")
        print(f"Processing time: {result['processing_time_seconds']:.2f} seconds")
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 