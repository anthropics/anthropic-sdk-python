from __future__ import annotations

import threading
from typing import Any, cast

import pytest

from anthropic.lib.tools._tool_dispatch import run_runnable_tool


class _SyncTool:
    def __init__(self) -> None:
        self.call_thread: int | None = None

    def call(self, input: object) -> str:
        assert input == {"value": 1}
        self.call_thread = threading.get_ident()
        return "sync-result"


class _AsyncTool:
    def __init__(self) -> None:
        self.call_thread: int | None = None

    async def call(self, input: object) -> str:
        assert input == {"value": 2}
        self.call_thread = threading.get_ident()
        return "async-result"


class _SyncAwaitableTool:
    def __init__(self) -> None:
        self.call_thread: int | None = None
        self.await_thread: int | None = None

    def call(self, input: object) -> Any:
        assert input == {"value": 3}
        self.call_thread = threading.get_ident()

        async def finish() -> str:
            self.await_thread = threading.get_ident()
            return "awaitable-result"

        return finish()


@pytest.mark.asyncio
async def test_sync_tool_runs_in_worker_thread() -> None:
    event_loop_thread = threading.get_ident()
    tool = _SyncTool()

    result = await run_runnable_tool(cast(Any, tool), {"value": 1})

    assert result == "sync-result"
    assert tool.call_thread is not None
    assert tool.call_thread != event_loop_thread


@pytest.mark.asyncio
async def test_native_async_tool_stays_on_event_loop_thread() -> None:
    event_loop_thread = threading.get_ident()
    tool = _AsyncTool()

    result = await run_runnable_tool(cast(Any, tool), {"value": 2})

    assert result == "async-result"
    assert tool.call_thread == event_loop_thread


@pytest.mark.asyncio
async def test_sync_wrapper_returning_awaitable_is_still_supported() -> None:
    event_loop_thread = threading.get_ident()
    tool = _SyncAwaitableTool()

    result = await run_runnable_tool(cast(Any, tool), {"value": 3})

    assert result == "awaitable-result"
    assert tool.call_thread is not None
    assert tool.call_thread != event_loop_thread
    assert tool.await_thread == event_loop_thread
