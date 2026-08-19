"""Shared fixtures for the memory-sync suite."""

from __future__ import annotations

from typing import Any
from contextlib import contextmanager
from collections.abc import Callable, Iterator, AsyncIterator

import pytest

import anthropic.lib.tools._memories as memories_mod
from anthropic.lib.tools._memories import SessionMemoryStores
from anthropic.types.beta.memory_stores import BetaManagedAgentsMemory


class Clock:
    """A settable stand-in for the module's ``monotonic``."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


@pytest.fixture()
def clock(monkeypatch: pytest.MonkeyPatch) -> Clock:
    c = Clock()
    monkeypatch.setattr(memories_mod, "monotonic", c)
    return c


async def run_sync(stores: SessionMemoryStores) -> None:
    """Drive one reconcile pass without clock bookkeeping.

    The public cadence path (``sync_if_due`` plus the clock) is exercised
    by the worker tests; unit tests call the pass directly.
    """
    await stores._sync_all(final=False)  # pyright: ignore[reportPrivateUsage] -- the suite's one deterministic driver


@contextmanager
def listing_interrupted_by(
    stores: SessionMemoryStores, interrupt: Callable[[], object], *, after_items: int | None = None
) -> Iterator[None]:
    """Run ``interrupt`` once while a sync's server listing is being consumed:
    right after the sync has processed ``after_items`` listed memories, or
    once the listing is exhausted when ``None``. This lands a change on disk
    after the sync's directory scan and before whatever it does next."""
    real_list = stores._list_memories

    async def interrupted(memory_store_id: str, **kwargs: Any) -> AsyncIterator[BetaManagedAgentsMemory]:
        consumed = 0
        async for item in real_list(memory_store_id, **kwargs):
            yield item
            consumed += 1
            if consumed == after_items:
                interrupt()
        if after_items is None:
            interrupt()

    stores._list_memories = interrupted  # type: ignore[method-assign]
    try:
        yield
    finally:
        stores._list_memories = real_list  # type: ignore[method-assign]
