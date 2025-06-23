"""
Core task functionality for video processing using Prefect.

This module provides Prefect tasks for audio extraction and transcription,
a Prefect flow to orchestrate these tasks, and a Pydantic model
for a high-level interface to video processing.
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING

from prefect import flow, task
from pydantic import BaseModel, computed_field

if TYPE_CHECKING:
    from pathlib import Path  # noqa: F401 - Used in type hints


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
    import json
    import time
    from random import randint

    time.sleep(2)  # Simulate API call

    metadata = {
        "duration": randint(60, 3600),
        "codec": "aac",
        "bitrate": f"{randint(128, 320)}kbps",
        "channels": 2,
        "sample_rate": 44100,
    }

    metadata["duration"] // 10
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

    import json
    import time
    from random import choice, randint

    # Simulate loading audio metadata
    metadata = json.loads(audio_path.read_text())

    time.sleep(1.5)

    # Simulate processing chunks with progress
    duration = metadata["duration"]
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

    @computed_field
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

    @computed_field
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
