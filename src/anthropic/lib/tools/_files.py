from __future__ import annotations

from pathlib import Path

__all__ = ["read_text_exact", "write_text_exact"]


def read_text_exact(path: Path) -> str:
    """Read a UTF-8 file without newline translation."""
    return path.read_bytes().decode("utf-8")


def write_text_exact(path: Path, text: str) -> None:
    """Write a UTF-8 file without newline translation."""
    path.write_bytes(text.encode("utf-8"))
