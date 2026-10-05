from pathlib import Path

import pytest

from anthropic.lib import files_from_dir, async_files_from_dir


def _create_directory_tree_with_symlink(root: Path, target: Path) -> None:
    (root / "included.txt").write_text("included")
    (root / "linked-directory").symlink_to(target, target_is_directory=True)


def test_files_from_dir_does_not_follow_directory_symlinks(tmp_path: Path) -> None:
    root = tmp_path / "upload"
    root.mkdir()
    _create_directory_tree_with_symlink(root, root)

    assert files_from_dir(root) == [("upload/included.txt", b"included")]


@pytest.mark.asyncio
async def test_async_files_from_dir_does_not_follow_directory_symlinks(tmp_path: Path) -> None:
    root = tmp_path / "upload"
    root.mkdir()
    _create_directory_tree_with_symlink(root, root)

    assert await async_files_from_dir(root) == [("upload/included.txt", b"included")]
