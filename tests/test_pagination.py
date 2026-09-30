"""Cursor pagination must keep walking while the service still hands back a cursor.

`files.list()` and every other `PageCursor` / `TokenPage` endpoint return an opaque
`next_page` token that is independent of the `data` array, so a page can legitimately
carry zero rows and still point at more results.
"""

from __future__ import annotations

from typing import Any

import httpx2

from anthropic import Anthropic, AsyncAnthropic

from .test_client import MockTransport

base_url = "http://127.0.0.1:4010"
api_key = "my-anthropic-api-key"


def _file(fid: str) -> dict[str, Any]:
    return {
        "id": fid,
        "type": "file",
        "filename": f"{fid}.txt",
        "mime_type": "text/plain",
        "size_bytes": 12,
        "created_at": "2026-01-01T00:00:00Z",
    }


# The middle page is empty but still resumes, which is what a filtered list returns
# when a whole page is dropped server side.
PAGES: dict[str | None, dict[str, Any]] = {
    None: {"data": [_file("file_1")], "next_page": "tok-2"},
    "tok-2": {"data": [], "next_page": "tok-3"},
    "tok-3": {"data": [_file("file_3")], "next_page": None},
}


def _handler(request: httpx2.Request) -> httpx2.Response:
    return httpx2.Response(200, json=PAGES[request.url.params.get("page")])


async def _async_handler(request: httpx2.Request) -> httpx2.Response:
    return _handler(request)


def _sync_client() -> Anthropic:
    return Anthropic(
        api_key=api_key,
        base_url=base_url,
        http_client=httpx2.Client(transport=MockTransport(handler=_handler)),
    )


def _async_client() -> AsyncAnthropic:
    return AsyncAnthropic(
        api_key=api_key,
        base_url=base_url,
        http_client=httpx2.AsyncClient(transport=MockTransport(handler=_async_handler)),
    )


def test_empty_page_holding_a_cursor_reports_a_next_page() -> None:
    page = _sync_client().files.list(page="tok-2")

    assert page.data == []
    assert page.next_page_info() is not None
    assert page.has_next_page() is True


def test_sync_auto_pagination_continues_past_an_empty_page() -> None:
    assert [f.id for f in _sync_client().files.list()] == ["file_1", "file_3"]


async def test_async_auto_pagination_continues_past_an_empty_page() -> None:
    ids = [f.id async for f in _async_client().files.list()]

    assert ids == ["file_1", "file_3"]
