"""
twat_pipeline - Video processing pipeline utilities using Prefect for workflow management.

This package provides a set of tasks and flows for processing video files,
including audio extraction and transcription. It uses Prefect for workflow
management and Pydantic for data validation.
"""

from importlib import metadata

from .__main__ import (
    VideoTranscript,
    extract_audio_task,
    generate_transcript_task,
    process_video_flow,
)

__version__ = metadata.version(__name__)
__all__ = [
    "VideoTranscript",
    "extract_audio_task",
    "generate_transcript_task",
    "process_video_flow",
    "__version__",
]
