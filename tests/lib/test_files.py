from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest

from anthropic.lib import files_from_zip, async_files_from_zip


def _make_zip(tmp_path: Path, entries: dict[str, bytes]) -> Path:
    """Helper to create a zip file with the given entries."""
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for name, content in entries.items():
            zf.writestr(name, content)
    return zip_path


class TestFilesFromZip:
    def test_basic(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path,
            {
                "my_skill/SKILL.md": b"# My Skill",
                "my_skill/analyze.py": b"print('hello')",
            },
        )
        files = files_from_zip(zip_path)
        names = {f[0] for f in files}
        assert names == {"my_skill/SKILL.md", "my_skill/analyze.py"}

        contents = {f[0]: f[1] for f in files}
        assert contents["my_skill/SKILL.md"] == b"# My Skill"
        assert contents["my_skill/analyze.py"] == b"print('hello')"

    def test_skips_directories(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path,
            {
                "my_skill/SKILL.md": b"# Skill",
            },
        )
        # Manually add a directory entry
        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.mkdir("my_skill/subdir")

        files = files_from_zip(zip_path)
        assert len(files) == 1
        assert files[0][0] == "my_skill/SKILL.md"

    def test_skips_macosx_metadata(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path,
            {
                "my_skill/SKILL.md": b"# Skill",
                "__MACOSX/my_skill/._SKILL.md": b"macos metadata",
                "__MACOSX/._my_skill": b"more metadata",
            },
        )
        files = files_from_zip(zip_path)
        assert len(files) == 1
        assert files[0][0] == "my_skill/SKILL.md"

    def test_nested_directories(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path,
            {
                "skill/SKILL.md": b"# Root",
                "skill/lib/helpers.py": b"def helper(): ...",
                "skill/lib/utils/common.py": b"CONST = 1",
            },
        )
        files = files_from_zip(zip_path)
        names = sorted(f[0] for f in files)
        assert names == [
            "skill/SKILL.md",
            "skill/lib/helpers.py",
            "skill/lib/utils/common.py",
        ]

    def test_accepts_string_path(self, tmp_path: Path) -> None:
        zip_path = _make_zip(tmp_path, {"SKILL.md": b"content"})
        files = files_from_zip(str(zip_path))
        assert len(files) == 1

    def test_nonexistent_file(self) -> None:
        with pytest.raises((FileNotFoundError, OSError)):
            files_from_zip("/nonexistent/path.zip")

    def test_invalid_zip(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "bad.zip"
        bad_file.write_bytes(b"not a zip file")
        with pytest.raises(zipfile.BadZipFile):
            files_from_zip(bad_file)


class TestAsyncFilesFromZip:
    @pytest.mark.anyio
    async def test_basic(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path,
            {
                "my_skill/SKILL.md": b"# Skill",
                "my_skill/code.py": b"x = 1",
            },
        )
        files = await async_files_from_zip(zip_path)
        names = {f[0] for f in files}
        assert names == {"my_skill/SKILL.md", "my_skill/code.py"}

    @pytest.mark.anyio
    async def test_skips_macosx(self, tmp_path: Path) -> None:
        zip_path = _make_zip(
            tmp_path,
            {
                "SKILL.md": b"content",
                "__MACOSX/._SKILL.md": b"meta",
            },
        )
        files = await async_files_from_zip(zip_path)
        assert len(files) == 1
        assert files[0][0] == "SKILL.md"


class TestMixedTupleFormats:
    """Verify that the SDK's file processing pipeline handles both
    2-tuple (no MIME type) and 3-tuple (with MIME type) entries,
    confirming that MIME type is truly optional."""

    def test_mixed_tuples_are_valid_file_types(self) -> None:
        """Both 2-tuple and 3-tuple entries should be accepted as FileTypes."""
        from anthropic._files import _transform_file

        # 2-tuple: (filename, content) — no MIME type
        result_2 = _transform_file(("analyze.py", b"print('hi')"))
        assert result_2[0] == "analyze.py"
        assert result_2[1] == b"print('hi')"

        # 3-tuple: (filename, content, mime_type)
        result_3 = _transform_file(("SKILL.md", b"# Skill", "text/markdown"))
        assert result_3[0] == "SKILL.md"
        assert result_3[1] == b"# Skill"
        assert result_3[2] == "text/markdown"

    def test_mixed_list_through_to_httpx_files(self) -> None:
        """A list mixing 2-tuple and 3-tuple entries should pass through
        to_httpx_files without error."""
        from anthropic._files import to_httpx_files

        mixed_files = [
            ("files[]", ("SKILL.md", b"# Skill", "text/markdown")),
            ("files[]", ("code.py", b"x = 1")),
        ]
        result = to_httpx_files(mixed_files)
        assert len(result) == 2
