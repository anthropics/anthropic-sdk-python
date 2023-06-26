import asyncio

import pytest

pytest.register_assert_rewrite("tests.utils")


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.new_event_loop()
