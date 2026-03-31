from __future__ import annotations

import os
import tempfile
from typing import Iterator
from pathlib import Path

import pytest

from anthropic.types.beta import (
    BetaMemoryTool20250818ViewCommand,
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
)
from anthropic.lib.tools._beta_functions import ToolError
from anthropic.lib.tools._beta_builtin_memory_tool import (
    BetaLocalFilesystemMemoryTool,
    BetaAsyncLocalFilesystemMemoryTool,
)


@pytest.fixture
def temp_directory() -> Iterator[str]:
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def sync_local_filesystem_tool(temp_directory: str) -> BetaLocalFilesystemMemoryTool:
    return BetaLocalFilesystemMemoryTool(base_path=temp_directory)


@pytest.fixture
def async_local_filesystem_tool(temp_directory: str) -> BetaAsyncLocalFilesystemMemoryTool:
    return BetaAsyncLocalFilesystemMemoryTool(base_path=temp_directory)


def get_directory_snapshot(base_path: str) -> dict[str, str]:
    """Get a snapshot of directory contents with relative paths."""
    snapshot: dict[str, str] = {}
    for root, _, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_path)
            with open(full_path, "r") as f:
                snapshot[rel_path] = f.read()
    return snapshot


class TestBetaLocalFilesystemMemoryTool:
    def test_create(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        result = sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Hello, World!",
                path="/memories/test_file.txt",
            )
        )
        assert result == "File created successfully at: /memories/test_file.txt"
        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/test_file.txt": "Hello, World!"}

    def test_create_nested_directories(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        result = sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Nested file",
                path="/memories/deep/nested/file.txt",
            )
        )
        assert result == "File created successfully at: /memories/deep/nested/file.txt"
        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/deep/nested/file.txt": "Nested file"}

    def test_create_error_if_file_already_exists(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Original",
                path="/memories/existing.txt",
            )
        )

        with pytest.raises(ToolError, match="File /memories/existing.txt already exists"):
            sync_local_filesystem_tool.create(
                BetaMemoryTool20250818CreateCommand(
                    command="create",
                    file_text="New",
                    path="/memories/existing.txt",
                )
            )

    def test_view_file(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Line 1\nLine 2\nLine 3",
                path="/memories/view_test.txt",
            )
        )

        result = sync_local_filesystem_tool.view(
            BetaMemoryTool20250818ViewCommand(command="view", path="/memories/view_test.txt")
        )
        assert (
            result
            == "Here's the content of /memories/view_test.txt with line numbers:\n     1\tLine 1\n     2\tLine 2\n     3\tLine 3"
        )

    def test_view_directory(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="File 1",
                path="/memories/dir/file1.txt",
            )
        )

        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="File 2",
                path="/memories/dir/file2.txt",
            )
        )

        result = sync_local_filesystem_tool.view(
            BetaMemoryTool20250818ViewCommand(command="view", path="/memories/dir")
        )

        assert "Here're the files and directories up to 2 levels deep in /memories/dir" in result
        assert "/memories/dir" in result
        assert "/memories/dir/file1.txt" in result
        assert "/memories/dir/file2.txt" in result

    def test_view_file_with_range(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5",
                path="/memories/range_test.txt",
            )
        )

        result = sync_local_filesystem_tool.view(
            BetaMemoryTool20250818ViewCommand(command="view", path="/memories/range_test.txt", view_range=[2, 4])
        )

        assert (
            result
            == "Here's the content of /memories/range_test.txt with line numbers:\n     2\tLine 2\n     3\tLine 3\n     4\tLine 4"
        )

    def test_view_error_for_non_existent_file(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        with pytest.raises(
            ToolError, match="The path /memories/nonexistent.txt does not exist. Please provide a valid path."
        ):
            sync_local_filesystem_tool.view(
                BetaMemoryTool20250818ViewCommand(command="view", path="/memories/nonexistent.txt")
            )

    def test_view_error_for_files_with_too_many_lines(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        too_many_lines = "\n".join(["line"] * 1000000)
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text=too_many_lines,
                path="/memories/huge.txt",
            )
        )

        with pytest.raises(ToolError, match=r"exceeds maximum line limit of 999,999 lines"):
            sync_local_filesystem_tool.view(
                BetaMemoryTool20250818ViewCommand(command="view", path="/memories/huge.txt")
            )

    def test_str_replace(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Line 1\nOld Text\nLine 3",
                path="/memories/replace_test.txt",
            )
        )

        result = sync_local_filesystem_tool.str_replace(
            BetaMemoryTool20250818StrReplaceCommand(
                command="str_replace",
                path="/memories/replace_test.txt",
                old_str="Old Text",
                new_str="New Text",
            )
        )

        assert (
            result
            == "The memory file has been edited. Here is the snippet showing the change (with line numbers):\n     1\tLine 1\n     2\tNew Text\n     3\tLine 3"
        )

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/replace_test.txt": "Line 1\nNew Text\nLine 3"}

    def test_str_replace_error_when_string_not_found(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Hello, World!",
                path="/memories/replace_test.txt",
            )
        )

        with pytest.raises(
            ToolError,
            match="No replacement was performed, old_str `NotFound` did not appear verbatim in /memories/replace_test.txt.",
        ):
            sync_local_filesystem_tool.str_replace(
                BetaMemoryTool20250818StrReplaceCommand(
                    command="str_replace",
                    path="/memories/replace_test.txt",
                    old_str="NotFound",
                    new_str="Python",
                )
            )

    def test_str_replace_error_when_string_appears_multiple_times(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Hello\nMiddle\nHello",
                path="/memories/replace_test.txt",
            )
        )

        with pytest.raises(
            ToolError,
            match=r"No replacement was performed\. Multiple occurrences of old_str `Hello` in lines: 1, 3\. Please ensure it is unique",
        ):
            sync_local_filesystem_tool.str_replace(
                BetaMemoryTool20250818StrReplaceCommand(
                    command="str_replace",
                    path="/memories/replace_test.txt",
                    old_str="Hello",
                    new_str="Hi",
                )
            )

    def test_str_replace_error_for_non_existent_file(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(
            ToolError, match="The path /memories/nonexistent.txt does not exist. Please provide a valid path."
        ):
            sync_local_filesystem_tool.str_replace(
                BetaMemoryTool20250818StrReplaceCommand(
                    command="str_replace",
                    path="/memories/nonexistent.txt",
                    old_str="old",
                    new_str="new",
                )
            )

    def test_insert(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        result = sync_local_filesystem_tool.insert(
            BetaMemoryTool20250818InsertCommand(
                command="insert", path="/memories/insert_test.txt", insert_line=1, insert_text="Inserted Line"
            )
        )
        assert result == "The file /memories/insert_test.txt has been edited."

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/insert_test.txt": "Line 1\nInserted Line\nLine 2\n"}

    def test_insert_at_beginning_of_file(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        sync_local_filesystem_tool.insert(
            BetaMemoryTool20250818InsertCommand(
                command="insert", path="/memories/insert_test.txt", insert_line=0, insert_text="First Line"
            )
        )

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/insert_test.txt": "First Line\nLine 1\nLine 2\n"}

    def test_insert_at_end_of_file(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        sync_local_filesystem_tool.insert(
            BetaMemoryTool20250818InsertCommand(
                command="insert", path="/memories/insert_test.txt", insert_line=2, insert_text="Last Line"
            )
        )

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/insert_test.txt": "Line 1\nLine 2\nLast Line\n"}

    def test_insert_error_for_non_existent_file(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(
            ToolError, match="The path /memories/nonexistent.txt does not exist. Please provide a valid path."
        ):
            sync_local_filesystem_tool.insert(
                BetaMemoryTool20250818InsertCommand(
                    command="insert", path="/memories/nonexistent.txt", insert_line=0, insert_text="text"
                )
            )

    def test_insert_error_for_invalid_insert_line(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        with pytest.raises(
            ToolError,
            match=r"Invalid `insert_line` parameter: 10. It should be within the range \[0, 2\]",
        ):
            sync_local_filesystem_tool.insert(
                BetaMemoryTool20250818InsertCommand(
                    command="insert", path="/memories/insert_test.txt", insert_line=10, insert_text="text"
                )
            )

    def test_delete(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="To be deleted", path="/memories/delete_me.txt"
            )
        )

        result = sync_local_filesystem_tool.delete(
            BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories/delete_me.txt")
        )
        assert result == "Successfully deleted /memories/delete_me.txt"

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {}

    def test_delete_directory(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="Content", path="/memories/subdir/file.txt")
        )

        result = sync_local_filesystem_tool.delete(
            BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories/subdir")
        )
        assert result == "Successfully deleted /memories/subdir"

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {}

    def test_delete_error_when_file_not_found(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        with pytest.raises(ToolError, match="The path /memories/nonexistent.txt does not exist"):
            sync_local_filesystem_tool.delete(
                BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories/nonexistent.txt")
            )

    def test_delete_not_allow_deleting_memories_directory(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="Cannot delete the /memories directory itself"):
            sync_local_filesystem_tool.delete(BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories"))

    def test_rename(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Original content", path="/memories/old_name.txt"
            )
        )

        result = sync_local_filesystem_tool.rename(
            BetaMemoryTool20250818RenameCommand(
                command="rename", old_path="/memories/old_name.txt", new_path="/memories/new_name.txt"
            )
        )
        assert result == "Successfully renamed /memories/old_name.txt to /memories/new_name.txt"

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/new_name.txt": "Original content"}

    def test_rename_to_nested_path(self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="Content", path="/memories/file.txt")
        )

        result = sync_local_filesystem_tool.rename(
            BetaMemoryTool20250818RenameCommand(
                command="rename", old_path="/memories/file.txt", new_path="/memories/nested/dir/file.txt"
            )
        )
        assert result == "Successfully renamed /memories/file.txt to /memories/nested/dir/file.txt"

        dir_snapshot = get_directory_snapshot(str(sync_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/nested/dir/file.txt": "Content"}

    def test_rename_error_when_source_not_found(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="The path /memories/nonexistent.txt does not exist"):
            sync_local_filesystem_tool.rename(
                BetaMemoryTool20250818RenameCommand(
                    command="rename", old_path="/memories/nonexistent.txt", new_path="/memories/new.txt"
                )
            )

    def test_rename_error_when_destination_exists(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="File 1", path="/memories/file1.txt")
        )

        sync_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="File 2", path="/memories/file2.txt")
        )

        with pytest.raises(ToolError, match="The destination /memories/file2.txt already exists"):
            sync_local_filesystem_tool.rename(
                BetaMemoryTool20250818RenameCommand(
                    command="rename", old_path="/memories/file1.txt", new_path="/memories/file2.txt"
                )
            )

    def test_path_validation_reject_paths_not_starting_with_memories(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="Path must start with /memories"):
            sync_local_filesystem_tool.create(
                BetaMemoryTool20250818CreateCommand(command="create", file_text="Invalid", path="/invalid/path.txt")
            )

    def test_path_validation_reject_paths_trying_to_escape_memories(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="Path /memories/../../../etc/passwd would escape /memories directory"):
            sync_local_filesystem_tool.create(
                BetaMemoryTool20250818CreateCommand(
                    command="create", file_text="Escape attempt", path="/memories/../../../etc/passwd"
                )
            )

    def test_symlink_validation_reject_symlink_pointing_outside_memories(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            Path(outside_dir, "secret.txt").write_text("sensitive data", encoding="utf-8")

            memories_path = sync_local_filesystem_tool.memory_root
            symlink_path = memories_path / "escape_link"

            os.symlink(outside_dir, symlink_path, target_is_directory=True)

            with pytest.raises(ToolError, match="Path .* would escape /memories directory"):
                sync_local_filesystem_tool.view(
                    BetaMemoryTool20250818ViewCommand(command="view", path="/memories/escape_link/secret.txt")
                )

    def test_symlink_validation_reject_creating_files_through_symlink_pointing_outside(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            memories_path = sync_local_filesystem_tool.memory_root
            symlink_path = memories_path / "bad_link"

            os.symlink(outside_dir, symlink_path, target_is_directory=True)

            with pytest.raises(ToolError, match="Path .* would escape /memories directory"):
                sync_local_filesystem_tool.create(
                    BetaMemoryTool20250818CreateCommand(
                        command="create", file_text="malicious content", path="/memories/bad_link/hacked.txt"
                    )
                )

    def test_symlink_validation_reject_parent_directory_that_is_symlink_pointing_outside(
        self, sync_local_filesystem_tool: BetaLocalFilesystemMemoryTool
    ) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            memories_path = sync_local_filesystem_tool.memory_root
            symlink_dir_path = memories_path / "subdir"

            os.symlink(outside_dir, symlink_dir_path, target_is_directory=True)

            with pytest.raises(ToolError, match="Path .* would escape /memories directory"):
                sync_local_filesystem_tool.create(
                    BetaMemoryTool20250818CreateCommand(
                        command="create", file_text="content", path="/memories/subdir/nested/file.txt"
                    )
                )


class TestBetaAsyncLocalFilesystemMemoryTool:
    async def test_create(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        result = await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Hello, World!",
                path="/memories/test_file.txt",
            )
        )
        assert result == "File created successfully at: /memories/test_file.txt"
        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/test_file.txt": "Hello, World!"}

    async def test_create_nested_directories(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        result = await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Nested file",
                path="/memories/deep/nested/file.txt",
            )
        )
        assert result == "File created successfully at: /memories/deep/nested/file.txt"
        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/deep/nested/file.txt": "Nested file"}

    async def test_create_error_if_file_already_exists(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Original",
                path="/memories/existing.txt",
            )
        )

        with pytest.raises(ToolError, match="File /memories/existing.txt already exists"):
            await async_local_filesystem_tool.create(
                BetaMemoryTool20250818CreateCommand(
                    command="create",
                    file_text="New",
                    path="/memories/existing.txt",
                )
            )

    async def test_view_file(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Line 1\nLine 2\nLine 3",
                path="/memories/view_test.txt",
            )
        )

        result = await async_local_filesystem_tool.view(
            BetaMemoryTool20250818ViewCommand(command="view", path="/memories/view_test.txt")
        )
        assert (
            result
            == "Here's the content of /memories/view_test.txt with line numbers:\n     1\tLine 1\n     2\tLine 2\n     3\tLine 3"
        )

    async def test_view_directory(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="File 1",
                path="/memories/dir/file1.txt",
            )
        )

        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="File 2",
                path="/memories/dir/file2.txt",
            )
        )

        result = await async_local_filesystem_tool.view(
            BetaMemoryTool20250818ViewCommand(command="view", path="/memories/dir")
        )

        assert "Here're the files and directories up to 2 levels deep in /memories/dir" in result
        assert "/memories/dir" in result
        assert "/memories/dir/file1.txt" in result
        assert "/memories/dir/file2.txt" in result

    async def test_view_file_with_range(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5",
                path="/memories/range_test.txt",
            )
        )

        result = await async_local_filesystem_tool.view(
            BetaMemoryTool20250818ViewCommand(command="view", path="/memories/range_test.txt", view_range=[2, 4])
        )

        assert (
            result
            == "Here's the content of /memories/range_test.txt with line numbers:\n     2\tLine 2\n     3\tLine 3\n     4\tLine 4"
        )

    async def test_view_error_for_non_existent_file(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(
            ToolError, match="The path /memories/nonexistent.txt does not exist. Please provide a valid path."
        ):
            await async_local_filesystem_tool.view(
                BetaMemoryTool20250818ViewCommand(command="view", path="/memories/nonexistent.txt")
            )

    async def test_view_error_for_files_with_too_many_lines(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        too_many_lines = "\n".join(["line"] * 1000000)
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text=too_many_lines,
                path="/memories/huge.txt",
            )
        )

        with pytest.raises(ToolError, match=r"exceeds maximum line limit of 999,999 lines"):
            await async_local_filesystem_tool.view(
                BetaMemoryTool20250818ViewCommand(command="view", path="/memories/huge.txt")
            )

    async def test_str_replace(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Line 1\nOld Text\nLine 3",
                path="/memories/replace_test.txt",
            )
        )

        result = await async_local_filesystem_tool.str_replace(
            BetaMemoryTool20250818StrReplaceCommand(
                command="str_replace",
                path="/memories/replace_test.txt",
                old_str="Old Text",
                new_str="New Text",
            )
        )

        assert (
            result
            == "The memory file has been edited. Here is the snippet showing the change (with line numbers):\n     1\tLine 1\n     2\tNew Text\n     3\tLine 3"
        )

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/replace_test.txt": "Line 1\nNew Text\nLine 3"}

    async def test_str_replace_error_when_string_not_found(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Hello, World!",
                path="/memories/replace_test.txt",
            )
        )

        with pytest.raises(
            ToolError,
            match="No replacement was performed, old_str `NotFound` did not appear verbatim in /memories/replace_test.txt.",
        ):
            await async_local_filesystem_tool.str_replace(
                BetaMemoryTool20250818StrReplaceCommand(
                    command="str_replace",
                    path="/memories/replace_test.txt",
                    old_str="NotFound",
                    new_str="Python",
                )
            )

    async def test_str_replace_error_when_string_appears_multiple_times(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create",
                file_text="Hello\nMiddle\nHello",
                path="/memories/replace_test.txt",
            )
        )

        with pytest.raises(
            ToolError,
            match=r"No replacement was performed\. Multiple occurrences of old_str `Hello` in lines: 1, 3\. Please ensure it is unique",
        ):
            await async_local_filesystem_tool.str_replace(
                BetaMemoryTool20250818StrReplaceCommand(
                    command="str_replace",
                    path="/memories/replace_test.txt",
                    old_str="Hello",
                    new_str="Hi",
                )
            )

    async def test_str_replace_error_for_non_existent_file(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(
            ToolError, match="The path /memories/nonexistent.txt does not exist. Please provide a valid path."
        ):
            await async_local_filesystem_tool.str_replace(
                BetaMemoryTool20250818StrReplaceCommand(
                    command="str_replace",
                    path="/memories/nonexistent.txt",
                    old_str="old",
                    new_str="new",
                )
            )

    async def test_insert(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        result = await async_local_filesystem_tool.insert(
            BetaMemoryTool20250818InsertCommand(
                command="insert", path="/memories/insert_test.txt", insert_line=1, insert_text="Inserted Line"
            )
        )
        assert result == "The file /memories/insert_test.txt has been edited."

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/insert_test.txt": "Line 1\nInserted Line\nLine 2\n"}

    async def test_insert_at_beginning_of_file(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        await async_local_filesystem_tool.insert(
            BetaMemoryTool20250818InsertCommand(
                command="insert", path="/memories/insert_test.txt", insert_line=0, insert_text="First Line"
            )
        )

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/insert_test.txt": "First Line\nLine 1\nLine 2\n"}

    async def test_insert_at_end_of_file(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        await async_local_filesystem_tool.insert(
            BetaMemoryTool20250818InsertCommand(
                command="insert", path="/memories/insert_test.txt", insert_line=2, insert_text="Last Line"
            )
        )

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/insert_test.txt": "Line 1\nLine 2\nLast Line\n"}

    async def test_insert_error_for_non_existent_file(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(
            ToolError, match="The path /memories/nonexistent.txt does not exist. Please provide a valid path."
        ):
            await async_local_filesystem_tool.insert(
                BetaMemoryTool20250818InsertCommand(
                    command="insert", path="/memories/nonexistent.txt", insert_line=0, insert_text="text"
                )
            )

    async def test_insert_error_for_invalid_insert_line(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Line 1\nLine 2", path="/memories/insert_test.txt"
            )
        )

        with pytest.raises(
            ToolError,
            match=r"Invalid `insert_line` parameter: 10\. It should be within the range \[0, 2\]",
        ):
            await async_local_filesystem_tool.insert(
                BetaMemoryTool20250818InsertCommand(
                    command="insert", path="/memories/insert_test.txt", insert_line=10, insert_text="text"
                )
            )

    async def test_delete(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="To be deleted", path="/memories/delete_me.txt"
            )
        )

        result = await async_local_filesystem_tool.delete(
            BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories/delete_me.txt")
        )
        assert result == "Successfully deleted /memories/delete_me.txt"

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {}

    async def test_delete_directory(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="Content", path="/memories/subdir/file.txt")
        )

        result = await async_local_filesystem_tool.delete(
            BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories/subdir")
        )
        assert result == "Successfully deleted /memories/subdir"

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {}

    async def test_delete_error_when_file_not_found(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="The path /memories/nonexistent.txt does not exist"):
            await async_local_filesystem_tool.delete(
                BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories/nonexistent.txt")
            )

    async def test_delete_not_allow_deleting_memories_directory(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="Cannot delete the /memories directory itself"):
            await async_local_filesystem_tool.delete(
                BetaMemoryTool20250818DeleteCommand(command="delete", path="/memories")
            )

    async def test_rename(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(
                command="create", file_text="Original content", path="/memories/old_name.txt"
            )
        )

        result = await async_local_filesystem_tool.rename(
            BetaMemoryTool20250818RenameCommand(
                command="rename", old_path="/memories/old_name.txt", new_path="/memories/new_name.txt"
            )
        )
        assert result == "Successfully renamed /memories/old_name.txt to /memories/new_name.txt"

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/new_name.txt": "Original content"}

    async def test_rename_to_nested_path(self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="Content", path="/memories/file.txt")
        )

        result = await async_local_filesystem_tool.rename(
            BetaMemoryTool20250818RenameCommand(
                command="rename", old_path="/memories/file.txt", new_path="/memories/nested/dir/file.txt"
            )
        )
        assert result == "Successfully renamed /memories/file.txt to /memories/nested/dir/file.txt"

        dir_snapshot = get_directory_snapshot(str(async_local_filesystem_tool.base_path))
        assert dir_snapshot == {"memories/nested/dir/file.txt": "Content"}

    async def test_rename_error_when_source_not_found(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="The path /memories/nonexistent.txt does not exist"):
            await async_local_filesystem_tool.rename(
                BetaMemoryTool20250818RenameCommand(
                    command="rename", old_path="/memories/nonexistent.txt", new_path="/memories/new.txt"
                )
            )

    async def test_rename_error_when_destination_exists(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="File 1", path="/memories/file1.txt")
        )

        await async_local_filesystem_tool.create(
            BetaMemoryTool20250818CreateCommand(command="create", file_text="File 2", path="/memories/file2.txt")
        )

        with pytest.raises(ToolError, match="The destination /memories/file2.txt already exists"):
            await async_local_filesystem_tool.rename(
                BetaMemoryTool20250818RenameCommand(
                    command="rename", old_path="/memories/file1.txt", new_path="/memories/file2.txt"
                )
            )

    async def test_path_validation_reject_paths_not_starting_with_memories(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="Path must start with /memories"):
            await async_local_filesystem_tool.create(
                BetaMemoryTool20250818CreateCommand(command="create", file_text="Invalid", path="/invalid/path.txt")
            )

    async def test_path_validation_reject_paths_trying_to_escape_memories(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with pytest.raises(ToolError, match="Path /memories/../../../etc/passwd would escape /memories directory"):
            await async_local_filesystem_tool.create(
                BetaMemoryTool20250818CreateCommand(
                    command="create", file_text="Escape attempt", path="/memories/../../../etc/passwd"
                )
            )

    async def test_validate_path_returns_resolved_path_not_symlink_target(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        """_validate_path must return the resolved path so that subsequent file
        operations hit the real location, not the (potentially swappable) symlink.

        Without this fix, an attacker could:
        1. Create /memories/link -> /memories/legit  (passes validation)
        2. Swap /memories/link -> /etc between validation and the file operation
        3. The file operation would follow the new symlink target
        """
        memories_path = Path(str(async_local_filesystem_tool.memory_root))
        memories_path.mkdir(parents=True, exist_ok=True)

        # Create a real directory inside memories and a symlink pointing to it
        legit_dir = memories_path / "legit"
        legit_dir.mkdir()
        (legit_dir / "file.txt").write_text("content", encoding="utf-8")

        link_path = memories_path / "link"
        os.symlink(legit_dir, link_path, target_is_directory=True)

        # _validate_path should return the resolved real path, not the symlink path
        result = await async_local_filesystem_tool._validate_path("/memories/link/file.txt")
        result_str = str(result)

        # The returned path should point to the resolved location (under legit/),
        # not through the symlink
        assert "link" not in result_str, (
            f"_validate_path returned unresolved symlink path: {result_str}"
        )
        assert str(legit_dir.resolve()) in result_str

    async def test_symlink_validation_reject_symlink_pointing_outside_memories(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            Path(outside_dir, "secret.txt").write_text("sensitive data", encoding="utf-8")

            memories_path = Path(str(async_local_filesystem_tool.memory_root))
            memories_path.mkdir(parents=True, exist_ok=True)
            symlink_path = memories_path / "escape_link"

            os.symlink(outside_dir, symlink_path, target_is_directory=True)

            with pytest.raises(ToolError, match="Path .* would escape /memories directory"):
                await async_local_filesystem_tool.view(
                    BetaMemoryTool20250818ViewCommand(command="view", path="/memories/escape_link/secret.txt")
                )

    async def test_symlink_validation_reject_creating_files_through_symlink_pointing_outside(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            memories_path = Path(str(async_local_filesystem_tool.memory_root))
            memories_path.mkdir(parents=True, exist_ok=True)
            symlink_path = memories_path / "bad_link"

            os.symlink(outside_dir, symlink_path, target_is_directory=True)

            with pytest.raises(ToolError, match="Path .* would escape /memories directory"):
                await async_local_filesystem_tool.create(
                    BetaMemoryTool20250818CreateCommand(
                        command="create", file_text="malicious content", path="/memories/bad_link/hacked.txt"
                    )
                )

    async def test_symlink_validation_reject_parent_directory_that_is_symlink_pointing_outside(
        self, async_local_filesystem_tool: BetaAsyncLocalFilesystemMemoryTool
    ) -> None:
        with tempfile.TemporaryDirectory() as outside_dir:
            memories_path = Path(str(async_local_filesystem_tool.memory_root))
            memories_path.mkdir(parents=True, exist_ok=True)
            symlink_dir_path = memories_path / "subdir"

            os.symlink(outside_dir, symlink_dir_path, target_is_directory=True)

            with pytest.raises(ToolError, match="Path .* would escape /memories directory"):
                await async_local_filesystem_tool.create(
                    BetaMemoryTool20250818CreateCommand(
                        command="create", file_text="content", path="/memories/subdir/nested/file.txt"
                    )
                )
