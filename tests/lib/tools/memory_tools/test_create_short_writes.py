from __future__ import annotations

import os
from pathlib import Path

import pytest

from anthropic.lib.tools._beta_builtin_memory_tool import (
    BetaAsyncLocalFilesystemMemoryTool,
    BetaLocalFilesystemMemoryTool,
)
from anthropic.types.beta import BetaMemoryTool20250818CreateCommand


def _force_short_writes(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    real_write = os.write
    write_sizes: list[int] = []

    def short_write(fd: int, data: bytes) -> int:
        chunk_size = min(3, len(data))
        written = real_write(fd, data[:chunk_size])
        write_sizes.append(written)
        return written

    monkeypatch.setattr(os, "write", short_write)
    return write_sizes


def test_create_retries_short_writes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    write_sizes = _force_short_writes(monkeypatch)
    tool = BetaLocalFilesystemMemoryTool(base_path=str(tmp_path))
    text = "prefix-☃-suffix"

    result = tool.create(
        BetaMemoryTool20250818CreateCommand(
            command="create",
            file_text=text,
            path="/memories/short-write.txt",
        )
    )

    assert result == "File created successfully at: /memories/short-write.txt"
    assert (tmp_path / "memories" / "short-write.txt").read_text(encoding="utf-8") == text
    assert len(write_sizes) > 1


@pytest.mark.asyncio
async def test_async_create_retries_short_writes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    write_sizes = _force_short_writes(monkeypatch)
    tool = BetaAsyncLocalFilesystemMemoryTool(base_path=str(tmp_path))
    text = "prefix-☃-suffix"

    result = await tool.create(
        BetaMemoryTool20250818CreateCommand(
            command="create",
            file_text=text,
            path="/memories/short-write.txt",
        )
    )

    assert result == "File created successfully at: /memories/short-write.txt"
    assert (tmp_path / "memories" / "short-write.txt").read_text(encoding="utf-8") == text
    assert len(write_sizes) > 1
