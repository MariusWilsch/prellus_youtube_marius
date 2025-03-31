"""
Text-to-Speech (TTS) Module for Transcript Pipeline

This module provides functionality to convert processed transcripts into audio
using text-to-speech technology. The current implementation uses Kokoro TTS,
a lightweight but high-quality open-source text-to-speech model.

Available Functions:
- generate_audio_from_transcript: Convert a processed transcript to audio
"""

from .tts_generator import TTSGenerator, generate_audio_from_transcript

__all__ = ["TTSGenerator", "generate_audio_from_transcript"]
