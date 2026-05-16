# this_file: src/twat_task/__main__.py
"""Fire CLI entry point for twat-task."""

from __future__ import annotations

import fire

from twat_task.__version__ import __version__


def _version() -> str:
    """Print the installed twat-task version."""
    return __version__


def _info() -> dict:
    """Show package info for twat-task.

    Returns:
        Dict with package name, version, and description.
    """
    return {
        "package": "twat-task",
        "version": __version__,
        "description": "Video processing task utilities using Prefect for workflow management.",
        "note": (
            "This package provides Prefect tasks/flows for video transcription. "
            "Use the Python API directly: from twat_task import process_video_flow, VideoTranscript"
        ),
    }


# TODO: Expose `run`, `list`, `status` subcommands once twat_task ships a
# CLI-friendly task registry or Prefect deployment layer. Currently the
# Prefect flow (process_video_flow) requires a Path argument and is best
# invoked via the Python API. Add them here when that surface exists.


COMMANDS: dict[str, object] = {
    "version": _version,
    "info": _info,
}


def cmd_version() -> None:
    """Entry point: twat-task-version."""
    fire.Fire(_version, name="twat-task-version")


def cmd_info() -> None:
    """Entry point: twat-task-info."""
    fire.Fire(_info, name="twat-task-info")


def main() -> None:
    """Fire CLI dispatcher for twat-task."""
    fire.Fire(COMMANDS, name="twat-task")


if __name__ == "__main__":
    main()
