#!/usr/bin/env python3
"""
Transcript Listing Utility

This script lists all available transcripts in the data directory,
showing information about each transcript including video ID, 
creation date, and file locations.

Usage:
    python scripts/list_transcripts.py [--details]

Options:
    --details  Show detailed information about each transcript
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

def format_timestamp(seconds):
    """Format seconds as mm:ss."""
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def format_size(size_in_bytes):
    """Format file size in a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} TB"

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
        if os.path.exists(os.path.join(item_path, "raw", "transcript.json")):
            transcript_dirs.append(item_path)
    
    return transcript_dirs

def get_transcript_info(transcript_dir, detailed=False):
    """Get information about a transcript."""
    dir_name = os.path.basename(transcript_dir)
    parts = dir_name.split('_')
    
    # Extract video ID (first part)
    video_id = parts[0] if parts else "unknown"
    
    # Try to parse timestamp
    timestamp = parse_timestamp(dir_name)
    fetch_date = timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Unknown"
    
    # Basic info
    info = {
        "video_id": video_id,
        "directory": transcript_dir,
        "fetch_date": fetch_date
    }
    
    # Try to load metadata
    metadata_path = os.path.join(transcript_dir, "metadata.json")
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                info["video_url"] = metadata.get("video_url", f"https://www.youtube.com/watch?v={video_id}")
                
                # Get transcript duration if available
                if "timestamp" in metadata:
                    start = metadata["timestamp"].get("start", 0)
                    end = metadata["timestamp"].get("end", 0)
                    duration = end - start
                    info["duration"] = format_timestamp(duration)
                    info["duration_seconds"] = duration
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Add detailed information if requested
    if detailed:
        # Get transcript files
        raw_json_path = os.path.join(transcript_dir, "raw", "transcript.json")
        raw_txt_path = os.path.join(transcript_dir, "raw", "transcript.txt")
        
        if os.path.exists(raw_json_path):
            info["raw_json"] = raw_json_path
            info["raw_json_size"] = format_size(os.path.getsize(raw_json_path))
        
        if os.path.exists(raw_txt_path):
            info["raw_txt"] = raw_txt_path
            info["raw_txt_size"] = format_size(os.path.getsize(raw_txt_path))
            
            # Count lines and words in text transcript
            try:
                with open(raw_txt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    info["line_count"] = len(content.splitlines())
                    info["word_count"] = len(content.split())
            except FileNotFoundError:
                pass
        
        # Check for processed files
        processed_dir = os.path.join(transcript_dir, "processed")
        if os.path.exists(processed_dir):
            processed_files = [f for f in os.listdir(processed_dir) if os.path.isfile(os.path.join(processed_dir, f))]
            if processed_files:
                info["processed_files"] = processed_files
        
        # Check for audio files
        audio_dir = os.path.join(transcript_dir, "audio")
        if os.path.exists(audio_dir):
            audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]
            if audio_files:
                info["audio_files"] = audio_files
    
    return info

def display_transcript_info(info, detailed=False):
    """Display transcript information."""
    print(f"\n{'-'*80}")
    print(f"Video ID: {info['video_id']}")
    print(f"Video URL: {info.get('video_url', 'Unknown')}")
    print(f"Fetched: {info['fetch_date']}")
    if "duration" in info:
        print(f"Duration: {info['duration']}")
    
    if detailed:
        print(f"\nDirectory: {info['directory']}")
        
        if "raw_json" in info:
            print(f"Raw JSON: {info['raw_json']} ({info['raw_json_size']})")
        
        if "raw_txt" in info:
            print(f"Plain text: {info['raw_txt']} ({info['raw_txt_size']})")
            if "line_count" in info and "word_count" in info:
                print(f"  - {info['line_count']} lines, {info['word_count']} words")
        
        if "processed_files" in info:
            print("\nProcessed files:")
            for file in info["processed_files"]:
                print(f"  - {file}")
        
        if "audio_files" in info:
            print("\nAudio files:")
            for file in info["audio_files"]:
                print(f"  - {file}")
    
    print(f"{'-'*80}")

def main():
    """Main function to list available transcripts."""
    parser = argparse.ArgumentParser(description="List available transcripts")
    parser.add_argument("--details", action="store_true", help="Show detailed information")
    args = parser.parse_args()
    
    transcript_dirs = get_transcript_dirs()
    
    if not transcript_dirs:
        print("No transcripts found in data/transcripts directory.")
        return 1
    
    # Sort by timestamp (newest first)
    transcript_dirs.sort(key=lambda x: parse_timestamp(os.path.basename(x)) or datetime.min, reverse=True)
    
    print(f"Found {len(transcript_dirs)} transcript(s):")
    
    for dir_path in transcript_dirs:
        info = get_transcript_info(dir_path, detailed=args.details)
        display_transcript_info(info, detailed=args.details)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 