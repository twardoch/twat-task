"""twat-task: Video processing task utilities using Prefect for workflow management.

This package provides a set of tasks and flows for processing video files,
including audio extraction and transcription. It uses Prefect for workflow
management and Pydantic for data validation.

Example:
    >>> from twat_task import VideoTranscript
    >>> from pathlib import Path
    >>>
    >>> # Process a video file
    >>> vt = VideoTranscript(video_path=Path("video.mp4"))
    >>> print(vt.audio_path)  # Extracts audio
    >>> print(vt.text_transcript)  # Generates transcript
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("twat-task")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

from twat_task.task import (
    VideoTranscript,
    extract_audio_task,
    generate_transcript_task,
    process_video_flow,
)


def main() -> None:
    """CLI entry point for twat-task."""
    from twat_task.__main__ import main as cli_main  # noqa: PLC0415

    cli_main()


__all__ = [
    "VideoTranscript",
    "__version__",
    "extract_audio_task",
    "generate_transcript_task",
    "main",
    "process_video_flow",
]
