from __future__ import annotations

import os
import json
from typing import Any, List, Callable, Awaitable, cast
from typing_extensions import TypeVar

import httpx
from respx import MockRouter
from inline_snapshot import outsource, get_snapshot_value

from anthropic import Anthropic, AsyncAnthropic
from anthropic._utils._utils import is_list

_T = TypeVar("_T")


def make_snapshot_request(
    func: Callable[[Anthropic], _T],
    *,
    content_snapshot: Any,
    respx_mock: MockRouter,
    mock_client: Anthropic,
    path: str,
) -> _T:
    live = os.environ.get("ANTHROPIC_LIVE") == "1"
    collected: list[str] = []
    if live:

        def _on_response(response: httpx.Response) -> None:
            collected.append(json.dumps(json.loads(response.read())))

        respx_mock.stop()

        client = Anthropic(
            http_client=httpx.Client(
                event_hooks={
                    "response": [_on_response],
                }
            )
        )
    else:
        responses = get_snapshot_value(content_snapshot)
        assert is_list(responses)

        curr = 0

        def get_response(_request: httpx.Request) -> httpx.Response:
            nonlocal curr
            content = responses[curr]
            assert isinstance(content, str)

            curr += 1
            return httpx.Response(
                200,
                content=content,
                headers={"content-type": "application/json"},
            )

        respx_mock.post(path).mock(side_effect=get_response)

        client = mock_client

    result = func(client)

    if not live:
        return result

    client.close()

    if len(collected) == 1:
        assert collected[0] == content_snapshot
    else:
        assert collected == content_snapshot

    return result


def make_stream_snapshot_request(
    func: Callable[[Anthropic], _T],
    *,
    content_snapshot: Any,
    respx_mock: MockRouter,
    mock_client: Anthropic,
    path: str,
) -> _T:
    live = os.environ.get("ANTHROPIC_LIVE") == "1"
    collected: list[str] = []
    if live:

        def _on_response(response: httpx.Response) -> None:
            response.read()
            collected.append(response.text)

        respx_mock.stop()

        client = Anthropic(
            http_client=httpx.Client(
                event_hooks={
                    "response": [_on_response],
                }
            )
        )
    else:
        response_contents = get_snapshot_value(content_snapshot)
        assert is_list(response_contents)

        response_contents = cast(
            List[str],
            response_contents,
        )

        curr = 0

        def get_response(_request: httpx.Request) -> httpx.Response:
            nonlocal curr
            content = response_contents[curr]
            assert isinstance(content, str)

            curr += 1
            return httpx.Response(
                200,
                content=content.encode("utf-8"),
                headers={"content-type": "text/event-stream"},
            )

        respx_mock.post(path).mock(side_effect=get_response)
        client = mock_client

    result = func(client)
    if not live:
        return result

    assert outsource(collected) == content_snapshot
    return result


async def make_async_snapshot_request(
    func: Callable[[AsyncAnthropic], Awaitable[_T]],
    *,
    content_snapshot: Any,
    respx_mock: MockRouter,
    mock_client: AsyncAnthropic,
    path: str,
) -> _T:
    live = os.environ.get("ANTHROPIC_LIVE") == "1"
    collected: list[str] = []
    if live:

        async def _on_response(response: httpx.Response) -> None:
            collected.append(json.dumps(json.loads(await response.aread())))

        respx_mock.stop()

        client = AsyncAnthropic(
            http_client=httpx.AsyncClient(
                event_hooks={
                    "response": [_on_response],
                }
            )
        )
    else:
        responses = get_snapshot_value(content_snapshot)
        assert is_list(responses)

        curr = 0

        def get_response(_request: httpx.Request) -> httpx.Response:
            nonlocal curr
            content = responses[curr]
            assert isinstance(content, str)

            curr += 1
            return httpx.Response(
                200,
                content=content,
                headers={"content-type": "application/json"},
            )

        respx_mock.post(path).mock(side_effect=get_response)

        client = mock_client

    result = await func(client)

    if not live:
        return result

    await client.close()

    if len(collected) == 1:
        assert collected[0] == content_snapshot
    else:
        assert collected == content_snapshot

    return result
