import asyncio
from typing import Generator

import pytest

pytest.register_assert_rewrite("tests.utils")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
