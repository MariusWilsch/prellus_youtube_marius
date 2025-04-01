#!/usr/bin/env python3
"""
Kokoro TTS Voice Options Test Script

This script generates audio samples using different voice options available in Kokoro TTS.
It helps you compare and choose the best voice for your needs.
"""

import os
import sys
import logging
import subprocess
import tempfile
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Sample text to use for testing voices
SAMPLE_TEXT = """
Hello! This is a sample text to test different voice options in Kokoro TTS.
I'm speaking English to demonstrate how natural and clear the voice sounds.
The quick brown fox jumps over the lazy dog.
"""

# Available voice options to test
VOICE_OPTIONS = [
    # American female voices
    "af_bella",
    "af_nicole",
    "af_sky",
    "af_sarah",
    # American male voices
    "am_adam",
    "am_michael",
    # British female voices
    "bf_emma",
    "bf_isabella",
    # British male voices
    "bm_george",
    "bm_lewis",
]

def generate_voice_sample(voice, output_path):
    """Generate an audio sample using the specified voice."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write(SAMPLE_TEXT)
        temp_file.flush()
        
        cmd = [
            "kokoro",
            "-l", "a",          # American English language
            "-m", voice,        # Voice to use
            "-i", temp_file.name,
            "-o", output_path
        ]
        
        try:
            logger.info(f"Generating sample with voice: {voice}")
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                logger.error(f"Error generating sample for {voice}: {process.stderr}")
                return False
            
            logger.info(f"Successfully generated sample: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Exception while generating sample for {voice}: {str(e)}")
            return False

def main():
    """Main function to generate voice samples."""
    # Create output directory
    output_dir = Path("outputs/voice_samples")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Track successful generations
    successful_voices = []
    
    # Generate a sample for each voice option
    for voice in VOICE_OPTIONS:
        output_path = output_dir / f"{voice}_sample.wav"
        if generate_voice_sample(voice, str(output_path)):
            successful_voices.append((voice, output_path))
    
    # Print summary
    print("\n" + "="*50)
    print("VOICE SAMPLE GENERATION SUMMARY")
    print("="*50)
    
    if successful_voices:
        print(f"Successfully generated {len(successful_voices)} voice samples:")
        for voice, path in successful_voices:
            print(f"  - {voice}: {path}")
        
        # Print playback instructions
        print("\nTo play the samples:")
        for voice, path in successful_voices:
            print(f"  afplay {path}    # Play {voice} sample")
    else:
        print("Failed to generate any voice samples.")
    
    return 0 if successful_voices else 1

if __name__ == "__main__":
    sys.exit(main()) 