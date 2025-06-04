from __future__ import annotations

import os
from typing import TypeVar, Iterator
from typing_extensions import AsyncIterator

_T = TypeVar("_T")


def load_fixture(fixture_name: str) -> str:
    """Load a fixture file from the fixtures directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_dir = os.path.join(current_dir, "fixtures")
    with open(os.path.join(fixtures_dir, fixture_name), "r") as f:
        return f.read()


def get_response(fixture_name: str) -> Iterator[bytes]:
    """Convert a fixture file into a stream of bytes for testing."""
    content = load_fixture(fixture_name)
    for line in content.splitlines():
        yield line.encode() + b"\n"


async def to_async_iter(iter: Iterator[_T]) -> AsyncIterator[_T]:
    """Convert a synchronous iterator to an asynchronous one."""
    for event in iter:
        yield event
