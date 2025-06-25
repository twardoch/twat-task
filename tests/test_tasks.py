"""Unit tests for tasks in twat_task.task."""

import json
from pathlib import Path
from unittest.mock import Mock, patch # Added Mock for type hint

import pytest
from twat_task.task import extract_audio_task, generate_transcript_task


def test_extract_audio_task_creates_output_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that extract_audio_task creates an output file with JSON content."""
    monkeypatch.setattr("time.sleep", lambda *_: None)  # ARG005: Use *args or _

    video_file = tmp_path / "test_video.mp4"
    audio_file = tmp_path / "test_audio.mp3"

    # Create a dummy video file (not strictly necessary for mock, but good practice)
    video_file.touch()

    extract_audio_task.fn(video_path=video_file, audio_path=audio_file)

    assert audio_file.exists()
    try:
        content = json.loads(audio_file.read_text())
        assert "duration" in content
        assert content["codec"] == "aac"  # Check specific mock value
        assert content["channels"] == 2  # Check specific mock value
        assert "bitrate" in content
        assert "sample_rate" in content
        assert content["sample_rate"] == 44100  # Check specific mock value
    except json.JSONDecodeError:
        pytest.fail("Output file is not valid JSON.")


def test_extract_audio_task_simulates_processing(tmp_path: Path) -> None:
    """Test that extract_audio_task simulates some processing time (mocked)."""
    video_file = tmp_path / "test_video.mp4"
    audio_file = tmp_path / "test_audio.mp3"
    video_file.touch()

    with patch("time.sleep") as mock_sleep:
        extract_audio_task.fn(video_path=video_file, audio_path=audio_file)
        # Expect sleeps: 1 initial, 10 in loop (total 11)
        # Original sleeps: time.sleep(2) and 10 * time.sleep(0.5)
        # Ruff S101: allow assert
        assert (
            mock_sleep.call_count >= 2
        )  # Check if sleep was called at least for the main parts


# Tests for generate_transcript_task


def test_generate_transcript_task_returns_string(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that generate_transcript_task returns a string."""
    monkeypatch.setattr("time.sleep", lambda *_: None)  # ARG005: Use *args or _

    audio_file = tmp_path / "test_audio.mp3"
    # Create a dummy audio metadata file, as expected by the mock task
    mock_metadata = {"duration": 120, "codec": "aac"}
    audio_file.write_text(json.dumps(mock_metadata))

    transcript = generate_transcript_task.fn(audio_path=audio_file)
    assert isinstance(transcript, str)
    assert len(transcript) > 0  # Expect some text


def test_generate_transcript_task_simulates_processing(tmp_path: Path) -> None:
    """Test that generate_transcript_task simulates processing (mocked)."""
    audio_file = tmp_path / "test_audio.mp3"
    # Ensure 'duration' is int for the calculation below and for what the task expects
    mock_metadata_content = {"duration": 180, "codec": "aac"}
    audio_file.write_text(json.dumps(mock_metadata_content))

    # The following line was duplicated in the original code, removing one instance.
    # mock_metadata = {"duration": 180, "codec": "aac"}
    # audio_file.write_text(json.dumps(mock_metadata))

    with patch("time.sleep") as mock_sleep:
        generate_transcript_task.fn(audio_path=audio_file)
        # Original: time.sleep(1.5) -> 1 call
        # Loop: N * time.sleep(0.3) where N = duration // 30
        # For duration 180, N = 180 // 30 = 6 calls.
        # Total expected calls = 1 (initial) + 6 (loop) = 7 calls.
        duration_from_mock = mock_metadata_content["duration"]
        if not isinstance(duration_from_mock, int): # mypy check
            raise TypeError("Duration in mock data must be an int for this test.")
        expected_sleep_calls = 1 + (duration_from_mock // 30)
        # Ruff S101: allow assert
        assert mock_sleep.call_count == expected_sleep_calls
