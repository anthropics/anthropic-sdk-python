from __future__ import annotations

import sys
from pathlib import Path

from ._beta_functions import ToolError

__all__ = ["READ_STREAM_CHUNK_BYTES", "LineRangeCollector", "read_line_range", "read_text_exact", "write_text_exact"]

READ_STREAM_CHUNK_BYTES = 64 * 1024


def read_text_exact(path: Path) -> str:
    """Read a UTF-8 file without newline translation."""
    return path.read_bytes().decode("utf-8")


def write_text_exact(path: Path, text: str) -> None:
    """Write a UTF-8 file without newline translation."""
    path.write_bytes(text.encode("utf-8"))


def read_line_range(path: Path, file_path: str, start_line: int, end_line: int, limit: int) -> str:
    """Return lines ``[start_line, end_line]`` of ``path``, capping the selected bytes at ``limit``."""
    lines = LineRangeCollector(file_path=file_path, start_line=start_line, end_line=end_line, limit=limit)
    if lines.range_is_empty():
        return ""
    with path.open("rb") as f:
        while chunk := f.read(READ_STREAM_CHUNK_BYTES):
            lines.collect_from(chunk)
            if lines.range_is_collected():
                break
    return lines.text()


class LineRangeCollector:
    """Collects the bytes of lines ``[start_line, end_line]`` from consecutive file chunks, capped at ``limit``."""

    def __init__(self, *, file_path: str, start_line: int, end_line: int, limit: int) -> None:
        self._file_path = file_path
        self._start_line = start_line
        self._end_line = end_line
        self._start = max(0, start_line - 1)
        self._end = end_line if end_line > 0 else sys.maxsize
        self._limit = limit
        self._line = 0
        self._collected = bytearray()

    def range_is_empty(self) -> bool:
        return self._end <= self._start

    def range_is_collected(self) -> bool:
        return self._line >= self._end

    def collect_from(self, chunk: bytes) -> None:
        line_start = 0
        while line_start < len(chunk) and not self.range_is_collected():
            newline = chunk.find(b"\n", line_start)
            line_end = len(chunk) if newline < 0 else newline
            if self._line >= self._start:
                self._collect(chunk[line_start:line_end], newline_terminated=newline >= 0)
            if newline < 0:
                break
            self._line += 1
            line_start = newline + 1

    def _collect(self, line_bytes: bytes, *, newline_terminated: bool) -> None:
        self._collected += line_bytes
        if newline_terminated and self._line + 1 < self._end:
            self._collected += b"\n"
        if len(self._collected) > self._limit:
            raise self._over_limit_error()

    def _over_limit_error(self) -> ToolError:
        if self._end - self._start == 1:
            return ToolError(
                f"read: line {self._start + 1} of {self._file_path} alone exceeds {self._limit}-byte limit. "
                "The read tool cannot return part of a line, so view_range cannot narrow this further."
            )
        return ToolError(
            f"read: view_range [{self._start_line}, {self._end_line}] of {self._file_path} exceeds {self._limit}-byte limit. "
            "Narrow the view_range to read a smaller portion."
        )

    def text(self) -> str:
        return self._collected.decode("utf-8")
