"""Test suite for twat_task."""

import pytest

import twat_task  # PLC0415: Moved to top level


def test_version() -> None:  # Added return type hint for MyPy
    """Verify package exposes version."""
    assert twat_task.__version__


def test_public_exports_import() -> None:
    """Every public export listed in __all__ is importable from twat_task."""
    for name in twat_task.__all__:
        assert getattr(twat_task, name) is not None


def test_main_outputs_version(capsys: pytest.CaptureFixture[str]) -> None:
    """The lightweight plugin CLI exposes a stable smoke-testable main()."""
    twat_task.main()

    assert "twat-task v" in capsys.readouterr().out
