from __future__ import annotations

import io
import os
import zipfile
from pathlib import Path

import anyio

from .._types import FileTypes


def files_from_dir(directory: str | os.PathLike[str]) -> list[FileTypes]:
    path = Path(directory)

    files: list[FileTypes] = []
    _collect_files(path, path.parent, files)
    return files


def _collect_files(directory: Path, relative_to: Path, files: list[FileTypes]) -> None:
    for path in directory.iterdir():
        if path.is_dir():
            _collect_files(path, relative_to, files)
            continue

        files.append((path.relative_to(relative_to).as_posix(), path.read_bytes()))


async def async_files_from_dir(directory: str | os.PathLike[str]) -> list[FileTypes]:
    path = anyio.Path(directory)

    files: list[FileTypes] = []
    await _async_collect_files(path, path.parent, files)
    return files


async def _async_collect_files(directory: anyio.Path, relative_to: anyio.Path, files: list[FileTypes]) -> None:
    async for path in directory.iterdir():
        if await path.is_dir():
            await _async_collect_files(path, relative_to, files)
            continue

        files.append((path.relative_to(relative_to).as_posix(), await path.read_bytes()))


def files_from_zip(zip_path: str | os.PathLike[str]) -> list[FileTypes]:
    """Read all files from a zip archive and return them as a list of file tuples.

    Each entry is returned as a ``(filename, content)`` tuple compatible with
    the ``files`` parameter accepted by :meth:`Skills.create` and similar APIs.

    Directories and macOS resource fork entries (``__MACOSX/``) are
    automatically skipped.
    """
    path = Path(zip_path)
    return _read_zip(path.read_bytes())


async def async_files_from_zip(zip_path: str | os.PathLike[str]) -> list[FileTypes]:
    """Async variant of :func:`files_from_zip`."""
    path = anyio.Path(zip_path)
    return _read_zip(await path.read_bytes())


def _read_zip(data: bytes) -> list[FileTypes]:
    files: list[FileTypes] = []
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for entry in zf.infolist():
            if entry.is_dir():
                continue
            if entry.filename.startswith("__MACOSX/"):
                continue
            files.append((entry.filename, zf.read(entry)))
    return files
