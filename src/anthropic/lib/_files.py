from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator, AsyncIterator

import anyio

from .._types import FileTypes


def _is_path_within_root(path: Path, root: Path) -> bool:
    """
    Check if a path is within root directory.
    Python 3.8 compatible alternative to Path.is_relative_to().
    """
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def files_from_dir(directory: str | os.PathLike[str]) -> list[FileTypes]:
    path = Path(directory).resolve()

    files: list[FileTypes] = []
    _collect_files(path, path.parent, files, root=path)
    return files


def _collect_files(directory: Path, relative_to: Path, files: list[FileTypes], root: Path) -> None:
    try:
        items = list(directory.iterdir())
    except (PermissionError, OSError):
        # Skip directories we can't read
        return

    for path in items:
        try:
            # Resolve symlinks and check they don't escape the root directory
            resolved_path = path.resolve()
            if not _is_path_within_root(resolved_path, root):
                continue

            if resolved_path.is_dir():
                _collect_files(resolved_path, relative_to, files, root=root)
                continue

            with open(resolved_path, 'rb') as f:
                content = f.read()
            files.append((str(path.relative_to(relative_to)), content))
        except (PermissionError, OSError):
            # Skip files/symlinks we can't read or resolve
            continue


async def async_files_from_dir(directory: str | os.PathLike[str]) -> list[FileTypes]:
    path = anyio.Path(directory)
    # Resolve to get absolute path - returns a standard Path, not anyio.Path
    resolved_root = Path(await path.resolve())

    files: list[FileTypes] = []
    await _async_collect_files(path, path.parent, files, root=resolved_root)
    return files


async def _async_collect_files(
    directory: anyio.Path, relative_to: anyio.Path, files: list[FileTypes], root: Path
) -> None:
    try:
        items = [item async for item in directory.iterdir()]
    except (PermissionError, OSError):
        # Skip directories we can't read
        return

    for path in items:
        try:
            # Resolve symlinks - this returns a standard Path, not anyio.Path
            resolved_path = Path(await path.resolve())

            # Check containment using standard Path methods (no await needed)
            if not _is_path_within_root(resolved_path, root):
                continue

            if resolved_path.is_dir():
                # Convert back to anyio.Path for recursive call
                await _async_collect_files(anyio.Path(resolved_path), relative_to, files, root=root)
                continue

            async with await anyio.open_file(resolved_path, 'rb') as f:
                content = await f.read()
            files.append((str(path.relative_to(relative_to)), content))
        except (PermissionError, OSError):
            # Skip files/symlinks we can't read or resolve
            continue


def files_from_dir_iter(directory: str | os.PathLike[str]) -> Iterator[FileTypes]:
    """
    Memory-efficient streaming version of files_from_dir.
    Yields files one at a time instead of loading all into memory.
    """
    path = Path(directory).resolve()
    yield from _collect_files_iter(path, path.parent, root=path)


def _collect_files_iter(directory: Path, relative_to: Path, root: Path) -> Iterator[FileTypes]:
    try:
        items = list(directory.iterdir())
    except (PermissionError, OSError):
        # Skip directories we can't read
        return

    for path in items:
        try:
            # Resolve symlinks and check they don't escape the root directory
            resolved_path = path.resolve()
            if not _is_path_within_root(resolved_path, root):
                continue

            if resolved_path.is_dir():
                yield from _collect_files_iter(resolved_path, relative_to, root=root)
                continue

            with open(resolved_path, 'rb') as f:
                content = f.read()
            yield (str(path.relative_to(relative_to)), content)
        except (PermissionError, OSError):
            # Skip files/symlinks we can't read or resolve
            continue


async def async_files_from_dir_iter(directory: str | os.PathLike[str]) -> AsyncIterator[FileTypes]:
    """
    Memory-efficient streaming version of async_files_from_dir.
    Yields files one at a time instead of loading all into memory.
    """
    path = anyio.Path(directory)
    resolved_root = Path(await path.resolve())
    async for file in _async_collect_files_iter(path, path.parent, root=resolved_root):
        yield file


async def _async_collect_files_iter(
    directory: anyio.Path, relative_to: anyio.Path, root: Path
) -> AsyncIterator[FileTypes]:
    try:
        items = [item async for item in directory.iterdir()]
    except (PermissionError, OSError):
        # Skip directories we can't read
        return

    for path in items:
        try:
            # Resolve symlinks - returns standard Path
            resolved_path = Path(await path.resolve())

            # Check containment (no await - it's a standard Path method)
            if not _is_path_within_root(resolved_path, root):
                continue

            if resolved_path.is_dir():
                async for file in _async_collect_files_iter(anyio.Path(resolved_path), relative_to, root=root):
                    yield file
                continue

            async with await anyio.open_file(resolved_path, 'rb') as f:
                content = await f.read()
            yield (str(path.relative_to(relative_to)), content)
        except (PermissionError, OSError):
            # Skip files/symlinks we can't read or resolve
            continue
