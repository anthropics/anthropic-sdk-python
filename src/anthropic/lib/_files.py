from __future__ import annotations

import os
from pathlib import Path

import anyio

from .._types import FileTypes


_DirectoryKey = tuple[int, int]


def _resolve_within_root(path: Path, root: Path) -> Path:
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as err:
        raise ValueError(
            "Refusing to follow directory-upload entry outside the requested root: "
            f"{path} -> {resolved}"
        ) from err
    return resolved


def files_from_dir(directory: str | os.PathLike[str]) -> list[FileTypes]:
    path = Path(directory)
    root = path.resolve(strict=True)

    files: list[FileTypes] = []
    _collect_files(path, path.parent, root, files, set())
    return files


def _collect_files(
    directory: Path,
    relative_to: Path,
    root: Path,
    files: list[FileTypes],
    active_directories: set[_DirectoryKey],
) -> None:
    resolved_directory = _resolve_within_root(directory, root)
    directory_stat = resolved_directory.stat()
    directory_key = (directory_stat.st_dev, directory_stat.st_ino)
    if directory_key in active_directories:
        raise ValueError(
            f"Refusing to follow a directory-upload symlink cycle at {directory}"
        )

    active_directories.add(directory_key)
    try:
        for path in directory.iterdir():
            resolved = _resolve_within_root(path, root)
            if resolved.is_dir():
                _collect_files(path, relative_to, root, files, active_directories)
                continue

            files.append((path.relative_to(relative_to).as_posix(), resolved.read_bytes()))
    finally:
        active_directories.remove(directory_key)


async def async_files_from_dir(directory: str | os.PathLike[str]) -> list[FileTypes]:
    path = anyio.Path(directory)
    root = await path.resolve(strict=True)

    files: list[FileTypes] = []
    await _async_collect_files(path, path.parent, root, files, set())
    return files


async def _async_resolve_within_root(path: anyio.Path, root: anyio.Path) -> anyio.Path:
    resolved = await path.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as err:
        raise ValueError(
            "Refusing to follow directory-upload entry outside the requested root: "
            f"{path} -> {resolved}"
        ) from err
    return resolved


async def _async_collect_files(
    directory: anyio.Path,
    relative_to: anyio.Path,
    root: anyio.Path,
    files: list[FileTypes],
    active_directories: set[_DirectoryKey],
) -> None:
    resolved_directory = await _async_resolve_within_root(directory, root)
    directory_stat = await resolved_directory.stat()
    directory_key = (directory_stat.st_dev, directory_stat.st_ino)
    if directory_key in active_directories:
        raise ValueError(
            f"Refusing to follow a directory-upload symlink cycle at {directory}"
        )

    active_directories.add(directory_key)
    try:
        async for path in directory.iterdir():
            resolved = await _async_resolve_within_root(path, root)
            if await resolved.is_dir():
                await _async_collect_files(path, relative_to, root, files, active_directories)
                continue

            files.append((path.relative_to(relative_to).as_posix(), await resolved.read_bytes()))
    finally:
        active_directories.remove(directory_key)
