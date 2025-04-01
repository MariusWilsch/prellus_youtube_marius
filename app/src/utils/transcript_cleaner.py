"""
Transcript cleaner utility module.

This module provides functions to clean transcripts by removing non-verbal markers
like [Music] and other similar markers.
"""

import os
import re
import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_transcript_text(content, markers=None):
    """
    Clean transcript text by removing specified markers.
    
    Args:
        content (str): Transcript content to clean
        markers (list, optional): List of markers to remove, defaults to ['[Music]']
        
    Returns:
        tuple: (cleaned_content, stats) where stats is a dict with cleaning statistics
    """
    if markers is None:
        markers = ['[Music]']
    
    original_length = len(content)
    
    # Count occurrences of each marker
    marker_counts = {}
    for marker in markers:
        marker_counts[marker] = content.count(marker)
    
    # Create a pattern that matches any of the markers
    pattern = '|'.join(re.escape(marker) for marker in markers)
    
    # Remove all instances of the markers (including any surrounding whitespace)
    cleaned_content = re.sub(f"\\s*({pattern})\\s*", " ", content)
    
    # Remove any double spaces that might have been created
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
    
    cleaned_length = len(cleaned_content)
    
    stats = {
        "original_length": original_length,
        "cleaned_length": cleaned_length,
        "characters_removed": original_length - cleaned_length,
        "markers_removed": marker_counts,
        "total_markers_removed": sum(marker_counts.values())
    }
    
    return cleaned_content, stats

def clean_transcript_file(input_file, output_file=None, markers=None, preserve_original=False):
    """
    Clean a transcript file by removing specified markers.
    
    Args:
        input_file (str): Path to the input transcript file
        output_file (str, optional): Path to save the cleaned transcript
        markers (list, optional): List of markers to remove
        preserve_original (bool): Whether to preserve the original file
        
    Returns:
        tuple: (output_file_path, stats) where stats is a dict with cleaning statistics
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
        
        # Clean the content
        cleaned_content, stats = clean_transcript_text(content, markers)
        
        logger.info(f"Original transcript length: {stats['original_length']} characters")
        logger.info(f"Cleaned transcript length: {stats['cleaned_length']} characters")
        logger.info(f"Removed {stats['characters_removed']} characters")
        logger.info(f"Removed {stats['total_markers_removed']} markers: {stats['markers_removed']}")
        
        # Write the cleaned content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        logger.info(f"Cleaned transcript saved to: {output_file}")
        
        # Create metadata file
        metadata = {
            "original_file": input_file,
            "cleaned_file": output_file,
            **stats,
            "timestamp": datetime.now().isoformat()
        }
        
        metadata_file = f"{output_file}.metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Metadata saved to: {metadata_file}")
        
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
                
                return input_file, stats
        
        return output_file, stats
    
    except Exception as e:
        logger.error(f"Error cleaning transcript: {str(e)}")
        raise

def clean_directory(directory, markers=None, recursive=False, preserve_original=True):
    """
    Clean all transcript files in a directory.
    
    Args:
        directory (str): Path to the directory
        markers (list, optional): List of markers to remove
        recursive (bool): Whether to process subdirectories
        preserve_original (bool): Whether to preserve original files
        
    Returns:
        list: List of tuples (cleaned_file_path, stats) for each processed file
    """
    if markers is None:
        markers = ['[Music]']
    
    directory_path = Path(directory)
    results = []
    
    # Find all .txt files in the directory
    glob_pattern = '**/*.txt' if recursive else '*.txt'
    transcript_files = list(directory_path.glob(glob_pattern))
    
    logger.info(f"Found {len(transcript_files)} transcript files in {directory}")
    
    for transcript_file in transcript_files:
        # Skip files that already have "_cleaned" in their name
        if "_cleaned" in transcript_file.name:
            continue
        
        output_file, stats = clean_transcript_file(
            str(transcript_file), 
            markers=markers, 
            preserve_original=preserve_original
        )
        results.append((output_file, stats))
    
    return results 