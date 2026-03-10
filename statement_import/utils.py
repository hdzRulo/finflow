"""Utility helpers for parser framework scaffolding."""

from pathlib import Path


def detect_file_type(path: Path) -> str:
    """Infer a simple file type from suffix for routing decisions."""
    return path.suffix.lower().strip(".")
