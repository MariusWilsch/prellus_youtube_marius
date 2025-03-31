#!/usr/bin/env python3
"""
Transcript Search Utility

This script allows searching within transcript text files for specific
keywords or phrases, displaying matching lines with context.

Usage:
    python scripts/search_transcripts.py <search_term> [--case-sensitive] [--context LINES]

Options:
    --case-sensitive    Perform case-sensitive search (default: case-insensitive)
    --context LINES     Number of context lines to display before and after match (default: 1)
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

def format_timestamp(seconds):
    """Format seconds as mm:ss."""
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def parse_timestamp(timestamp_str):
    """Parse timestamp from directory name."""
    try:
        # Try to find the part that looks like a timestamp (YYYYMMDD_HHMMSS)
        parts = timestamp_str.split('_')
        if len(parts) < 2:
            return None
            
        # Check for the format we expect in our directory names
        date_part = None
        time_part = None
        
        # Look for a part that matches YYYYMMDD format (8 digits)
        for i, part in enumerate(parts):
            if part.isdigit() and len(part) == 8 and i+1 < len(parts):
                date_part = part
                time_part = parts[i+1]
                break
        
        if not date_part or not time_part:
            return None
            
        # Parse date part (YYYYMMDD)
        year = int(date_part[:4])
        month = int(date_part[4:6])
        day = int(date_part[6:8])
        
        # Parse time part (HHMMSS)
        hour = int(time_part[:2]) if len(time_part) >= 2 else 0
        minute = int(time_part[2:4]) if len(time_part) >= 4 else 0
        second = int(time_part[4:6]) if len(time_part) >= 6 else 0
        
        return datetime(year, month, day, hour, minute, second)
    except (ValueError, IndexError):
        return None

def get_transcript_dirs():
    """Get all transcript directories."""
    base_dir = os.path.join(project_root, "data", "transcripts")
    if not os.path.exists(base_dir):
        return []
    
    transcript_dirs = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if not os.path.isdir(item_path) or item.startswith('.'):
            continue
        
        # Check if this is a valid transcript directory
        if os.path.exists(os.path.join(item_path, "raw", "transcript.txt")):
            transcript_dirs.append(item_path)
    
    return transcript_dirs

def extract_video_id(dir_name):
    """Extract video ID from directory name."""
    parts = dir_name.split('_')
    return parts[0] if parts else "unknown"

def search_transcript(transcript_path, search_term, case_sensitive=False, context_lines=1):
    """
    Search within a transcript file for the specified term.
    
    Args:
        transcript_path: Path to the transcript text file
        search_term: String or regex pattern to search for
        case_sensitive: Whether the search should be case-sensitive
        context_lines: Number of context lines to display before and after match
        
    Returns:
        List of tuples containing (line_number, line_content, is_match)
    """
    if not os.path.exists(transcript_path):
        return []
    
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(re.escape(search_term), flags)
    
    # Read the entire transcript file
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find matching lines
    matches = []
    for i, line in enumerate(lines):
        if pattern.search(line):
            # Add context lines before the match
            start_idx = max(0, i - context_lines)
            for j in range(start_idx, i):
                matches.append((j + 1, lines[j], False))
            
            # Add the match
            matches.append((i + 1, line, True))
            
            # Add context lines after the match
            end_idx = min(len(lines), i + context_lines + 1)
            for j in range(i + 1, end_idx):
                matches.append((j + 1, lines[j], False))
            
            # Add a separator if we're not at the end
            if i + context_lines + 1 < len(lines):
                matches.append((-1, "", False))
    
    return matches

def display_search_results(transcript_dir, matches, search_term):
    """Display search results for a transcript."""
    if not matches:
        return
    
    dir_name = os.path.basename(transcript_dir)
    video_id = extract_video_id(dir_name)
    
    # Try to get video URL from metadata
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    metadata_path = os.path.join(transcript_dir, "metadata.json")
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                video_url = metadata.get("video_url", video_url)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Parse timestamp
    timestamp = parse_timestamp(dir_name)
    fetch_date = timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Unknown"
    
    # Print header
    print(f"\n{'-'*80}")
    print(f"Video ID: {video_id}")
    print(f"Video URL: {video_url}")
    print(f"Fetched: {fetch_date}")
    print(f"Search term: '{search_term}'")
    print(f"Matches: {len([m for m in matches if m[0] > 0 and m[2]])}")
    print(f"{'-'*80}")
    
    # Print matches with context
    current_group = -1
    for line_num, line, is_match in matches:
        if line_num == -1:
            # This is a separator
            print(f"{'.'*40}")
            current_group = -1
            continue
        
        if current_group != line_num // 100:
            current_group = line_num // 100
        
        # Format the line (highlight match if it's a match line)
        if is_match:
            # Print the line number with highlighting
            print(f"\033[1;33m{line_num:4d}:\033[0m {line.rstrip()}")
        else:
            # Context line
            print(f"{line_num:4d}: {line.rstrip()}")
    
    print(f"{'-'*80}")

def main():
    """Main function to search transcripts."""
    parser = argparse.ArgumentParser(description="Search within transcript text")
    parser.add_argument("search_term", help="Term or phrase to search for")
    parser.add_argument("--case-sensitive", action="store_true", help="Perform case-sensitive search")
    parser.add_argument("--context", type=int, default=1, help="Number of context lines to display (default: 1)")
    args = parser.parse_args()
    
    transcript_dirs = get_transcript_dirs()
    
    if not transcript_dirs:
        print("No transcripts found in data/transcripts directory.")
        return 1
    
    # Sort by timestamp (newest first)
    transcript_dirs.sort(key=lambda x: parse_timestamp(os.path.basename(x)) or datetime.min, reverse=True)
    
    search_term = args.search_term
    found_matches = False
    
    for dir_path in transcript_dirs:
        transcript_path = os.path.join(dir_path, "raw", "transcript.txt")
        if not os.path.exists(transcript_path):
            continue
        
        matches = search_transcript(
            transcript_path, 
            search_term, 
            case_sensitive=args.case_sensitive,
            context_lines=args.context
        )
        
        if matches:
            found_matches = True
            display_search_results(dir_path, matches, search_term)
    
    if not found_matches:
        print(f"No matches found for '{search_term}' in any transcripts.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 