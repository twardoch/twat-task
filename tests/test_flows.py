"""Unit tests for flows in twat_task.task."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from twat_task.task import process_video_flow


@pytest.fixture
def mock_tasks(monkeypatch):
    """Fixture to mock tasks used by process_video_flow."""
    mock_extract = MagicMock()
    mock_generate = MagicMock(return_value="mock transcript")

    monkeypatch.setattr("twat_task.task.extract_audio_task", mock_extract)
    monkeypatch.setattr("twat_task.task.generate_transcript_task", mock_generate)
    return mock_extract, mock_generate


def test_process_video_flow_new_video(tmp_path: Path, mock_tasks):
    """Test process_video_flow when audio needs extraction."""
    mock_extract_audio, mock_generate_transcript = mock_tasks
    video_file = tmp_path / "new_video.mp4"
    video_file.touch() # Create dummy video file

    expected_audio_path = video_file.with_suffix(".mp3")

    # Call the flow's underlying function directly
    audio_path, transcript = process_video_flow.fn(video_path=video_file)

    assert audio_path == expected_audio_path
    assert transcript == "mock transcript"

    # Check that extract_audio_task was called since audio file doesn't exist
    mock_extract_audio.fn.assert_called_once_with(video_file, expected_audio_path)
    # Check that generate_transcript_task was called with the audio path
    mock_generate_transcript.fn.assert_called_once_with(expected_audio_path)


def test_process_video_flow_existing_audio(tmp_path: Path, mock_tasks):
    """Test process_video_flow when audio file already exists."""
    mock_extract_audio, mock_generate_transcript = mock_tasks
    video_file = tmp_path / "existing_video.mp4"
    audio_file = tmp_path / "existing_video.mp3"

    video_file.touch()
    audio_file.touch() # Create dummy audio file to simulate existence

    # Call the flow's underlying function directly
    audio_path, transcript = process_video_flow.fn(video_path=video_file)

    assert audio_path == audio_file
    assert transcript == "mock transcript"

    # Check that extract_audio_task was NOT called
    mock_extract_audio.fn.assert_not_called()
    # Check that generate_transcript_task was called
    mock_generate_transcript.fn.assert_called_once_with(audio_file)


def test_process_video_flow_return_values(tmp_path: Path, monkeypatch):
    """Test the return values of process_video_flow."""
    video_file = tmp_path / "test.mp4"
    video_file.touch()
    expected_audio_path = video_file.with_suffix(".mp3")
    expected_transcript = "this is a test transcript"

    # Mock the sub-tasks more simply for this specific test
    mock_extract = MagicMock()
    mock_generate = MagicMock(return_value=expected_transcript)

    monkeypatch.setattr("twat_task.task.extract_audio_task", mock_extract)
    monkeypatch.setattr("twat_task.task.generate_transcript_task", mock_generate)

    audio_path, transcript_text = process_video_flow.fn(video_path=video_file)

    assert audio_path == expected_audio_path
    assert transcript_text == expected_transcript
