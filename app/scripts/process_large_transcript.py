#!/usr/bin/env python3
"""
Process Large Transcript

This script handles very large transcripts by breaking them into chunks,
creating a master document that outlines the content, and then processing
each chunk while maintaining continuity between them.

Usage:
    python process_large_transcript.py --transcript-file=<path> [--output-file=<path>] [--chunk-size=<size>] [--clean-transcript]

Example:
    python process_large_transcript.py --transcript-file=data/transcripts/long_video/raw/transcript.txt --output-file=data/transcripts/long_video/processed/narrative_transcript.txt --chunk-size=20000 --clean-transcript

The script requires the GOOGLE_API_KEY environment variable to be set for Gemini API access.
"""

import os
import json
import time
import argparse
import logging
import sys
import re  # Add missing import for regex operations
from datetime import datetime
import google.generativeai as genai
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('large_transcript_processor.log')
    ]
)

logger = logging.getLogger(__name__)

# Try to import the transcript cleaner utility
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.utils.transcript_cleaner import clean_transcript_file
    CLEANER_AVAILABLE = True
except ImportError:
    logger.warning("Transcript cleaner utility not available. Will not clean transcripts.")
    CLEANER_AVAILABLE = False

# Master document generation prompt
MASTER_DOCUMENT_PROMPT = """
You are a specialized analyzer of long transcripts. Your task is to create a master document that outlines the topics and subjects discussed in a very long transcript based on character positions.

TASK DESCRIPTION:
Analyze the given transcript and create a structured outline of topics and subjects discussed, organized by character positions. This will serve as a guide for processing the transcript in chunks.

INPUT FORMAT:
A complete transcript that may be several hours long (up to 3 million characters).

OUTPUT GUIDELINES:

Content Analysis:
<analyze>
- Identify the main topics and subjects discussed throughout the transcript
- Note the approximate character positions where topics begin and end
- Create logical segments that can be processed separately while maintaining overall flow
</analyze>

Organization:
<organize>
- Divide the transcript into approximately {num_chunks} sections based on character positions
- For each section, provide:
  1. Character range (e.g., "Characters 0-25,000")
  2. Main topics and subjects covered in that range
  3. Brief description of the content
- Ensure sections have logical breakpoints to maintain narrative flow when processed separately
</organize>

Style:
<style>
- Keep the document concise but detailed enough to guide processing
- Use clear section headers with character positions
- Provide enough context for each section to ensure continuity
</style>

OUTPUT FORMAT:
Create a structured document with clearly labeled sections based on character positions. Include an introduction explaining the overall content of the transcript and a conclusion summarizing the key themes.

EXAMPLE FORMAT:
```
# Master Document: [Title Based on Transcript Content]

## Overview
[Brief overview of the entire transcript content]

## Section 1: Characters 0-25,000
- Main topics: [List topics]
- Summary: [Brief summary of this section]
- Key points: [Important points to maintain]

## Section 2: Characters 25,001-50,000
- Main topics: [List topics]
- Summary: [Brief summary of this section]
- Key points: [Important points to maintain]

[... continue for all sections ...]

## Conclusion
[Brief note on ensuring continuity across all sections]
```
"""

# Chunk processing prompt
CHUNK_PROCESSING_PROMPT = """
You are a specialized transcript processor tasked with transforming a portion of a long transcript into a more engaging, well-structured narrative while maintaining the core content and educational value.

TASK DESCRIPTION:
Your task is to process a chunk of a transcript (chunk {chunk_num} of {total_chunks}) to make it more engaging while preserving the core content and educational value. This chunk will be combined with other processed chunks to create a complete narrative.

CONTEXT AND CONTINUITY:
{continuity_context}

INPUT FORMAT:
A segment from a longer transcript, approximately {chunk_size} characters in length.

OUTPUT GUIDELINES:

Content Preservation:
<preserve>
- All key facts, data points, statistics, and educational content
- The overall argument or narrative arc within this chunk
- All major examples, case studies, and illustrations
- Technical accuracy of all explanations
- The relative time/emphasis given to each subtopic
</preserve>

Style Transformation:
<transform>
- Convert lecture-style explanations into storytelling narratives
- Replace academic language with more conversational phrasing
- Improve transitions between topics for smoother flow
- Reduce redundancies and speech disfluencies
- Enhance clarity while maintaining all original information
- Use proper punctuation including periods (.) and commas (,) for natural speech rhythm
- Ensure proper pacing for text-to-speech models by including appropriate punctuation
</transform>

Length Requirements:
<length>
- Your output should be approximately the same length as the input (within 20% variance)
- Input length: {input_length} characters
- Target output length: {target_length_min} to {target_length_max} characters
- IMPORTANT: Aim for the HIGHER end of the target range (closer to {target_length_max} characters)
- Expand on the content while maintaining accuracy to reach the target length
- If your output is too long, focus on conciseness while preserving key information
</length>

Continuity with Other Chunks:
<continuity>
- Ensure smooth transitions with previous and subsequent chunks
- Maintain consistent style, tone, and terminology across chunks
- Do not repeat information that was covered in previous chunks
- Ensure your chunk flows naturally from the previous processed content
</continuity>

IMPORTANT RULES:
- Do NOT add new factual information that wasn't in the original chunk
- Do NOT remove any substantive content from the original
- Do NOT change the meaning of any technical explanations
- Do NOT contradict any statements from the original transcript
- Your output MUST be within the target length range, preferably toward the UPPER end
- Ensure smooth flow with previous content if not the first chunk
- ALWAYS remove any [Music] tags or similar audio markers from the output
- ALWAYS include proper punctuation (periods, commas) for natural speech rhythm in text-to-speech models

OUTPUT FORMAT:
Provide a cohesive, flowing transcript segment that reads like a well-crafted narrative while teaching the exact same content. Use proper punctuation throughout to ensure good pacing and natural rhythm when read by text-to-speech models.

EXAMPLE:

INPUT EXAMPLE:
the land of Britain was once considered
a myth by the mighty Roman Empire
to them it was nothing more than an old
Legend This would change in the year 55
BC when Julius Caesar set his sights on
this fabled island and sailed towards
its Shores the historical Discovery
would end in defeat
[Music]
almost a century later the Romans Found
Glory when Roman Emperor Claudius
stepped foot on British soil they set
their eyes on Stonehenge using the
sacred site for their worship and
rituals londinium was established
and the Romans seized control of the
land but what happened next in the
history of the United Kingdom
to understand this fascinating land we
must start from the very beginning
[Music]
what would become the United Kingdom
began way back within the prehistoric
Paleolithic period which dates back to
950
000 years ago a time that the earliest

OUTPUT EXAMPLE:
The land of Britain was once considered a myth by the mighty Roman Empire. To them, it was nothing more than an old legend, a distant whisper on the winds of time. This would change dramatically in the year 55 BC, when Julius Caesar set his sights on this fabled island and sailed towards its shores. The historical discovery, however, would end in defeat for the ambitious general.

Almost a century later, the Romans finally found glory when Roman Emperor Claudius stepped foot on British soil. They set their eyes on Stonehenge, using the sacred site for their worship and rituals. Londinium was established, and the Romans seized control of the land. But what happened next in the rich tapestry of the United Kingdom's history?

To understand this fascinating land, we must start from the very beginning. What would become the United Kingdom began way back within the prehistoric Paleolithic period, which dates back to an astonishing 950,000 years ago, a time when the earliest human ancestors first walked upon British soil.
"""

def create_master_document(
    transcript: str,
    chunk_size: int = 25000,
    model: str = "models/gemini-2.0-flash-lite"
) -> str:
    """
    Creates a master document that outlines the topics in the transcript by character positions.
    
    Args:
        transcript: The complete transcript text
        chunk_size: Approximate size of each chunk in characters
        model: Gemini model to use
        
    Returns:
        The master document as a string
    """
    logger.info(f"Creating master document for transcript of {len(transcript)} characters")
    
    # Calculate approximate number of chunks
    num_chunks = (len(transcript) + chunk_size - 1) // chunk_size
    logger.info(f"Transcript will be divided into approximately {num_chunks} chunks")
    
    # Prepare the prompt
    prompt = MASTER_DOCUMENT_PROMPT.format(num_chunks=num_chunks)
    
    # Initialize the model
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")
    
    genai.configure(api_key=api_key)
    gen_model = genai.GenerativeModel(model)
    
    # Generate the master document
    try:
        logger.info("Generating master document")
        response = gen_model.generate_content(
            f"{prompt}\n\nTRANSCRIPT TO ANALYZE:\n\n{transcript}",
            generation_config={
                "max_output_tokens": 4096,
                "temperature": 0.2  # Lower temperature for more deterministic output
            }
        )
        
        master_doc = response.text
        logger.info(f"Master document generated ({len(master_doc)} characters)")
        return master_doc
        
    except Exception as e:
        logger.error(f"Error generating master document: {str(e)}")
        raise

def process_transcript_chunk(
    chunk: str,
    master_doc: str,
    chunk_num: int,
    total_chunks: int,
    previous_output: Optional[str] = None,
    model: str = "models/gemini-2.0-flash-lite",
    max_retries: int = 3
) -> str:
    """
    Processes a single chunk of the transcript with awareness of previous chunks.
    
    Args:
        chunk: The transcript chunk to process
        master_doc: The master document outlining topics
        chunk_num: Current chunk number (1-based)
        total_chunks: Total number of chunks
        previous_output: Output from the previous chunk (if any)
        model: Gemini model to use
        max_retries: Maximum number of retries for length validation
        
    Returns:
        Processed chunk text
    """
    logger.info(f"Processing chunk {chunk_num}/{total_chunks} ({len(chunk)} characters)")
    
    # Initialize the model
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")
    
    genai.configure(api_key=api_key)
    gen_model = genai.GenerativeModel(model)
    
    # Prepare continuity context based on chunk position
    if chunk_num == 1:
        continuity_context = """
        This is the FIRST chunk of the transcript. Your output will be the beginning of the processed transcript.
        - Start with an engaging introduction
        - Set the tone and style for the entire narrative
        - Ensure your ending allows smooth continuation to the next chunk
        """
    else:
        continuity_context = f"""
        This is chunk {chunk_num} of {total_chunks}. 
        - Your output must continue seamlessly from the previous processed chunk
        - Do NOT repeat information already covered in previous chunks
        - Reference the master document to understand how this chunk fits in the overall narrative
        - The previous processed chunk ends with:
        
        ```
        {previous_output[-500:] if previous_output else "No previous output available"}
        ```
        
        Your output should continue directly from this point, maintaining the style, tone, and flow.
        """
    
    # Calculate target length range (within 20% of input length instead of 10%)
    input_length = len(chunk)
    target_length_min = max(int(input_length * 0.8), 1000)  # 20% lower bound
    target_length_max = int(input_length * 1.2)  # 20% upper bound
    # Calculate a preferred target slightly above the minimum (around 90-95% of input)
    preferred_target = int(input_length * 0.95)
    
    # Add detailed logging for target lengths
    logger.info(f"Target length range for chunk {chunk_num}: {target_length_min} to {target_length_max} characters (80%-120% of input)")
    logger.info(f"Preferred target length: {preferred_target} characters (95% of input)")
    
    # Prepare the prompt
    prompt = CHUNK_PROCESSING_PROMPT.format(
        chunk_num=chunk_num,
        total_chunks=total_chunks,
        chunk_size=len(chunk),
        continuity_context=continuity_context,
        input_length=input_length,
        target_length_min=target_length_min,
        target_length_max=target_length_max
    )
    
    # Process with retries for length validation
    retry_count = 0
    while retry_count <= max_retries:
        try:
            logger.info(f"Generating content for chunk {chunk_num} (attempt {retry_count + 1}/{max_retries + 1})")
            
            # Prepare the full context
            full_prompt = f"{prompt}\n\nMASTER DOCUMENT:\n\n{master_doc}\n\n"
            if previous_output and chunk_num > 1:
                full_prompt += f"PREVIOUS PROCESSED CHUNK:\n\n{previous_output}\n\n"
            full_prompt += f"CHUNK TO PROCESS:\n\n{chunk}"
            
            # Generate content
            response = gen_model.generate_content(
                full_prompt,
                generation_config={
                    "max_output_tokens": 4096,
                    "temperature": 0.7
                }
            )
            
            processed_chunk = response.text
            processed_length = len(processed_chunk)
            logger.info(f"Generated content for chunk {chunk_num} ({processed_length} characters)")
            
            # Validate length with more detailed logging
            if processed_length < target_length_min:
                percentage = (processed_length / input_length) * 100
                logger.warning(f"Processed chunk {chunk_num} is too short: {processed_length} characters ({percentage:.1f}% of input). Minimum target: {target_length_min} (80%).")
                
                # Additional check to accept if very close to the 80% threshold (within 0.5%)
                if processed_length >= (target_length_min - 100):
                    logger.info(f"Output is very close to the 80% threshold, accepting it as valid: {processed_length} vs {target_length_min}")
                    percentage = (processed_length / input_length) * 100
                    logger.info(f"Processed chunk length is acceptable: {processed_length} characters ({percentage:.1f}% of input)")
                    return processed_chunk
                
                if retry_count < max_retries:
                    logger.warning(f"Retrying with emphasis on length (attempt {retry_count + 2}/{max_retries + 1}).")
                    prompt += f"\n\nIMPORTANT: Your previous response was too short ({processed_length} characters, {percentage:.1f}% of input). Please ensure your output is AT LEAST {target_length_min} characters (80% of input) but preferably closer to {preferred_target} characters (95% of input) while maintaining quality and accuracy. ADD MORE DETAIL to reach the target length."
                    retry_count += 1
                    continue
                else:
                    logger.warning(f"Max retries reached. Proceeding with chunk that is {percentage:.1f}% of target length.")
            else:
                percentage = (processed_length / input_length) * 100
                logger.info(f"Processed chunk length is acceptable: {processed_length} characters ({percentage:.1f}% of input)")
            
            return processed_chunk
            
        except Exception as e:
            retry_count += 1
            if retry_count > max_retries:
                logger.error(f"Failed to process chunk {chunk_num} after {max_retries} retries: {str(e)}")
                raise
            logger.warning(f"Error processing chunk {chunk_num}: {str(e)}. Retrying ({retry_count}/{max_retries}).")
            time.sleep(2 ** retry_count)  # Exponential backoff
    
    raise RuntimeError(f"Failed to process chunk {chunk_num} after {max_retries} retries")

def split_transcript_into_chunks(transcript: str, chunk_size: int = 25000) -> List[str]:
    """
    Splits the transcript into chunks of approximately equal size.
    
    Args:
        transcript: The complete transcript text
        chunk_size: Target size of each chunk in characters
        
    Returns:
        List of transcript chunks
    """
    logger.info(f"Splitting transcript of {len(transcript)} characters into chunks of ~{chunk_size} characters")
    
    # If transcript is shorter than chunk size, return it as a single chunk
    if len(transcript) <= chunk_size:
        return [transcript]
    
    chunks = []
    remaining_text = transcript
    
    while remaining_text:
        # If remaining text is shorter than chunk_size, add it as the final chunk
        if len(remaining_text) <= chunk_size:
            chunks.append(remaining_text)
            break
        
        # Find a good breakpoint (end of paragraph or sentence) near the chunk_size
        # First try to find a paragraph break near the target length
        breakpoint = chunk_size
        
        # Look for paragraph breaks (double newlines) within a window around the target size
        search_window = 1000  # Look 1000 chars before and after the target size
        search_start = max(0, breakpoint - search_window)
        search_end = min(len(remaining_text), breakpoint + search_window)
        search_text = remaining_text[search_start:search_end]
        
        # Look for paragraph breaks
        paragraph_breaks = [search_start + m.start() for m in re.finditer(r'\n\s*\n', search_text)]
        
        # If found paragraph breaks, use the closest one to the target
        if paragraph_breaks:
            closest_break = min(paragraph_breaks, key=lambda x: abs(x - breakpoint))
            breakpoint = closest_break + 2  # +2 to include the newlines
        else:
            # No paragraph breaks found, look for sentence endings
            sentence_breaks = [search_start + m.start() for m in re.finditer(r'[.!?]\s+', search_text)]
            if sentence_breaks:
                closest_break = min(sentence_breaks, key=lambda x: abs(x - breakpoint))
                breakpoint = closest_break + 1  # +1 to include the punctuation
        
        # Add the chunk and update remaining text
        chunks.append(remaining_text[:breakpoint])
        remaining_text = remaining_text[breakpoint:]
    
    logger.info(f"Split transcript into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        logger.info(f"Chunk {i+1}: {len(chunk)} characters")
    
    return chunks

def process_large_transcript(
    transcript_file: str,
    output_file: Optional[str] = None,
    chunk_size: int = 20000,
    model: str = "models/gemini-2.0-flash-lite",
    clean_transcript: bool = False,
    markers_to_clean: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Process a large transcript by breaking it into chunks and processing each chunk.
    
    Args:
        transcript_file: Path to the transcript file
        output_file: Path to save the processed transcript
        chunk_size: Size of each chunk in characters
        model: Model to use for processing
        clean_transcript: Whether to clean the transcript by removing markers
        markers_to_clean: List of markers to remove, defaults to ['[Music]']
        
    Returns:
        Dict with metadata about the processing
    """
    if markers_to_clean is None:
        markers_to_clean = ['[Music]']
        
    # Determine output file if not provided
    if output_file is None:
        transcript_path = Path(transcript_file)
        parent_dir = transcript_path.parent.parent
        output_dir = parent_dir / "processed"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / "narrative_transcript.txt")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Read the transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript = f.read()
    
    logger.info(f"Processing transcript of length: {len(transcript)} characters")
    
    # Generate the master document
    start_time = time.time()
    master_doc = create_master_document(transcript, chunk_size, model)
    master_doc_time = time.time() - start_time
    
    # Save the master document
    master_doc_file = output_file.replace('.txt', '_master.txt')
    with open(master_doc_file, 'w', encoding='utf-8') as f:
        f.write(master_doc)
    
    logger.info(f"Master document generated in {master_doc_time:.2f} seconds")
    logger.info(f"Master document saved to: {master_doc_file}")
    logger.info(f"Master document length: {len(master_doc)} characters")
    
    # Split the transcript into chunks


    chunks = split_transcript_into_chunks(transcript, chunk_size)
    
    logger.info(f"Transcript split into {len(chunks)} chunks")
    
    # Process each chunk
    processed_chunks = []
    chunk_times = []
    chunk_sizes = []
    output_sizes = []
    
    previous_output = None
    for i, chunk in enumerate(chunks):
        #print 200 chars of chunk
        logger.info(f"Chunk {i+1} first 200 chars: {chunk[:200]}")
        chunk_start_time = time.time()
        logger.info(f"Processing chunk {i+1}/{len(chunks)}")
        logger.info(f"Chunk {i+1} size: {len(chunk)} characters")
        
        # Save chunk to file for debugging
        chunk_file = output_file.replace('.txt', f'_chunk{i+1}.txt')
        
        # Process the chunk
        processed_chunk = process_transcript_chunk(
            chunk,
            master_doc,
            i+1,
            len(chunks),
            previous_output,
            model
        )
        
        # Save processed chunk
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(processed_chunk)
        
        processed_chunks.append(processed_chunk)
        previous_output = processed_chunk
        
        chunk_time = time.time() - chunk_start_time
        chunk_times.append(chunk_time)
        chunk_sizes.append(len(chunk))
        output_sizes.append(len(processed_chunk))
        
        logger.info(f"Chunk {i+1} processed in {chunk_time:.2f} seconds")
        logger.info(f"Chunk {i+1} output length: {len(processed_chunk)} characters")
        logger.info(f"Chunk {i+1} saved to: {chunk_file}")
    
    # Concatenate the processed chunks
    processed_transcript = '\n'.join(processed_chunks)
    
    # Write the processed transcript to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_transcript)
    
    total_time = time.time() - start_time
    
    logger.info(f"Transcript processing completed in {total_time:.2f} seconds")
    logger.info(f"Processed transcript saved to: {output_file}")
    logger.info(f"Original length: {len(transcript)} characters")
    logger.info(f"Processed length: {len(processed_transcript)} characters")
    
    # Clean the transcript if requested
    if clean_transcript and CLEANER_AVAILABLE:
        logger.info(f"Cleaning transcript by removing markers: {markers_to_clean}")
        
        # Clean the full processed transcript
        cleaned_file, clean_stats = clean_transcript_file(
            output_file,
            markers=markers_to_clean,
            preserve_original=False  # Replace the original
        )
        
        logger.info(f"Transcript cleaned: removed {clean_stats['total_markers_removed']} markers")
        logger.info(f"Cleaned transcript length: {clean_stats['cleaned_length']} characters")
        
        # Update the processed transcript length in our stats
        processed_length = clean_stats['cleaned_length']
    else:
        processed_length = len(processed_transcript)
        if clean_transcript and not CLEANER_AVAILABLE:
            logger.warning("Transcript cleaner utility not available. Transcript not cleaned.")
    
    # Create metadata
    metadata = {
        "original_length": len(transcript),
        "processed_length": processed_length,
        "processing_time_seconds": total_time,
        "num_chunks": len(chunks),
        "chunk_sizes": chunk_sizes,
        "output_sizes": output_sizes,
        "chunk_times": [round(t, 2) for t in chunk_times],
        "model": model
    }
    
    # Save metadata
    metadata_file = output_file.replace('.txt', '_metadata.json')
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Metadata saved to: {metadata_file}")
    
    return metadata

def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(description="Process large transcript by chunking")
    parser.add_argument("--transcript-file", required=True, help="Path to the transcript file")
    parser.add_argument("--output-file", help="Path to save the processed transcript")
    parser.add_argument("--chunk-size", type=int, default=20000, help="Size of each chunk in characters")
    parser.add_argument("--model", default="models/gemini-2.0-flash-lite", help="Model to use for processing")
    parser.add_argument("--clean-transcript", action="store_true", help="Clean the transcript by removing markers like [Music]")
    parser.add_argument("--markers", default="[Music]", help="Comma-separated list of markers to remove (default: [Music])")
    
    args = parser.parse_args()
    
    # Check if GOOGLE_API_KEY is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable not set")
        sys.exit(1)
    
    # Configure genai with the API key
    genai.configure(api_key=api_key)
    
    # Split markers string into list
    markers_to_clean = [marker.strip() for marker in args.markers.split(',')]
    
    # Process the transcript
    process_large_transcript(
        args.transcript_file,
        args.output_file,
        args.chunk_size,
        args.model,
        args.clean_transcript,
        markers_to_clean
    )

if __name__ == "__main__":
    main() 