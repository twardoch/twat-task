# twat-task

**Part of the [TWAT (Twardoch Workflow Automation Tools) collection](https://pypi.org/project/twat/)**

`twat-task` is a Python package designed for building and managing video processing pipelines. It leverages the power of [Prefect](https://www.prefect.io/) for robust workflow orchestration, focusing initially on tasks like audio extraction from video files and generating text transcripts from that audio.

While the current version uses mock implementations for the core video/audio processing (simulating delays and creating placeholder files), it provides a solid structural foundation and a clear API for integrating actual processing logic.

## What is `twat-task`?

`twat-task` provides a set of pre-defined [Prefect](https://www.prefect.io/) tasks and flows specifically tailored for common video processing operations. It simplifies the process of:

*   **Extracting audio:** Separating the audio track from a video file.
*   **Transcribing audio:** Converting spoken words in the audio into written text.
*   **Orchestrating these tasks:** Ensuring that these steps run in the correct order, with proper error handling, caching, and logging, thanks to Prefect.

It's built with modern Python features, including type hints and Pydantic models for data validation and a clear, easy-to-use interface.

## Who is it for?

`twat-task` is aimed at:

*   **Python Developers:** Anyone looking to incorporate video processing capabilities into their applications or workflows.
*   **Data Engineers & Scientists:** Professionals who need to process video content at scale, for example, to analyze speech patterns, generate subtitles, or make video content searchable.
*   **Prefect Users:** Developers already using or planning to use Prefect for workflow automation, as `twat-task` provides ready-made components that integrate seamlessly.
*   **Users of the TWAT Collection:** If you're already using other tools from the [TWAT (Twardoch Workflow Automation Tools) collection](https://pypi.org/project/twat/), `twat-task` will fit naturally into your toolkit.

## Why is it useful?

*   **Simplified Video Processing:** Offers a high-level interface (`VideoTranscript`) that abstracts away the complexities of individual processing steps.
*   **Workflow Management:** Built on Prefect, it provides:
    *   **Robustness:** Automatic retries for failed tasks.
    *   **Caching:** Results are cached, so re-running a flow with the same inputs won't re-process unchanged data, saving time and resources.
    *   **Observability:** Detailed logging and a UI (via Prefect) for monitoring flow runs.
    *   **Scalability:** Prefect allows for scaling workflows from local execution to distributed environments.
*   **Extensible:** While currently mock, the tasks are designed to be easily replaced with actual video and audio processing libraries (e.g., MoviePy, FFmpeg, OpenAI Whisper, Google Speech-to-Text).
*   **Modern Python:** Uses Pydantic for data validation and settings management, and `functools.cached_property` for efficient computation.
*   **Part of an Ecosystem:** As a component of the `twat` collection, it's designed to work well with other related tools for workflow automation.

## Installation

### From PyPI

As `twat-task` is part of the [TWAT collection](https://pypi.org/project/twat/), it is available on PyPI. You can install it using pip:

```bash
pip install twat-task
```

You can check the [twat-task PyPI page](https://pypi.org/project/twat-task/) for specific versions and more details.

### For Development or Local Use

To install the package for development or local use (e.g., to contribute or modify the code), clone the repository and install it in editable mode:

```bash
git clone https://github.com/twardoch/twat-task.git
cd twat-task
pip install -e .[dev] # Installs core and development dependencies
```
This command installs the package along with its core and development dependencies (like testing and linting tools specified in `project.optional-dependencies.dev` in `pyproject.toml`).

## Usage

`twat-task` is primarily designed to be used programmatically within your Python applications.

### Programmatic Usage

The main interface is the `VideoTranscript` class. Here's a basic example:

```python
from pathlib import Path
from twat_task import VideoTranscript

# Create a dummy video file for the example.
# In a real scenario, this would be your actual video file.
dummy_video_path = Path("example_video.mp4")
if not dummy_video_path.exists():
    # Create a tiny file if it doesn't exist
    dummy_video_path.write_text("This is a dummy video file content.")

# Initialize VideoTranscript with the path to your video file
vt = VideoTranscript(video_path=dummy_video_path)

# 1. Accessing audio_path (triggers audio extraction if not already done)
# The (mock) extracted audio path will typically be 'example_video.mp3'.
# This currently creates a JSON file with mock metadata instead of a real audio file.
try:
    print(f"Mock audio path: {vt.audio_path}")
    # You can inspect the content of vt.audio_path to see the mock metadata:
    # if vt.audio_path.exists():
    #     with open(vt.audio_path, 'r') as f:
    #         print(f"Mock audio metadata: {f.read()}")
except Exception as e:
    print(f"Error accessing audio_path: {e}")

# 2. Accessing text_transcript (triggers transcription if not already done)
# This will print a randomly generated string of text based on the mock audio data.
try:
    print(f"Mock transcript: {vt.text_transcript}")
except Exception as e:
    print(f"Error accessing text_transcript: {e}")

# How it works:
# - When you access `vt.audio_path` or `vt.text_transcript` for the first time
#   for a given `VideoTranscript` instance, the underlying Prefect flow
#   `process_video_flow` runs for that specific video_path.
# - This flow executes the (currently mock) audio extraction and transcription tasks.
# - Results are cached. Subsequent access to these properties for the same
#   `VideoTranscript` instance (and thus the same video_path) will return
#   the stored values without re-running the tasks.

# Optional: Clean up the dummy files created by the example
# Ensure audio_path was successfully created before trying to unlink
if hasattr(vt, '_audio_path_computed_value_') and vt.audio_path.exists(): # Check if audio_path was accessed and file exists
     vt.audio_path.unlink(missing_ok=True)
if dummy_video_path.exists():
    dummy_video_path.unlink(missing_ok=True)
```

This example demonstrates the lazy-loading nature of the processing. The actual (mock) audio extraction and transcription only occur when the `audio_path` or `text_transcript` properties are first accessed.

---

## Technical Deep Dive

This section provides a more detailed look into the internal workings of `twat-task` and guidelines for development and contribution.

### How the Code Works

The `twat-task` package is structured around a Pydantic model that orchestrates Prefect tasks and flows for video processing.

1.  **`VideoTranscript` (Pydantic Model)**:
    *   Located in `src/twat_task/task.py`.
    *   This is the primary user-facing class. It takes a `video_path` (Path object) as input during initialization.
    *   It uses Pydantic for data validation and to define computed fields for `audio_path` and `text_transcript`.
    *   **Lazy Evaluation & Caching**:
        *   The properties `audio_path` and `text_transcript` are implemented using `@computed_field` (from Pydantic) and `@cached_property` (from `functools`).
        *   This means the actual processing (audio extraction, transcription) is only triggered when one of these properties is accessed for the first time for a given `VideoTranscript` instance.
        *   Once computed, the results are cached for that instance. Subsequent accesses return the stored value directly, avoiding redundant processing for that instance.

2.  **`process_video_flow` (Prefect Flow)**:
    *   Defined in `src/twat_task/task.py`.
    *   This is the main Prefect flow that orchestrates the video processing pipeline.
    *   When `VideoTranscript.audio_path` or `VideoTranscript.text_transcript` is accessed, this flow is invoked with the `video_path`.
    *   **Steps:**
        1.  It determines the target path for the audio file (e.g., `video_name.mp3`).
        2.  It calls the `extract_audio_task` if the audio file doesn't already exist at the target path.
        3.  It then calls the `generate_transcript_task` using the path of the (mock) audio file.
    *   Returns a tuple: `(audio_path, transcript_text)`. Prefect handles caching of task runs based on inputs, which can further optimize re-runs across different `VideoTranscript` instances if inputs to tasks are identical.

3.  **`extract_audio_task` (Prefect Task)**:
    *   Defined in `src/twat_task/task.py`.
    *   **Current Behavior (Mock):**
        *   Simulates a delay to mimic real audio extraction time.
        *   Does **not** actually process video or extract audio.
        *   Instead, it creates a JSON text file at the specified `audio_path` (e.g., `example_video.mp3`).
        *   This JSON file contains mock metadata about the supposed audio, such as `duration`, `codec`, `bitrate`, etc.
    *   **Future Implementation:** This task is intended to be replaced with actual audio extraction logic using libraries like `moviepy` or by calling `ffmpeg` subprocesses.
    *   Decorated with `@task(retries=2)` from Prefect, enabling automatic retries on failure.

4.  **`generate_transcript_task` (Prefect Task)**:
    *   Defined in `src/twat_task/task.py`.
    *   **Current Behavior (Mock):**
        *   Simulates a delay for transcription.
        *   Reads the mock metadata from the JSON file created by `extract_audio_task`.
        *   Generates a random string of text to serve as the mock transcript. The length of the transcript is loosely based on the mock `duration`.
    *   **Future Implementation:** This task is designed to be replaced with actual speech-to-text engines (e.g., OpenAI Whisper API, Google Cloud Speech-to-Text, local models like Vosk).
    *   Also decorated with `@task(retries=2)` for Prefect-managed retries.

5.  **Project Structure**:
    *   `src/twat_task/`: Contains the main package code.
        *   `__init__.py`: Makes `VideoTranscript` and other necessary components available for import.
        *   `task.py`: Core logic including Pydantic models, Prefect tasks, and flows.
        *   `__version__.py`: Version information, managed by `hatch-vcs`.
    *   `tests/`: Contains Pytest tests.
    *   `examples/`: Usage examples (e.g., `testprefect_example.py`).
    *   `pyproject.toml`: Defines project metadata, dependencies, build system (`hatch`), and development tool configurations.
    *   `.github/workflows/`: Contains GitHub Actions for CI/CD (e.g., testing, releasing).

### Development Environment & Workflow

This project uses [Hatch](https://hatch.pypa.io/latest/) for managing dependencies, environments, and common development tasks. The configuration is defined in `pyproject.toml`.

1.  **Prerequisites:**
    *   Python 3.10 or newer.
    *   Install Hatch: `pip install hatch`

2.  **Setup:**
    *   Clone the repository: `git clone https://github.com/twardoch/twat-task.git`
    *   Navigate to the project directory: `cd twat-task`
    *   To set up the development environment and install dependencies (including dev tools):
        ```bash
        hatch env create # Ensures the default environment is set up
        # For installing in editable mode for IDEs, after cloning:
        # pip install -e .[dev]
        ```
        If you plan to use `hatch run ...` commands, `hatch env create` (or allowing Hatch to create it on first run) is sufficient. The `pip install -e .[dev]` is good for ensuring your IDE picks up the editable install.

3.  **Running Common Tasks (using Hatch scripts defined in `pyproject.toml`):**

    *   **Run Tests:**
        ```bash
        hatch run test  # Uses script from [tool.hatch.envs.default.scripts]
        ```
        To run tests with coverage report:
        ```bash
        hatch run test-cov
        ```
        Test files are located in the `tests/` directory.

    *   **Linting and Formatting:**
        The project uses [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting, and [MyPy](http://mypy-lang.org/) for static type checking.
        ```bash
        # Run all checks (linting, type-checking, tests with coverage)
        hatch run check-all # Script from [tool.hatch.envs.default.scripts]

        # Auto-format code using Ruff
        hatch run format

        # Run Ruff linter separately
        hatch run lint

        # Run MyPy type checker separately
        hatch run type-check
        ```
        Configuration for Ruff and MyPy can be found in `pyproject.toml`.
        Note: `hatch run <script_name>` will run scripts from the `[tool.hatch.envs.default.scripts]` section if no environment is specified.

    *   **Building the Package:**
        To create wheel and sdist packages (output to `dist/` directory):
        ```bash
        hatch build
        ```

4.  **Pre-commit Hooks:**
    *   The project is configured with `pre-commit` (see `.pre-commit-config.yaml`).
    *   To install pre-commit hooks:
        ```bash
        # Ensure pre-commit is installed (often included via dev dependencies)
        # pip install pre-commit
        pre-commit install
        ```
    *   This will run checks (like Ruff formatting and linting) automatically before each commit.

### Coding and Contribution Guidelines

*   **Coding Style:**
    *   Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
    *   Adhere to the Ruff linting rules defined in `pyproject.toml` (e.g., line length 88 characters, import sorting via `isort` settings within Ruff).
    *   All code should be type-hinted and pass MyPy checks as configured in `pyproject.toml`.
*   **Testing:**
    *   Write Pytest tests for new features and bug fixes.
    *   Ensure tests pass and maintain high code coverage.
*   **Commit Messages:**
    *   Follow conventional commit message guidelines (e.g., `feat: add new feature`, `fix: resolve bug`). This helps in automated changelog generation and versioning.
*   **Dependencies:**
    *   Manage dependencies using `pyproject.toml`. Add new dependencies to the appropriate section (e.g., `dependencies` or `project.optional-dependencies`).
*   **Contributions:**
    *   Contributions are highly welcome!
    *   Please open an issue first to discuss significant changes or new features.
    *   Submit pull requests against the `main` (or default) development branch.
    *   Ensure your code passes all automated checks (tests, linting, type checks) run by GitHub Actions (see `.github/workflows/`) before submitting a PR.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
