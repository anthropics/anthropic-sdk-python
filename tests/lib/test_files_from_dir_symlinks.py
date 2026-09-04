from __future__ import annotations

import os
import pathlib

import pytest

from anthropic.lib._files import async_files_from_dir, files_from_dir


pytestmark = pytest.mark.skipif(
    os.name == "nt", reason="symlink creation is not reliably available on Windows CI"
)


def _make_tree(tmp_path: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
    root = tmp_path / "bundle"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    return root, outside


def test_files_from_dir_rejects_file_symlink_outside_root(
    tmp_path: pathlib.Path,
) -> None:
    root, outside = _make_tree(tmp_path)
    secret = outside / "secret.txt"
    secret.write_text("outside-secret")
    (root / "leak.txt").symlink_to(secret)

    with pytest.raises(ValueError, match="outside the requested root"):
        files_from_dir(root)


def test_files_from_dir_allows_symlinks_that_stay_inside_root(
    tmp_path: pathlib.Path,
) -> None:
    root, _ = _make_tree(tmp_path)
    target = root / "actual.txt"
    target.write_text("inside")
    (root / "alias.txt").symlink_to(target.name)

    files = dict(files_from_dir(root))

    assert files[f"{root.name}/actual.txt"] == b"inside"
    assert files[f"{root.name}/alias.txt"] == b"inside"


def test_files_from_dir_rejects_directory_symlink_cycle(
    tmp_path: pathlib.Path,
) -> None:
    root, _ = _make_tree(tmp_path)
    subdir = root / "subdir"
    subdir.mkdir()
    (subdir / "back").symlink_to(root, target_is_directory=True)

    with pytest.raises(ValueError, match="symlink cycle"):
        files_from_dir(root)


@pytest.mark.asyncio()
async def test_async_files_from_dir_rejects_directory_symlink_outside_root(
    tmp_path: pathlib.Path,
) -> None:
    root, outside = _make_tree(tmp_path)
    (outside / "data.txt").write_text("outside")
    (root / "external").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError, match="outside the requested root"):
        await async_files_from_dir(root)


@pytest.mark.asyncio()
async def test_async_files_from_dir_rejects_directory_symlink_cycle(
    tmp_path: pathlib.Path,
) -> None:
    root, _ = _make_tree(tmp_path)
    subdir = root / "subdir"
    subdir.mkdir()
    (subdir / "back").symlink_to(root, target_is_directory=True)

    with pytest.raises(ValueError, match="symlink cycle"):
        await async_files_from_dir(root)
