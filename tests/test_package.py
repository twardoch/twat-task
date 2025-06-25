"""Test suite for twat_task."""

import twat_task # PLC0415: Moved to top level


def test_version() -> None: # Added return type hint for MyPy
    """Verify package exposes version."""
    assert twat_task.__version__
