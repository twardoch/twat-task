"""
Core task functionality for video processing using Prefect.

This module provides Prefect tasks for audio extraction and transcription,
a Prefect flow to orchestrate these tasks, and a Pydantic model
for a high-level interface to video processing.
"""

from __future__ import annotations

import json # PLC0415: Moved to top level
import time # PLC0415: Moved to top level
from functools import cached_property
from pathlib import Path
from random import choice, randint # PLC0415: Moved to top level, S311: random is fine for mock data
from typing import TYPE_CHECKING

from prefect import flow, task
from pydantic import BaseModel, computed_field

if TYPE_CHECKING:
    from pathlib import Path


@task(retries=2)
def extract_audio_task(video_path: Path, audio_path: Path) -> None:
    """
    Extract audio from a video file.

    This task simulates audio extraction. In a real implementation,
    this would use a library like moviepy or ffmpeg.

    Args:
        video_path: Path to the input video file.
        audio_path: Path where the extracted audio should be saved.

    Note:
        This is currently a mock implementation for demonstration purposes.
        It simulates a delay and creates a text file with mock metadata
        instead of an actual audio file.
    """

    # Simulate fetching video metadata as JSON
    # Imports moved to top level

    time.sleep(2)  # Simulate API call

    metadata = {
        "duration": randint(60, 3600),  # nosec B311: random is fine for mock data
        "codec": "aac",
        "bitrate": f"{randint(128, 320)}kbps",  # nosec B311: random is fine for mock data
        "channels": 2,
        "sample_rate": 44100,
    }

    duration_val = metadata["duration"]
    if not isinstance(duration_val, int): # mypy check
        raise TypeError("Duration should be an int")
    duration_val // 10 # Original logic, now with type safety for mypy
    for _i in range(10):
        time.sleep(0.5)  # Simulate processing time

    # Save simulated audio and metadata
    audio_path.write_text(json.dumps(metadata))


@task(retries=2)
def generate_transcript_task(audio_path: Path) -> str:
    """
    Generate transcript from an audio file.

    This task simulates speech recognition and transcription. In a real
    implementation, this would use a service like OpenAI Whisper,
    Google Speech-to-Text, or another speech recognition library.

    Args:
        audio_path: Path to the input audio file.

    Returns:
        The generated transcript text.

    Note:
        This is currently a mock implementation for demonstration purposes.
        It simulates reading metadata from the audio file (which itself is
        a mock) and generating random text.
    """
    # Imports moved to top level

    # Simulate loading audio metadata
    loaded_metadata = json.loads(audio_path.read_text()) # Renamed to avoid conflict with outer scope 'metadata'

    time.sleep(1.5)

    # Simulate processing chunks with progress
    duration = loaded_metadata.get("duration")
    if not isinstance(duration, int): # mypy check
        # Fallback or error for missing/invalid duration
        duration = 60 # Default to 60 seconds if not found or invalid
        # Or raise TypeError(f"Duration {duration} should be an int or is missing")

    chunk_size = 30  # Process in 30-second chunks
    chunks = duration // chunk_size


    words = [
        "hello",
        "world",
        "this",
        "is",
        "a",
        "test",
        "video",
        "with",
        "some",
        "random",
        "words",
        "being",
        "processed",
    ]

    transcript_parts = []
    for _i in range(chunks):
        time.sleep(0.3)  # Simulate API call and processing
        # Generate some random text
        # nosec B311: random is fine for mock data
        chunk_text = " ".join(choice(words) for _ in range(randint(5, 15)))
        transcript_parts.append(chunk_text)

    return " ".join(transcript_parts)


@flow
def process_video_flow(video_path: Path) -> tuple[Path, str]:
    """
    Process a video file to extract audio and generate its transcript.

    This Prefect flow coordinates the video processing tasks:
    1. Extract audio from the video (if an audio file doesn't already exist).
    2. Generate a transcript from the extracted audio.

    Args:
        video_path: Path to the input video file.

    Returns:
        A tuple containing:
            - `audio_path` (Path): Path to the extracted (mock) audio file.
            - `transcript` (str): The generated (mock) transcript text.
    """
    audio = video_path.with_suffix(".mp3")
    # Only extract audio if the file does not exist
    if not audio.exists():
        extract_audio_task(video_path, audio)
    transcript = generate_transcript_task(audio)
    return audio, transcript


class VideoTranscript(BaseModel):
    """
    A Pydantic model for managing video transcription.

    This class provides a high-level interface for processing a video file.
    Audio extraction and transcript generation are performed lazily using
    Prefect flows when the `audio_path` or `text_transcript` attributes
    are accessed for the first time. Results are cached for subsequent access.

    Attributes:
        video_path: The path to the input video file.
        audio_path: Path to the extracted audio file. This is a computed
            property. Accessing it will trigger the video processing flow
            if it hasn't run yet.
        text_transcript: The generated transcript text. This is a computed
            property. Accessing it will trigger the video processing flow
            if it hasn't run yet.
    """

    video_path: Path

    @computed_field(alias="audio_path", repr=False) # repr=False to avoid inclusion in model repr if desired
    @cached_property
    def audio_path(self) -> Path:
        """
        Gets the path to the extracted audio file.

        If the video has not been processed yet, this will trigger the
        `process_video_flow` to extract audio and generate the transcript.
        The result is cached.
        """
        audio, _ = process_video_flow(self.video_path)
        return audio

    @computed_field(alias="text_transcript", repr=False) # repr=False to avoid inclusion in model repr if desired
    @cached_property
    def text_transcript(self) -> str:
        """
        Gets the transcript text for the video.

        If the video has not been processed yet, this will trigger the
        `process_video_flow` to extract audio and generate the transcript.
        The result is cached.
        """
        _, transcript = process_video_flow(self.video_path)
        return transcript
