"""
Tests for the YouTube Transcript Fetcher module.

This module contains tests for the YouTubeTranscriptFetcher class, which
is responsible for extracting transcripts from YouTube videos.
"""

import unittest
from unittest.mock import patch, MagicMock
import pytest

from src.transcript_pipeline.fetcher.youtube_transcript import YouTubeTranscriptFetcher


class TestYouTubeTranscriptFetcher(unittest.TestCase):
    """Test cases for the YouTubeTranscriptFetcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fetcher = YouTubeTranscriptFetcher()
        
        # Sample transcript data for testing
        self.sample_transcript = [
            {
                "text": "Hello, this is a test transcript.",
                "start": 0.0,
                "duration": 2.5
            },
            {
                "text": "This is the second segment.",
                "start": 2.5,
                "duration": 2.0
            }
        ]
    
    def test_extract_video_id(self):
        """Test extracting video ID from different URL formats."""
        # Standard YouTube URL
        url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        # YouTube URL with additional parameters
        url2 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s"
        # YouTube short URL
        url3 = "https://youtu.be/dQw4w9WgXcQ"
        # YouTube embed URL
        url4 = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        
        self.assertEqual(self.fetcher.extract_video_id(url1), "dQw4w9WgXcQ")
        self.assertEqual(self.fetcher.extract_video_id(url2), "dQw4w9WgXcQ")
        self.assertEqual(self.fetcher.extract_video_id(url3), "dQw4w9WgXcQ")
        self.assertEqual(self.fetcher.extract_video_id(url4), "dQw4w9WgXcQ")
        
        # Test invalid URL
        with self.assertRaises(ValueError):
            self.fetcher.extract_video_id("https://www.example.com")
    
    @patch('src.transcript_pipeline.fetcher.youtube_transcript.YouTubeTranscriptApi')
    def test_fetch_transcript_preferred_language(self, mock_api):
        """Test fetching transcript in preferred language."""
        # Setup mock
        mock_api.get_transcript.return_value = self.sample_transcript
        
        # Call method
        result = self.fetcher.fetch_transcript("dQw4w9WgXcQ")
        
        # Check results
        self.assertEqual(result, self.sample_transcript)
        mock_api.get_transcript.assert_called_once_with("dQw4w9WgXcQ", languages=["en"])
    
    @patch('src.transcript_pipeline.fetcher.youtube_transcript.YouTubeTranscriptApi')
    def test_fetch_transcript_with_metadata(self, mock_api):
        """Test fetching transcript with metadata."""
        # Setup mock
        mock_api.get_transcript.return_value = self.sample_transcript
        
        # Call method
        result = self.fetcher.fetch_transcript_with_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        # Check results
        self.assertEqual(result["transcript"], self.sample_transcript)
        self.assertEqual(result["metadata"]["video_id"], "dQw4w9WgXcQ")
        self.assertEqual(result["metadata"]["video_url"], "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        # Check timestamps
        self.assertEqual(result["metadata"]["timestamp"]["start"], 0.0)
        self.assertEqual(result["metadata"]["timestamp"]["end"], 4.5)  # 2.5 + 2.0
    
    @patch('src.transcript_pipeline.fetcher.youtube_transcript.YouTubeTranscriptApi')
    def test_fetch_transcript_fallback(self, mock_api):
        """Test fallback behavior when preferred language not available."""
        # Setup mocks for fallback scenario
        from youtube_transcript_api import NoTranscriptFound
        mock_api.get_transcript.side_effect = NoTranscriptFound("en")
        
        # Mock transcript list
        mock_transcript_list = MagicMock()
        mock_transcript = MagicMock()
        mock_transcript.fetch.return_value = self.sample_transcript
        mock_transcript.language_code = "fr"
        
        mock_transcript_list.find_manually_created_transcript.return_value = mock_transcript
        mock_api.list_transcripts.return_value = mock_transcript_list
        
        # Call method
        result = self.fetcher.fetch_transcript("dQw4w9WgXcQ")
        
        # Check results
        self.assertEqual(result, self.sample_transcript)
        mock_api.list_transcripts.assert_called_once_with("dQw4w9WgXcQ")
        mock_transcript_list.find_manually_created_transcript.assert_called_once()
    
    @patch('src.transcript_pipeline.fetcher.youtube_transcript.YouTubeTranscriptApi')
    def test_transcript_disabled(self, mock_api):
        """Test handling of disabled transcripts."""
        # Setup mock
        from youtube_transcript_api import TranscriptsDisabled
        mock_api.get_transcript.side_effect = TranscriptsDisabled()
        
        # Call method and check exception
        with self.assertRaises(ValueError) as context:
            self.fetcher.fetch_transcript("dQw4w9WgXcQ")
        
        self.assertIn("Transcripts are disabled", str(context.exception))


if __name__ == '__main__':
    unittest.main() 