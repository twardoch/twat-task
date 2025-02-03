# twat-pipeline

Video processing pipeline utilities using Prefect for workflow management. This package provides a set of tasks and flows for processing video files, including audio extraction and transcription.

## Features

- High-level interface for video processing pipelines
- Built-in tasks for common operations:
  - Audio extraction from video files
  - Speech-to-text transcription
- Workflow management using Prefect:
  - Automatic retries for failed tasks
  - Progress tracking and logging
  - Task caching and resumability
- Pydantic models for data validation
- Type hints and modern Python features

## Installation

```bash
pip install twat-pipeline
```

## Usage

### Basic Usage

The simplest way to use the package is through the `VideoTranscript` class:

```python
from pathlib import Path
from twat_pipeline import VideoTranscript

# Create a video transcript object
vt = VideoTranscript(video_path=Path("video.mp4"))

# Access computed properties (processing happens automatically)
print("Audio file:", vt.audio_path)
print("Transcript:", vt.text_transcript)
```

### Using Individual Tasks

You can also use the individual tasks and flows directly:

```python
from pathlib import Path
from twat_pipeline import extract_audio_task, generate_transcript_task, process_video_flow

# Process a video file step by step
video_path = Path("video.mp4")
audio_path = video_path.with_suffix(".mp3")

# Extract audio
extract_audio_task(video_path, audio_path)

# Generate transcript
transcript = generate_transcript_task(audio_path)
print("Transcript:", transcript)

# Or use the complete flow
audio, transcript = process_video_flow(video_path)
```

### Task Configuration

Tasks are configured with sensible defaults:

- `extract_audio_task`: 
  - Retries: 2 attempts
  - Output format: MP3
  - Metadata preservation

- `generate_transcript_task`:
  - Retries: 2 attempts
  - Chunk size: 30 seconds
  - Progress tracking

### Customization

The package is designed to be easily customizable:

```python
from prefect import task
from twat_pipeline import VideoTranscript

# Create a custom audio extraction task
@task(retries=3, cache_key_fn=lambda x: str(x))
def my_audio_extractor(video_path, audio_path):
    # Your custom audio extraction logic here
    pass

# Use it in your workflow
class CustomVideoTranscript(VideoTranscript):
    @property
    def audio_path(self):
        audio = self.video_path.with_suffix(".wav")
        my_audio_extractor(self.video_path, audio)
        return audio
```

## Dependencies

- `prefect`: For workflow management and task orchestration
- `pydantic`: For data validation and model management

## Note

The current implementation uses mock tasks for demonstration. In a real-world scenario, you would:

1. Replace `extract_audio_task` with actual video processing (e.g., using `moviepy` or `ffmpeg`)
2. Replace `generate_transcript_task` with a real speech recognition service (e.g., Whisper or Google Speech-to-Text)

## License

MIT License 