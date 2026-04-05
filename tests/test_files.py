from pathlib import Path

import anyio
import pytest
from dirty_equals import IsDict, IsList, IsBytes, IsTuple

from anthropic._files import to_httpx_files, async_to_httpx_files

readme_path = Path(__file__).parent.parent.joinpath("README.md")


def test_pathlib_includes_file_name() -> None:
    result = to_httpx_files({"file": readme_path})
    print(result)
    assert result == IsDict({"file": IsTuple("README.md", IsBytes())})


def test_tuple_input() -> None:
    result = to_httpx_files([("file", readme_path)])
    print(result)
    assert result == IsList(IsTuple("file", IsTuple("README.md", IsBytes())))


@pytest.mark.asyncio
async def test_async_pathlib_includes_file_name() -> None:
    result = await async_to_httpx_files({"file": readme_path})
    print(result)
    assert result == IsDict({"file": IsTuple("README.md", IsBytes())})


@pytest.mark.asyncio
async def test_async_supports_anyio_path() -> None:
    result = await async_to_httpx_files({"file": anyio.Path(readme_path)})
    print(result)
    assert result == IsDict({"file": IsTuple("README.md", IsBytes())})


@pytest.mark.asyncio
async def test_async_tuple_input() -> None:
    result = await async_to_httpx_files([("file", readme_path)])
    print(result)
    assert result == IsList(IsTuple("file", IsTuple("README.md", IsBytes())))


def test_pathlike_in_tuple() -> None:
    result = to_httpx_files({"file": ("custom_name.txt", readme_path, "text/plain")})
    assert result == IsDict({"file": IsTuple("custom_name.txt", IsBytes(), "text/plain")})


@pytest.mark.asyncio
async def test_async_pathlike_in_tuple() -> None:
    result = await async_to_httpx_files({"file": ("custom_name.txt", readme_path, "text/plain")})
    assert result == IsDict({"file": IsTuple("custom_name.txt", IsBytes(), "text/plain")})


def test_string_not_allowed() -> None:
    with pytest.raises(TypeError, match="Expected file types input to be a FileContent type or to be a tuple"):
        to_httpx_files(
            {
                "file": "foo",  # type: ignore
            }
        )
