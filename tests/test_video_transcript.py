"""Integration tests for the VideoTranscript model in twat_task.task."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from twat_task.task import VideoTranscript


@pytest.fixture
def mock_process_video_flow(monkeypatch):
    """Fixture to mock the process_video_flow used by VideoTranscript."""
    mock_flow = MagicMock()
    # Set a default return value, can be overridden in tests
    # It should return a tuple (audio_path, transcript_text)
    mock_flow.return_value = (Path("mock_audio.mp3"), "mock transcript")

    # We need to patch where it's looked up, which is in twat_task.task module
    monkeypatch.setattr("twat_task.task.process_video_flow", mock_flow)
    return mock_flow


def test_video_transcript_instantiation(tmp_path: Path):
    """Test VideoTranscript can be instantiated with a video_path."""
    video_file = tmp_path / "test_video.mp4"
    video_file.touch()

    vt = VideoTranscript(video_path=video_file)
    assert vt.video_path == video_file


def test_video_transcript_invalid_path_type():
    """Test VideoTranscript raises ValidationError for invalid video_path type."""
    with pytest.raises(ValidationError):
        VideoTranscript(video_path="not_a_path_object") # type: ignore


def test_video_transcript_audio_path_lazy_evaluation(tmp_path: Path, mock_process_video_flow: MagicMock):
    """Test audio_path is computed lazily and calls the flow."""
    video_file = tmp_path / "test_video.mp4"
    video_file.touch()

    expected_audio_output = tmp_path / "output.mp3"
    mock_process_video_flow.return_value = (expected_audio_output, "some transcript")

    vt = VideoTranscript(video_path=video_file)

    # Flow should not have been called yet
    mock_process_video_flow.fn.assert_not_called()

    # Access audio_path
    audio_p = vt.audio_path
    assert audio_p == expected_audio_output
    mock_process_video_flow.fn.assert_called_once_with(video_path=video_file)

    # Access again, should use cached value, no new call
    audio_p_cached = vt.audio_path
    assert audio_p_cached == expected_audio_output
    mock_process_video_flow.fn.assert_called_once() # Still only one call


def test_video_transcript_text_transcript_lazy_evaluation(tmp_path: Path, mock_process_video_flow: MagicMock):
    """Test text_transcript is computed lazily and calls the flow."""
    video_file = tmp_path / "test_video.mp4"
    video_file.touch()

    expected_transcript_output = "this is the expected transcript"
    mock_process_video_flow.return_value = (tmp_path / "audio.mp3", expected_transcript_output)

    vt = VideoTranscript(video_path=video_file)

    # Flow should not have been called yet
    mock_process_video_flow.fn.assert_not_called()

    # Access text_transcript
    transcript_t = vt.text_transcript
    assert transcript_t == expected_transcript_output
    mock_process_video_flow.fn.assert_called_once_with(video_path=video_file)

    # Access again, should use cached value
    transcript_t_cached = vt.text_transcript
    assert transcript_t_cached == expected_transcript_output
    mock_process_video_flow.fn.assert_called_once() # Still only one call


def test_video_transcript_access_order_calls_flow_once(tmp_path: Path, mock_process_video_flow: MagicMock):
    """Test that accessing audio_path then text_transcript (or vice-versa) calls flow only once."""
    video_file = tmp_path / "test_video.mp4"
    video_file.touch()

    expected_audio = tmp_path / "audio_example.wav"
    expected_text = "transcript from example"
    mock_process_video_flow.return_value = (expected_audio, expected_text)

    vt = VideoTranscript(video_path=video_file)

    # Access audio_path first
    ap = vt.audio_path
    assert ap == expected_audio
    mock_process_video_flow.fn.assert_called_once_with(video_path=video_file)

    # Then access text_transcript
    tt = vt.text_transcript
    assert tt == expected_text
    # The flow should still have been called only once due to caching by process_video_flow itself
    # and caching of computed fields
    mock_process_video_flow.fn.assert_called_once()

    # Test reverse access order
    mock_process_video_flow.reset_mock() # Reset call count for new instance
    vt2 = VideoTranscript(video_path=video_file)
    tt2 = vt2.text_transcript
    assert tt2 == expected_text
    mock_process_video_flow.fn.assert_called_once_with(video_path=video_file)

    ap2 = vt2.audio_path
    assert ap2 == expected_audio
    mock_process_video_flow.fn.assert_called_once()
