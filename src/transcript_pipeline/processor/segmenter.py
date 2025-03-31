"""
Transcript Segmenter Module

This module provides functionality to segment large transcripts into manageable chunks
for processing. It attempts to split transcripts at natural boundaries such as
paragraph breaks, speaker changes, or topic transitions.
"""

import os
import re
import json
import logging
import time
from typing import Dict, Any, List, Tuple, Optional
import math

logger = logging.getLogger(__name__)

class TranscriptSegmenter:
    """
    Segments large transcripts into smaller chunks for easier processing.
    
    This class provides methods to split large transcript texts into manageable segments
    based on natural boundaries in the text, such as paragraph breaks, speaker changes,
    or topical shifts.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the transcript segmenter with configuration parameters.
        
        Args:
            config: Configuration parameters for the segmenter
        """
        self.config = config or {}
        
        # Set default configuration values if not provided
        self.target_segment_size = self.config.get("target_segment_size", 20000)
        self.min_segment_size = self.config.get("min_segment_size", 17000)
        self.max_segment_size = self.config.get("max_segment_size", 23000)
        self.overlap_size = self.config.get("overlap_size", 1000)
        
        # Boundary preferences (higher number = stronger preference for splitting here)
        self.boundary_weights = {
            "speaker_change": self.config.get("speaker_change_weight", 5),
            "paragraph_break": self.config.get("paragraph_break_weight", 3),
            "sentence_break": self.config.get("sentence_break_weight", 2),
            "topic_change": self.config.get("topic_change_weight", 4)
        }
        
        logger.info(f"Initialized TranscriptSegmenter with target size {self.target_segment_size} characters")
    
    def segment_transcript(self, transcript_text: str) -> List[str]:
        """
        Segment a transcript into manageable chunks.
        
        Args:
            transcript_text: The full transcript text to segment
            
        Returns:
            A list of segment strings
        """
        logger.info(f"Segmenting transcript of {len(transcript_text)} characters")
        
        # If the transcript is already small enough, return it as a single segment
        if len(transcript_text) <= self.target_segment_size:
            logger.info("Transcript is already within target size, returning as single segment")
            return [transcript_text]
        
        # Split the transcript into paragraphs
        paragraphs = self._split_into_paragraphs(transcript_text)
        logger.info(f"Split transcript into {len(paragraphs)} paragraphs")
        
        # Identify potential segment boundaries
        boundaries = self._identify_boundaries(paragraphs)
        logger.info(f"Identified {len(boundaries)} potential segment boundaries")
        
        # Create segments based on boundaries and size constraints
        segments = self._create_segments(paragraphs, boundaries)
        logger.info(f"Created {len(segments)} segments")
        
        return segments
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """
        Split the transcript text into paragraphs.
        
        Args:
            text: The transcript text
            
        Returns:
            A list of paragraph strings
        """
        # Split on double newlines (common paragraph delimiter)
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter out empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return paragraphs
    
    def _identify_boundaries(self, paragraphs: List[str]) -> List[Dict[str, Any]]:
        """
        Identify potential segment boundaries in the transcript.
        
        Args:
            paragraphs: List of paragraph strings
            
        Returns:
            List of boundary information dictionaries
        """
        boundaries = []
        cumulative_length = 0
        
        for i, paragraph in enumerate(paragraphs):
            paragraph_length = len(paragraph)
            cumulative_length += paragraph_length
            
            # Skip the first paragraph as it can't be a boundary
            if i == 0:
                continue
            
            # Calculate boundary score based on various factors
            boundary_score = 0
            
            # Check for speaker change
            if self._is_speaker_change(paragraphs[i-1], paragraph):
                boundary_score += self.boundary_weights["speaker_change"]
            
            # Check for paragraph break (always true between paragraphs)
            boundary_score += self.boundary_weights["paragraph_break"]
            
            # Check for topic change indicators
            if self._has_topic_change_indicators(paragraphs[i-1], paragraph):
                boundary_score += self.boundary_weights["topic_change"]
            
            # Record this boundary
            boundaries.append({
                "index": i,
                "position": cumulative_length - paragraph_length,
                "score": boundary_score
            })
        
        return boundaries
    
    def _is_speaker_change(self, prev_paragraph: str, curr_paragraph: str) -> bool:
        """
        Detect if there is a speaker change between paragraphs.
        
        Args:
            prev_paragraph: The previous paragraph text
            curr_paragraph: The current paragraph text
            
        Returns:
            True if there appears to be a speaker change, False otherwise
        """
        # Common speaker indicators
        speaker_pattern = r'^[A-Z][a-z]*\s*:'
        
        # Check if current paragraph starts with a speaker indicator
        if re.match(speaker_pattern, curr_paragraph):
            # Extract speaker names
            prev_speaker_match = re.match(speaker_pattern, prev_paragraph)
            curr_speaker_match = re.match(speaker_pattern, curr_paragraph)
            
            # If both have speaker indicators, check if they're different
            if prev_speaker_match and curr_speaker_match:
                prev_speaker = prev_speaker_match.group(0)
                curr_speaker = curr_speaker_match.group(0)
                return prev_speaker != curr_speaker
            
            # If only current has a speaker indicator, it's a change
            return True
        
        return False
    
    def _has_topic_change_indicators(self, prev_paragraph: str, curr_paragraph: str) -> bool:
        """
        Detect if there are indicators of a topic change between paragraphs.
        
        Args:
            prev_paragraph: The previous paragraph text
            curr_paragraph: The current paragraph text
            
        Returns:
            True if there appears to be a topic change, False otherwise
        """
        # Topic change phrases
        topic_indicators = [
            r'\bnext\b', r'\bnow\b', r'\banother\b', r'\bmoving on\b',
            r'\blet\'s talk about\b', r'\bturning to\b', r'\bregarding\b',
            r'\bon another note\b', r'\bspeaking of\b', r'\bin terms of\b',
            r'\bfirstly\b', r'\bsecondly\b', r'\bthirdly\b', r'\bfinally\b',
            r'\bto begin with\b', r'\blastly\b', r'\bin conclusion\b',
            r'\bto summarize\b'
        ]
        
        # Check for topic indicators at the start of the current paragraph
        for indicator in topic_indicators:
            if re.search(indicator, curr_paragraph[:50], re.IGNORECASE):
                return True
        
        return False
    
    def _create_segments(self, paragraphs: List[str], boundaries: List[Dict[str, Any]]) -> List[str]:
        """
        Create coherent segments from paragraphs using identified boundaries.
        
        Args:
            paragraphs: List of paragraph strings
            boundaries: List of boundary information dictionaries
            
        Returns:
            List of segment strings
        """
        # Calculate the number of segments needed based on total length
        total_length = sum(len(p) for p in paragraphs)
        ideal_num_segments = max(1, round(total_length / self.target_segment_size))
        
        logger.info(f"Aiming for approximately {ideal_num_segments} segments")
        
        # If we need just one segment, return the whole transcript
        if ideal_num_segments == 1:
            return ["\n\n".join(paragraphs)]
        
        # Sort boundaries by score (highest to lowest)
        sorted_boundaries = sorted(boundaries, key=lambda x: x["score"], reverse=True)
        
        # Take the top N-1 boundaries for N segments
        top_boundaries = sorted_boundaries[:ideal_num_segments - 1]
        
        # Sort boundaries by position (ascending)
        selected_boundaries = sorted(top_boundaries, key=lambda x: x["position"])
        
        # Add a boundary at the end
        selected_boundaries.append({"index": len(paragraphs), "position": total_length, "score": 0})
        
        # Create segments using the selected boundaries
        segments = []
        start_idx = 0
        
        for boundary in selected_boundaries:
            end_idx = boundary["index"]
            
            # Create a segment from paragraphs between start and end
            segment_paragraphs = paragraphs[start_idx:end_idx]
            segment = "\n\n".join(segment_paragraphs)
            
            # Ensure the segment isn't too small
            if len(segment) >= self.min_segment_size or start_idx == 0:
                segments.append(segment)
                start_idx = end_idx
            
        # If the last segment is too small, merge it with the previous one
        if len(segments) > 1 and len(segments[-1]) < self.min_segment_size:
            merged_segment = segments[-2] + "\n\n" + segments[-1]
            segments = segments[:-2] + [merged_segment]
        
        # Check for segments exceeding max size
        final_segments = []
        for segment in segments:
            if len(segment) > self.max_segment_size:
                # Split overly long segments
                sub_segments = self._split_long_segment(segment)
                final_segments.extend(sub_segments)
            else:
                final_segments.append(segment)
        
        logger.info(f"Final segment count: {len(final_segments)}")
        return final_segments
    
    def _split_long_segment(self, segment: str) -> List[str]:
        """
        Split a segment that is too long into multiple smaller segments.
        
        Args:
            segment: The segment text to split
            
        Returns:
            List of smaller segment strings
        """
        # If the segment isn't too long, return it as is
        if len(segment) <= self.max_segment_size:
            return [segment]
        
        # Split into paragraphs again
        paragraphs = self._split_into_paragraphs(segment)
        
        # Calculate approximate segment count needed
        segment_count = max(2, math.ceil(len(segment) / self.target_segment_size))
        
        # Calculate target paragraphs per segment
        paragraphs_per_segment = len(paragraphs) // segment_count
        
        # Create segments
        sub_segments = []
        for i in range(0, len(paragraphs), paragraphs_per_segment):
            sub_paragraphs = paragraphs[i:i + paragraphs_per_segment]
            sub_segment = "\n\n".join(sub_paragraphs)
            
            # If this isn't the last segment and it's too long, adjust
            if i + paragraphs_per_segment < len(paragraphs) and len(sub_segment) > self.max_segment_size:
                # Find a good breaking point
                break_point = self._find_sentence_break(sub_segment, self.target_segment_size)
                
                # Split at the breaking point
                first_part = sub_segment[:break_point]
                remaining = sub_segment[break_point:]
                
                sub_segments.append(first_part)
                
                # Process the remaining text recursively
                remaining_segments = self._split_long_segment(remaining)
                sub_segments.extend(remaining_segments)
                
                # Skip the rest of the loop as we've handled this portion
                break
            else:
                sub_segments.append(sub_segment)
        
        return sub_segments
    
    def _find_sentence_break(self, text: str, target_position: int) -> int:
        """
        Find a suitable sentence break near the target position.
        
        Args:
            text: The text to search for a break point
            target_position: The approximate character position to break at
            
        Returns:
            The actual character position to break at
        """
        # Define a reasonable search window
        window_start = max(0, target_position - 1000)
        window_end = min(len(text), target_position + 1000)
        
        # Extract the search window
        search_text = text[window_start:window_end]
        
        # Find all sentence endings in the search window
        sentence_endings = list(re.finditer(r'[.!?]\s+', search_text))
        
        if not sentence_endings:
            # If no sentence endings found, just break at the target
            return target_position
        
        # Find the sentence ending closest to the target
        closest_break = min(sentence_endings, key=lambda x: abs(x.end() - (target_position - window_start)))
        
        # Calculate the actual position in the original text
        actual_break = window_start + closest_break.end()
        
        return actual_break

def segment_transcript(transcript_text: str, config: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Convenience function to segment a transcript.
    
    Args:
        transcript_text: The full transcript text to segment
        config: Configuration parameters for the segmenter
        
    Returns:
        List[str]: List of segment strings
    """
    segmenter = TranscriptSegmenter(config)
    return segmenter.segment_transcript(transcript_text)
