from __future__ import annotations

from typing import Any, cast

import httpx
import pytest

from anthropic import APIStatusError
from anthropic.lib.environments import _poller
from anthropic.lib.environments._poller import aiter_work, iter_work


class _WorkData:
    type = "session"


class _WorkItem:
    def __init__(self, work_id: str = "work_1") -> None:
        self.id = work_id
        self.data = _WorkData()


def _api_status_error(code: int) -> APIStatusError:
    request = httpx.Request("POST", "https://api.example/work")
    response = httpx.Response(code, request=request, content=b"{}")
    return APIStatusError("boom", response=response, body=None)


class _SyncWork:
    def __init__(self) -> None:
        self.item = _WorkItem()
        self.events: list[str] = []
        self.poll_calls = 0
        self.ack_calls = 0

    def poll(self, _environment_id: str, **_kwargs: Any) -> _WorkItem:
        self.poll_calls += 1
        self.events.append("poll")
        if self.poll_calls > 1:
            raise AssertionError("polled again before the claimed item was acknowledged")
        return self.item

    def ack(self, work_id: str, **_kwargs: Any) -> None:
        assert work_id == self.item.id
        self.ack_calls += 1
        self.events.append("ack")
        if self.ack_calls == 1:
            raise _api_status_error(500)

    def stop(self, _work_id: str, **_kwargs: Any) -> None:
        raise AssertionError("auto_stop=False should not stop the item")


class _AsyncWork:
    def __init__(self) -> None:
        self.item = _WorkItem()
        self.events: list[str] = []
        self.poll_calls = 0
        self.ack_calls = 0

    async def poll(self, _environment_id: str, **_kwargs: Any) -> _WorkItem:
        self.poll_calls += 1
        self.events.append("poll")
        if self.poll_calls > 1:
            raise AssertionError("polled again before the claimed item was acknowledged")
        return self.item

    async def ack(self, work_id: str, **_kwargs: Any) -> None:
        assert work_id == self.item.id
        self.ack_calls += 1
        self.events.append("ack")
        if self.ack_calls == 1:
            raise _api_status_error(500)

    async def stop(self, _work_id: str, **_kwargs: Any) -> None:
        raise AssertionError("auto_stop=False should not stop the item")


def test_sync_transient_ack_failure_retries_same_claim_before_polling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_poller.time, "sleep", lambda _seconds: None)
    work = _SyncWork()

    item = next(iter_work(cast(Any, work), environment_id="env_1", auto_stop=False))

    assert item is work.item
    assert work.events == ["poll", "ack", "ack"]
    assert work.poll_calls == 1


async def test_async_transient_ack_failure_retries_same_claim_before_polling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(_poller.anyio, "sleep", _no_sleep)
    work = _AsyncWork()
    iterator = aiter_work(cast(Any, work), environment_id="env_1", auto_stop=False)

    item = await iterator.__anext__()

    assert item is work.item
    assert work.events == ["poll", "ack", "ack"]
    assert work.poll_calls == 1
