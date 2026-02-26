"""Tests for anthropic._files: file transformation utilities for httpx.

Covers to_httpx_files, async_to_httpx_files, read_file_content,
async_read_file_content, is_file_content, is_base64_file_input,
and assert_is_file_content.
"""

from __future__ import annotations

import io
from pathlib import Path

import anyio
import pytest
from dirty_equals import IsDict, IsList, IsBytes, IsTuple

from anthropic._files import (
    is_file_content,
    read_file_content,
    to_httpx_files,
    is_base64_file_input,
    async_to_httpx_files,
    assert_is_file_content,
    async_read_file_content,
)

readme_path = Path(__file__).parent.parent.joinpath("README.md")


# ---------------------------------------------------------------------------
# is_file_content — type guard for accepted file input types
# ---------------------------------------------------------------------------
class TestIsFileContent:
    """Verify the type guard accepts bytes, tuples, IO objects, and PathLike."""

    @pytest.mark.parametrize(
        "value, expected",
        [
            pytest.param(b"raw bytes", True, id="bytes"),
            pytest.param(io.BytesIO(b"stream"), True, id="BytesIO"),
            pytest.param(readme_path, True, id="pathlib.Path"),
            pytest.param(("name", b"content"), True, id="tuple"),
            pytest.param("a string", False, id="str-rejected"),
            pytest.param(42, False, id="int-rejected"),
            pytest.param(None, False, id="none-rejected"),
            pytest.param(["a", "list"], False, id="list-rejected"),
        ],
        ids=str,
    )
    def test_type_guard(self, value: object, expected: bool) -> None:
        assert is_file_content(value) is expected


# ---------------------------------------------------------------------------
# is_base64_file_input — type guard for IO and PathLike
# ---------------------------------------------------------------------------
class TestIsBase64FileInput:
    """Verify the type guard accepts IO objects and PathLike, rejects others."""

    @pytest.mark.parametrize(
        "value, expected",
        [
            pytest.param(io.BytesIO(b"data"), True, id="BytesIO"),
            pytest.param(readme_path, True, id="pathlib.Path"),
            pytest.param(b"raw bytes", False, id="bytes-rejected"),
            pytest.param("string", False, id="str-rejected"),
            pytest.param(None, False, id="none-rejected"),
        ],
        ids=str,
    )
    def test_type_guard(self, value: object, expected: bool) -> None:
        assert is_base64_file_input(value) is expected


# ---------------------------------------------------------------------------
# assert_is_file_content — raises on invalid types
# ---------------------------------------------------------------------------
class TestAssertIsFileContent:
    """Verify that assert_is_file_content raises RuntimeError for bad types."""

    def test_accepts_valid_bytes(self) -> None:
        """Should not raise for bytes input."""
        assert_is_file_content(b"ok")

    def test_accepts_valid_path(self) -> None:
        """Should not raise for PathLike input."""
        assert_is_file_content(readme_path)

    def test_accepts_valid_bytesio(self) -> None:
        """Should not raise for IO input."""
        assert_is_file_content(io.BytesIO(b"ok"))

    def test_rejects_string(self) -> None:
        """Strings are not valid file content."""
        with pytest.raises(RuntimeError, match="Expected file input"):
            assert_is_file_content("bad")

    def test_rejects_string_with_key(self) -> None:
        """Error message includes key name when provided."""
        with pytest.raises(RuntimeError, match="Expected entry at `mykey`"):
            assert_is_file_content("bad", key="mykey")

    def test_rejects_int(self) -> None:
        with pytest.raises(RuntimeError):
            assert_is_file_content(42)


# ---------------------------------------------------------------------------
# read_file_content / async_read_file_content — PathLike -> bytes
# ---------------------------------------------------------------------------
class TestReadFileContent:
    """Verify sync and async file content reading."""

    def test_reads_pathlike(self) -> None:
        """PathLike inputs are read into bytes."""
        result = read_file_content(readme_path)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_passes_through_bytes(self) -> None:
        """Bytes are returned as-is."""
        data = b"hello"
        assert read_file_content(data) is data

    def test_passes_through_io(self) -> None:
        """IO objects are returned as-is."""
        buf = io.BytesIO(b"hello")
        assert read_file_content(buf) is buf

    async def test_async_reads_pathlike(self) -> None:
        """Async variant reads PathLike into bytes."""
        result = await async_read_file_content(readme_path)
        assert isinstance(result, bytes)
        assert len(result) > 0

    async def test_async_passes_through_bytes(self) -> None:
        """Async variant returns bytes as-is."""
        data = b"hello"
        assert await async_read_file_content(data) is data

    async def test_async_passes_through_io(self) -> None:
        """Async variant returns IO as-is."""
        buf = io.BytesIO(b"hello")
        assert await async_read_file_content(buf) is buf


# ---------------------------------------------------------------------------
# to_httpx_files — sync file transformation
# ---------------------------------------------------------------------------
class TestToHttpxFiles:
    """Verify sync transformation of RequestFiles to HttpxRequestFiles."""

    # -- None passthrough --
    def test_none_returns_none(self) -> None:
        """None input should pass through as None."""
        assert to_httpx_files(None) is None

    # -- Mapping inputs --
    def test_pathlib_includes_filename(self) -> None:
        """PathLike values in a mapping are converted to (name, bytes) tuples."""
        result = to_httpx_files({"file": readme_path})
        assert result == IsDict({"file": IsTuple("README.md", IsBytes())})

    def test_bytes_passed_through(self) -> None:
        """Bytes values in a mapping are kept as-is."""
        data = b"raw content"
        result = to_httpx_files({"file": data})
        assert result == {"file": data}

    def test_bytesio_passed_through(self) -> None:
        """IO objects in a mapping are kept as-is."""
        buf = io.BytesIO(b"buffered")
        result = to_httpx_files({"file": buf})
        assert result == {"file": buf}

    def test_empty_mapping(self) -> None:
        """Empty dict produces empty dict."""
        assert to_httpx_files({}) == {}

    def test_tuple_with_content_type(self) -> None:
        """Tuple (name, content, content_type) is properly transformed.

        When content is bytes, the tuple passes through is_file_content and
        is returned as-is since tuples are a valid FileContent type.
        """
        result = to_httpx_files({"file": ("doc.pdf", b"pdf-bytes", "application/pdf")})
        assert isinstance(result, dict)
        entry = result["file"]
        assert entry == ("doc.pdf", b"pdf-bytes", "application/pdf")

    def test_tuple_passed_through(self) -> None:
        """Tuples are valid FileContent and pass through is_file_content as-is.

        Because isinstance(tuple, tuple) is True, tuples match is_file_content
        and are returned without further transformation. The PathLike inside
        the tuple is NOT read — callers handle that downstream.
        """
        t = ("doc.md", readme_path)
        result = to_httpx_files({"file": t})
        assert isinstance(result, dict)
        assert result["file"] is t

    # -- Sequence inputs --
    def test_sequence_input(self) -> None:
        """List-of-tuples input is transformed correctly."""
        result = to_httpx_files([("file", readme_path)])
        assert result == IsList(IsTuple("file", IsTuple("README.md", IsBytes())))

    def test_empty_sequence(self) -> None:
        """Empty sequence produces empty list."""
        assert to_httpx_files([]) == []

    # -- Error cases --
    def test_string_value_raises_type_error(self) -> None:
        """String file values are rejected with a clear error."""
        with pytest.raises(TypeError, match="Expected file types input to be a FileContent type or to be a tuple"):
            to_httpx_files({"file": "not_a_file"})  # type: ignore

    def test_int_value_raises_type_error(self) -> None:
        """Integer file values are rejected."""
        with pytest.raises(TypeError, match="Expected file types input to be a FileContent type or to be a tuple"):
            to_httpx_files({"file": 123})  # type: ignore


# ---------------------------------------------------------------------------
# async_to_httpx_files — async file transformation
# ---------------------------------------------------------------------------
class TestAsyncToHttpxFiles:
    """Verify async transformation of RequestFiles to HttpxRequestFiles."""

    async def test_none_returns_none(self) -> None:
        """None input should pass through as None."""
        assert await async_to_httpx_files(None) is None

    async def test_pathlib_includes_filename(self) -> None:
        """PathLike values in a mapping are converted to (name, bytes) tuples."""
        result = await async_to_httpx_files({"file": readme_path})
        assert result == IsDict({"file": IsTuple("README.md", IsBytes())})

    async def test_anyio_path_supported(self) -> None:
        """anyio.Path is accepted and read correctly."""
        result = await async_to_httpx_files({"file": anyio.Path(readme_path)})
        assert result == IsDict({"file": IsTuple("README.md", IsBytes())})

    async def test_bytes_passed_through(self) -> None:
        """Bytes values are kept as-is."""
        data = b"raw"
        result = await async_to_httpx_files({"file": data})
        assert result == {"file": data}

    async def test_bytesio_passed_through(self) -> None:
        """IO objects are kept as-is."""
        buf = io.BytesIO(b"buf")
        result = await async_to_httpx_files({"file": buf})
        assert result == {"file": buf}

    async def test_sequence_input(self) -> None:
        """List-of-tuples input is transformed correctly."""
        result = await async_to_httpx_files([("file", readme_path)])
        assert result == IsList(IsTuple("file", IsTuple("README.md", IsBytes())))

    async def test_empty_mapping(self) -> None:
        """Empty dict produces empty dict."""
        assert await async_to_httpx_files({}) == {}

    async def test_empty_sequence(self) -> None:
        """Empty sequence produces empty list."""
        assert await async_to_httpx_files([]) == []

    async def test_string_value_raises_type_error(self) -> None:
        """String file values are rejected with a clear error."""
        with pytest.raises(TypeError, match="Expected file types input to be a FileContent type or to be a tuple"):
            await async_to_httpx_files({"file": "not_a_file"})  # type: ignore

    async def test_tuple_with_content_type(self) -> None:
        """Tuple (name, content, content_type) passes through as-is when content is bytes."""
        result = await async_to_httpx_files({"file": ("doc.pdf", b"pdf-bytes", "application/pdf")})
        assert isinstance(result, dict)
        entry = result["file"]
        assert entry == ("doc.pdf", b"pdf-bytes", "application/pdf")

    async def test_tuple_passed_through(self) -> None:
        """Tuples are valid FileContent and pass through as-is.

        Same as sync: tuples match is_file_content, so PathLike inside
        the tuple is NOT read by _transform_file.
        """
        t = ("doc.md", readme_path)
        result = await async_to_httpx_files({"file": t})
        assert isinstance(result, dict)
        assert result["file"] is t
