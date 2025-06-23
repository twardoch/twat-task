# twat-task

Video processing pipeline utilities using Prefect for workflow management. This package provides a set of tasks and flows for processing video files, including audio extraction and transcription.

**Note:** The current version uses mock implementations for video/audio processing tasks, simulating delays and creating placeholder files. It serves as a structural foundation for integrating actual processing logic.

## Features

- High-level interface (`VideoTranscript`) for video processing.
- Prefect-based tasks for:
  - Audio extraction from video files (mocked).
  - Speech-to-text transcription (mocked).
- Prefect flow (`process_video_flow`) to orchestrate the tasks.
- Workflow management capabilities via Prefect (retries, logging, caching).
- Pydantic models for data validation.
- Modern Python features with type hints.
- Managed with Hatch (testing, linting, building).

## Installation

Currently, this package is not published on PyPI. To install it for development or local use, clone the repository and install it in editable mode:

```bash
git clone https://github.com/twardoch/twat-task.git
cd twat-task
pip install -e .
```

This will install the package and its dependencies.

## Usage

Here's a basic example of how to use `twat-task`:

```python
from pathlib import Path
from twat_task import VideoTranscript

# Create a dummy video file for the example to run
# In a real scenario, this would be an actual video file.
dummy_video_path = Path("example_video.mp4")
dummy_video_path.touch()

# Initialize VideoTranscript with the path to your video file
vt = VideoTranscript(video_path=dummy_video_path)

# Accessing audio_path will trigger the (mock) audio extraction
# The extracted audio path will be like 'example_video.mp3'
print(f"Mock audio path: {vt.audio_path}")

# Accessing text_transcript will trigger (mock) transcription
# This will print a randomly generated string of text
print(f"Mock transcript: {vt.text_transcript}")

# Clean up the dummy files (optional)
vt.audio_path.unlink(missing_ok=True)
dummy_video_path.unlink(missing_ok=True)
```

When you access `vt.audio_path` or `vt.text_transcript` for the first time, the underlying Prefect flow `process_video_flow` will run, executing the (currently mock) audio extraction and transcription tasks. The results are cached, so subsequent access will return the stored values without re-running the tasks.

## Development

This project uses [Hatch](https://hatch.pypa.io/) for environment and project management.

1.  **Setup:**
    *   Ensure you have Hatch installed (`pip install hatch`).
    *   The dependencies, including development tools, are managed by `pyproject.toml`.

2.  **Running Tests:**
    ```bash
    hatch run test
    ```
    To run tests with coverage:
    ```bash
    hatch run test-cov
    ```

3.  **Linting and Type Checking:**
    ```bash
    hatch run lint:all
    ```
    This runs `ruff` for formatting/linting and `mypy` for type checking.
    To auto-format:
    ```bash
    hatch run lint:fmt
    ```

4.  **Building the Package:**
    ```bash
    hatch build
    ```
    This will create wheel and sdist packages in the `dist/` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License
