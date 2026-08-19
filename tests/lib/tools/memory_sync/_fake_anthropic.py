"""An ``AsyncAnthropic``-shaped stub backed by an in-memory store.

A memory store is a folder: path → content. ``MemoryServer`` is that dict
plus a log of the writes the code under test sent it. The SDK-shaped
resource ``SessionMemoryStores`` actually calls is a private adapter.

Paths are bare (``"push.md"``); the leading ``/`` the wire uses is added
and stripped internally so tests use one path vocabulary throughout.
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any
from collections.abc import Mapping, Callable, Awaitable, AsyncIterator

import httpx

from anthropic import APIStatusError


def _sha(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _status_error(code: int) -> APIStatusError:
    request = httpx.Request("POST", "https://api.example/v1/memory")
    return APIStatusError(f"status {code}", response=httpx.Response(code, request=request), body=None)


class MemoryServer:
    """The test's view of one remote memory store.

    ``files`` is its current state (path → content); ``received`` is every
    write the code under test sent it. Arranging via :meth:`write` /
    :meth:`delete` changes ``files`` without touching ``received`` — only
    the sync's own requests are recorded.
    """

    def __init__(self, initial: Mapping[str, str | None]) -> None:
        # A ``None`` value is a memory with null content — the wire allows it.
        self.files: dict[str, str | None] = dict(initial)
        self.received: list[tuple[Any, ...]] = []
        # Reject create/update content larger than this with a 400, like the
        # real server's per-memory cap.
        self.max_content_bytes: int | None = None
        # Session lookups the code under test performed (the worker shares one
        # fetch between the skills and memory downloads).
        self.retrieves: list[str] = []
        # Single-memory content fetches (the sync's content pass), in arrival
        # order — a test asserting "no content moved" checks this stays empty.
        self.content_fetches: list[str] = []
        # Called with the path as each content fetch arrives — raise to break
        # the fetch, or delete the path to race it against a server delete.
        self.fetch_hook: Callable[[str], None] | None = None
        # Awaited with the path as each create/update arrives, before the
        # request is recorded — park it to hold an upload open.
        self.upload_hook: Callable[[str], Awaitable[None]] | None = None

    def write(self, path: str, content: str) -> None:
        self.files[path] = content

    def delete(self, path: str) -> None:
        del self.files[path]


# Requests recorded on ``server.received``, in domain terms: paths and
# content. ``was`` is the pre-image content the request's precondition
# guards on — the builder computes the sha.


def created(path: str, content: str) -> tuple[Any, ...]:
    return ("create", path, content)


def updated(path: str, content: str, *, was: str) -> tuple[Any, ...]:
    return ("update", path, content, _sha(was))


def deleted(path: str, *, was: str) -> tuple[Any, ...]:
    return ("delete", path, _sha(was))


class _Resource:
    """Adapts a ``MemoryServer`` to the ``client.beta.memory_stores.memories`` shape.

    Items are built on the fly from ``server.files`` so there is no cached
    state to drift; ids are derived from paths so there is no id table.
    """

    def __init__(self, server: MemoryServer, *, noise: bool = False) -> None:
        self._server = server
        self._noise = noise

    def _item(self, path: str, *, view: str = "full") -> Any:
        content = self._server.files[path]
        return SimpleNamespace(
            type="memory",
            id=f"mem:{path}",
            path="/" + path,
            content=content if view == "full" else None,
            content_sha256=_sha(content or ""),
        )

    def list(self, memory_store_id: str, *, view: str = "basic", **_: Any) -> AsyncIterator[Any]:
        async def _iter() -> AsyncIterator[Any]:
            if self._noise:
                # Depth-limited listings roll directories up as prefixes;
                # only ``memory`` items carry content.
                yield SimpleNamespace(type="memory_prefix", path="/projects/")
            if memory_store_id == "memstore_broken":
                # One memory is listed, then the pager explodes.
                yield SimpleNamespace(
                    type="memory",
                    id="mem:half",
                    path="/half.md",
                    content="partial" if view == "full" else None,
                    content_sha256=_sha("partial"),
                )
                raise RuntimeError("list exploded")
            for path in list(self._server.files):
                yield self._item(path, view=view)

        return _iter()

    async def retrieve(self, memory_id: str, *, memory_store_id: str, view: str = "basic") -> Any:  # noqa: ARG002
        path = memory_id.removeprefix("mem:")
        self._server.content_fetches.append(path)
        if self._server.fetch_hook is not None:
            self._server.fetch_hook(path)
        if path not in self._server.files:
            raise _status_error(404)
        return self._item(path, view=view)

    def _check_size(self, content: str) -> None:
        cap = self._server.max_content_bytes
        if cap is not None and len(content.encode()) > cap:
            raise _status_error(400)

    async def create(self, _memory_store_id: str, *, path: str, content: str) -> Any:
        bare = path.lstrip("/")
        if self._server.upload_hook is not None:
            await self._server.upload_hook(bare)
        self._server.received.append(created(bare, content))
        self._check_size(content)
        self._server.files[bare] = content
        return self._item(bare)

    async def update(
        self,
        memory_id: str,
        *,
        memory_store_id: str,  # noqa: ARG002
        content: str,
        precondition: dict[str, str],
    ) -> Any:
        path = memory_id.removeprefix("mem:")
        if self._server.upload_hook is not None:
            await self._server.upload_hook(path)
        self._server.received.append(("update", path, content, precondition["content_sha256"]))
        self._check_size(content)
        if path not in self._server.files:
            raise _status_error(404)
        if _sha(self._server.files[path] or "") != precondition["content_sha256"]:
            raise _status_error(409)
        self._server.files[path] = content
        return self._item(path)

    async def delete(
        self,
        memory_id: str,
        *,
        memory_store_id: str,  # noqa: ARG002
        expected_content_sha256: str | None = None,
    ) -> Any:
        path = memory_id.removeprefix("mem:")
        self._server.received.append(("delete", path, expected_content_sha256))
        if path not in self._server.files:
            raise _status_error(404)
        if expected_content_sha256 is not None and _sha(self._server.files[path] or "") != expected_content_sha256:
            raise _status_error(409)
        del self._server.files[path]
        return SimpleNamespace(id=memory_id, type="memory_deleted")


def fake_anthropic(
    initial: Mapping[str, str | None],
    *,
    access: str | None = None,
    broken_store: bool = False,
    broken_store_last: bool = False,
    no_stores: bool = False,
    mount_path: str | None = None,
    noise: bool = False,
) -> tuple[Any, MemoryServer]:
    """An ``AsyncAnthropic``-shaped client with one memory store named ``notes``.

    The store lands at ``{workdir}/memory/notes``. Returns the client to
    hand to ``SessionMemoryStores`` and the server handle for the test.
    ``broken_store`` attaches a second store, ahead of ``notes``, whose
    listing explodes after one memory; ``broken_store_last`` puts it after,
    so ``notes`` lands first and the failure comes later. ``no_stores``
    attaches no memory store at all. ``noise`` adds a non-store resource
    to the session and a ``memory_prefix`` rollup to every listing.
    """
    server = MemoryServer(initial)
    resources: list[Any] = (
        []
        if no_stores
        else [
            SimpleNamespace(
                type="memory_store",
                memory_store_id="memstore_notes",
                mount_path=mount_path,
                name="notes",
                access=access,
            )
        ]
    )
    if noise:
        resources.insert(0, SimpleNamespace(type="file", file_id="file_1"))
    if broken_store or broken_store_last:
        broken = SimpleNamespace(
            type="memory_store", memory_store_id="memstore_broken", mount_path=None, name="broken", access=None
        )
        if broken_store_last:
            resources.append(broken)
        else:
            resources.insert(0, broken)

    async def _retrieve(session_id: str) -> Any:
        server.retrieves.append(session_id)
        return SimpleNamespace(agent=SimpleNamespace(skills=[]), resources=resources)

    client = SimpleNamespace(
        beta=SimpleNamespace(
            sessions=SimpleNamespace(retrieve=_retrieve),
            memory_stores=SimpleNamespace(memories=_Resource(server, noise=noise)),
        )
    )
    return client, server
