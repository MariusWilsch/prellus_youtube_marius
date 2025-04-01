#!/usr/bin/env python3
"""
Script to clean processed transcripts by removing non-verbal markers like [Music].

This script takes a processed transcript file and removes specified markers 
such as [Music], creating a cleaner version for reading or further processing.
"""

import os
import re
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='transcript_cleaner.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('transcript_cleaner')

def setup_argparser():
    """
    Set up and return the argument parser for the script.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(description='Clean transcript by removing non-verbal markers.')
    parser.add_argument('--input-file', required=True, help='Path to the input transcript file')
    parser.add_argument('--output-file', help='Path to save the cleaned transcript (default: original filename with _cleaned suffix)')
    parser.add_argument('--markers', default='[Music]', help='Comma-separated list of markers to remove (default: [Music])')
    parser.add_argument('--preserve-original', action='store_true', help='Whether to preserve the original file')
    return parser

def clean_transcript(input_file, output_file=None, markers=None, preserve_original=False):
    """
    Clean a transcript file by removing specified markers.
    
    Args:
        input_file (str): Path to the input transcript file
        output_file (str, optional): Path to save the cleaned transcript
        markers (list, optional): List of markers to remove
        preserve_original (bool): Whether to preserve the original file
        
    Returns:
        str: Path to the cleaned transcript file
    """
    if markers is None:
        markers = ['[Music]']
    
    # If no output file specified, create one with _cleaned suffix
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}")
    
    logger.info(f"Cleaning transcript: {input_file}")
    logger.info(f"Markers to remove: {markers}")
    
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_length = len(content)
        logger.info(f"Original transcript length: {original_length} characters")
        
        # Create a pattern that matches any of the markers
        pattern = '|'.join(re.escape(marker) for marker in markers)
        
        # Remove all instances of the markers (including any surrounding whitespace)
        cleaned_content = re.sub(f"\\s*({pattern})\\s*", " ", content)
        
        # Remove any double spaces that might have been created
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
        
        cleaned_length = len(cleaned_content)
        logger.info(f"Cleaned transcript length: {cleaned_length} characters")
        logger.info(f"Removed {original_length - cleaned_length} characters")
        
        # Write the cleaned content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        logger.info(f"Cleaned transcript saved to: {output_file}")
        
        # If not preserving the original, replace it with the cleaned version
        if not preserve_original and output_file != input_file:
            if os.path.exists(output_file):
                # Create a backup of the original file
                backup_file = f"{input_file}.bak"
                os.rename(input_file, backup_file)
                logger.info(f"Original file backed up to: {backup_file}")
                
                # Replace the original with the cleaned version
                os.rename(output_file, input_file)
                logger.info(f"Original file replaced with cleaned version")
                
                return input_file
        
        return output_file
    
    except Exception as e:
        logger.error(f"Error cleaning transcript: {str(e)}")
        raise

def create_metadata(input_file, output_file, original_length, cleaned_length, markers_removed):
    """
    Create metadata for the cleaning operation.
    
    Args:
        input_file (str): Path to the input transcript file
        output_file (str): Path to the cleaned transcript file
        original_length (int): Length of the original transcript
        cleaned_length (int): Length of the cleaned transcript
        markers_removed (dict): Dictionary of markers and their count
    """
    metadata = {
        "original_file": input_file,
        "cleaned_file": output_file,
        "original_length": original_length,
        "cleaned_length": cleaned_length,
        "characters_removed": original_length - cleaned_length,
        "markers_removed": markers_removed,
        "timestamp": datetime.now().isoformat()
    }
    
    metadata_file = f"{output_file}.metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Metadata saved to: {metadata_file}")

def clean_directory(directory, markers=None, recursive=False):
    """
    Clean all transcript files in a directory.
    
    Args:
        directory (str): Path to the directory
        markers (list, optional): List of markers to remove
        recursive (bool): Whether to process subdirectories
    """
    if markers is None:
        markers = ['[Music]']
    
    directory_path = Path(directory)
    
    # Find all .txt files in the directory
    glob_pattern = '**/*.txt' if recursive else '*.txt'
    transcript_files = list(directory_path.glob(glob_pattern))
    
    logger.info(f"Found {len(transcript_files)} transcript files in {directory}")
    
    for transcript_file in transcript_files:
        # Skip files that already have "_cleaned" in their name
        if "_cleaned" in transcript_file.name:
            continue
        
        clean_transcript(str(transcript_file), markers=markers, preserve_original=True)

def main():
    """
    Main entry point for the script.
    """
    parser = setup_argparser()
    args = parser.parse_args()
    
    logger.info("Starting transcript cleaning process")
    
    # Convert comma-separated markers to a list
    markers = [marker.strip() for marker in args.markers.split(',')]
    
    # Clean the transcript
    cleaned_file = clean_transcript(
        args.input_file,
        args.output_file,
        markers,
        args.preserve_original
    )
    
    logger.info(f"Transcript cleaning completed: {cleaned_file}")
    print(f"Transcript cleaned and saved to: {cleaned_file}")

if __name__ == "__main__":
    main() 