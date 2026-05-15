"""Command-line entry point for twat-task."""

from __future__ import annotations

from twat_task import __version__


def main() -> None:
    """Print package information for the lightweight twat-task CLI."""
    print(f"twat-task v{__version__}")


if __name__ == "__main__":
    main()
