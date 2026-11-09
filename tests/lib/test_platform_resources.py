from __future__ import annotations

import re
import inspect
import pathlib
import contextlib
from typing import Any

import httpx2
import pytest

from anthropic import (
    Anthropic,
    AnthropicError,
    AsyncAnthropic,
    AnthropicVertex,
    AnthropicBedrock,
    AsyncAnthropicVertex,
    AsyncAnthropicBedrock,
)
from anthropic.lib.bedrock._mantle import USER_PROFILE_ID_BODY_PATHS

MESSAGE_PARAMS: dict[str, Any] = {
    "max_tokens": 16,
    "messages": [{"role": "user", "content": "Hi"}],
    "model": "claude-fake",
}

MESSAGE = {
    "id": "msg_fake",
    "type": "message",
    "role": "assistant",
    "model": "claude-fake",
    "content": [{"type": "text", "text": "Hello"}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {"input_tokens": 1, "output_tokens": 1},
}

# The HTTP method and path of every method of `client.messages` and `client.beta.messages`.
MESSAGES_ROUTES: list[tuple[str, str]] = sorted(
    set(re.findall(r'title="(\w+) (/v1/messages[^"]*)"', (pathlib.Path(__file__).parents[2] / "api.md").read_text()))
)

# What `client.beta.messages` has and the platform does not serve.
NOT_SERVED = {
    "bedrock": {"batches", "count_tokens"},
    "vertex": {"batches"},
}

# The other `POST` paths. On these, Mantle reads the user profile ID from the header.
MANTLE_HEADER_PATHS = {"/v1/messages/batches", "/v1/messages/batches/{message_batch_id}/cancel"}


def platform_client(platform: str, sync: bool, requests: list[httpx2.Request] | None = None) -> Any:
    def respond(request: httpx2.Request) -> httpx2.Response:
        if requests is not None:
            requests.append(request)
        return httpx2.Response(200, json=MESSAGE)

    transport = httpx2.MockTransport(respond)
    if platform == "bedrock":
        if sync:
            return AnthropicBedrock(
                aws_region="us-east-1", api_key="fake-api-key", http_client=httpx2.Client(transport=transport)
            )
        return AsyncAnthropicBedrock(
            aws_region="us-east-1", api_key="fake-api-key", http_client=httpx2.AsyncClient(transport=transport)
        )

    if sync:
        return AnthropicVertex(
            region="us-east5",
            project_id="fake-project",
            access_token="fake-access-token",
            http_client=httpx2.Client(transport=transport),
        )
    return AsyncAnthropicVertex(
        region="us-east5",
        project_id="fake-project",
        access_token="fake-access-token",
        http_client=httpx2.AsyncClient(transport=transport),
    )


def public_members(value: object) -> set[str]:
    return {name for name in dir(value) if not name.startswith("_")}


each_platform_client = pytest.mark.parametrize(
    ("platform", "sync"),
    [("bedrock", True), ("bedrock", False), ("vertex", True), ("vertex", False)],
    ids=["bedrock-sync", "bedrock-async", "vertex-sync", "vertex-async"],
)


@pytest.mark.parametrize(
    "view", [None, "with_raw_response", "with_streaming_response"], ids=lambda view: view or "methods"
)
@each_platform_client
def test_beta_messages_methods_are_up_to_date(
    platform: str, sync: bool, view: str | None, client: Anthropic, async_client: AsyncAnthropic
) -> None:
    first_party: object = (client if sync else async_client).beta.messages
    listed: object = platform_client(platform, sync).beta.messages
    if view is not None:
        first_party = getattr(first_party, view)
        listed = getattr(listed, view)

    assert public_members(listed) == public_members(first_party) - NOT_SERVED[platform], (
        f"Update the classes in `src/anthropic/lib/{platform}/_beta_messages.py`, which list the methods of "
        "`client.beta.messages` by hand. Add a method that the platform does not serve to `NOT_SERVED` instead."
    )


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
@pytest.mark.parametrize(
    ("platform", "method"), [("bedrock", "parse"), ("vertex", "parse"), ("vertex", "count_tokens")]
)
async def test_beta_messages_raw_response(platform: str, method: str, sync: bool) -> None:
    requests: list[httpx2.Request] = []
    params = {name: value for name, value in MESSAGE_PARAMS.items() if method == "parse" or name != "max_tokens"}

    response = getattr(platform_client(platform, sync, requests).beta.messages.with_raw_response, method)(**params)
    if not sync:
        response = await response

    assert response.http_request is requests[0]
    assert "/v1/messages" not in requests[0].url.path


# No method sends `?beta=true`, but the checks on the path allow for a caller's own `client.post()` that does.
@pytest.mark.parametrize("query", ["", "?beta=true"], ids=["plain", "beta-query"])
@pytest.mark.parametrize(("http_method", "path"), MESSAGES_ROUTES)
@each_platform_client
async def test_messages_routes_are_all_handled(
    platform: str, sync: bool, http_method: str, path: str, query: str
) -> None:
    requests: list[httpx2.Request] = []
    send = getattr(platform_client(platform, sync, requests), http_method)
    body = {"body": dict(MESSAGE_PARAMS)} if http_method == "post" else {}

    # The client refuses a route that the platform does not serve.
    with contextlib.suppress(AnthropicError):
        response = send(re.sub(r"\{\w+\}", "fake", path) + query, cast_to=httpx2.Response, **body)
        if inspect.isawaitable(response):
            await response

    assert [str(request.url) for request in requests if "/v1/messages" in request.url.path] == [], (
        f"Give this route the path that the platform serves it on, or refuse it, in `_prepare_options` in "
        f"`src/anthropic/lib/{platform}/_client.py`."
    )


def test_mantle_user_profile_id_paths_are_up_to_date() -> None:
    post_paths = {path for http_method, path in MESSAGES_ROUTES if http_method == "post"}

    assert post_paths == {path for path in USER_PROFILE_ID_BODY_PATHS if "?" not in path} | MANTLE_HEADER_PATHS, (
        "Add the path to `USER_PROFILE_ID_BODY_PATHS` in `src/anthropic/lib/bedrock/_mantle.py` if Mantle reads the "
        "user profile ID from the body of its requests, and to `MANTLE_HEADER_PATHS` if it reads the header."
    )
