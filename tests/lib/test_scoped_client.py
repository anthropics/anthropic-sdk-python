"""Direct unit tests for `_copy_client_with_bearer_auth`.

These verify the load-bearing invariants of the util — auth replaced, parent
not mutated, helper-telemetry header set — without re-exercising `copy()`'s
own inheritance contract (which is the SDK's job to keep working). Both sync
and async client paths are covered so the `ClientT` generic threads through.
"""

from __future__ import annotations

import pathlib
from typing import Any

import httpx2
import pytest

from anthropic import Anthropic, AnthropicAWS, AsyncAnthropic, AsyncAnthropicAWS, OpenTelemetryOptions
from anthropic.lib._scoped_client import ClientT, copy_scoped_client, _copy_client_with_bearer_auth


def test_sets_bearer_auth_token_on_copy() -> None:
    parent = Anthropic(api_key="parent-key")
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-work-poller")
    assert scoped.auth_token == "env-key"


def test_clears_parent_api_key_on_copy() -> None:
    """If this ever starts returning a sub-client with `api_key` set, the
    parent's API credential would silently authenticate every helper request,
    because an API key beats an auth token."""
    parent = Anthropic(api_key="parent-key")
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-work-poller")
    assert scoped.api_key is None


def test_clears_inherited_credentials_provider() -> None:
    """When the parent client carries a credentials provider (e.g. workload
    identity), the sub-client must use the explicit bearer token as the
    unambiguous credential — not stack the provider's auth on top of it."""
    from anthropic.lib.credentials._types import AccessToken

    def fake_provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
        return AccessToken(token="provider-token")

    parent = Anthropic(credentials=fake_provider)
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-work-poller")
    assert scoped.credentials is None


def test_stamps_helper_telemetry_header() -> None:
    parent = Anthropic(api_key="parent-key")
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")
    assert scoped._custom_headers.get("x-stainless-helper") == "environments-worker"


def test_does_not_mutate_parent_client() -> None:
    """Building the sub-client must not touch the parent's auth state.

    Without this, a long-lived parent client could be silently re-credentialed
    every time a runner helper started."""
    parent = Anthropic(api_key="parent-key")
    _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-work-poller")
    assert parent.api_key == "parent-key"
    assert parent.auth_token is None


def test_empty_auth_token_raises() -> None:
    """An empty `auth_token` would silently fall back to the parent's
    `auth_token` via `copy()`'s truthy-or, producing a sub-client with no
    intentional credential set."""
    parent = Anthropic(api_key="parent-key")
    with pytest.raises(ValueError, match="auth_token"):
        _copy_client_with_bearer_auth(parent, auth_token="", helper="environments-work-poller")


@pytest.mark.asyncio()
async def test_async_client_path_clears_api_key_and_sets_bearer() -> None:
    """The same invariants hold for `AsyncAnthropic` — verifies the
    `ClientT` typevar threads sync/async correctly through `copy()`."""
    parent = AsyncAnthropic(api_key="parent-key")
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="session-tool-runner")
    assert isinstance(scoped, AsyncAnthropic)
    assert scoped.api_key is None
    assert scoped.auth_token == "env-key"
    assert scoped._custom_headers.get("x-stainless-helper") == "session-tool-runner"


def test_strips_inherited_authorization_from_parent_default_headers() -> None:
    """If the parent client was configured with a custom
    `default_headers={"Authorization": ...}` (or `X-Api-Key`), those would
    otherwise win over the bearer we just set because
    `AsyncAnthropic.default_headers` merges `_custom_headers` after
    `auth_headers`. The helper strips them from the sub-client's custom
    headers so the bearer is unambiguous on the wire."""
    parent = Anthropic(
        api_key="parent-key",
        default_headers={"Authorization": "Bearer parent-token", "X-Api-Key": "parent-key"},
    )
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")

    # Strip is case-insensitive, so neither name leaks through under any
    # casing.
    custom = {k.lower() for k in scoped._custom_headers}
    assert "authorization" not in custom
    assert "x-api-key" not in custom
    # Parent client is unmutated — its custom headers still carry the original
    # entries.
    parent_custom = {k.lower(): v for k, v in parent._custom_headers.items()}
    assert parent_custom["authorization"] == "Bearer parent-token"
    assert parent_custom["x-api-key"] == "parent-key"


@pytest.mark.asyncio()
async def test_scoped_sub_client_sends_only_bearer_on_the_wire() -> None:
    """Integration-level check: send a real HTTP request through the scoped
    sub-client (via `httpx2.MockTransport`) and inspect the headers actually
    on the wire. Asserts exactly one auth credential is sent — the bearer —
    and the parent's API key doesn't leak.

    This is the surface that the case-mismatch bug fixed by this whole
    refactor lived on. The unit tests above check the sub-client's *state*;
    this one checks the request the SDK builds *from* that state. If a future
    change to `_build_headers` reverses the merge order or
    `_copy_client_with_bearer_auth` stops stripping the parent's
    `X-Api-Key`, this is the test that catches it."""
    captured: list[httpx2.Request] = []

    async def handler(req: httpx2.Request) -> httpx2.Response:
        captured.append(req)
        return httpx2.Response(200, json={"id": "agent_test"})

    transport = httpx2.MockTransport(handler)
    http_client = httpx2.AsyncClient(transport=transport)
    # Parent has *every* way a credential could leak: an api_key, an
    # Authorization in default_headers, AND an X-Api-Key in default_headers.
    parent = AsyncAnthropic(
        api_key="parent-key",
        default_headers={
            "Authorization": "Bearer parent-token",
            "X-Api-Key": "parent-key",
        },
        http_client=http_client,
    )

    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")
    # Any GET that doesn't require a body — agents.retrieve is a thin GET that
    # exercises the same auth path the worker / poller use.
    await scoped.beta.agents.retrieve("agent_test")

    assert len(captured) == 1
    req = captured[0]
    # `httpx2.Headers` is case-insensitive, so .get() catches any casing.
    assert req.headers.get("authorization") == "Bearer env-key"
    # The parent's `X-Api-Key` must NOT be on the wire — that was the bug.
    assert req.headers.get("x-api-key") is None
    # Helper telemetry is on every scoped request.
    assert req.headers.get("x-stainless-helper") == "environments-worker"


def _config_with_its_own_host_and_workspace(tmp_path: pathlib.Path) -> dict[str, Any]:
    return {
        "base_url": "https://parent.example",
        "workspace_id": "wrkspc_parent",
        "authentication": {"type": "user_oauth", "credentials_path": str(tmp_path / "credentials.json")},
    }


def test_keeps_the_host_and_headers_of_the_parents_credential(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`copy()` drops both with the credential that brought them, but the
    bearer is for the deployment and workspace the parent talks to."""
    monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
    captured: list[httpx2.Request] = []

    def handler(req: httpx2.Request) -> httpx2.Response:
        captured.append(req)
        return httpx2.Response(200, json={"id": "agent_test"})

    parent = Anthropic(
        config=_config_with_its_own_host_and_workspace(tmp_path),
        http_client=httpx2.Client(transport=httpx2.MockTransport(handler)),
    )

    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")
    scoped.beta.agents.retrieve("agent_test")
    copy = copy_scoped_client(scoped, open_telemetry={**scoped.open_telemetry, "conversation_id": "conv_1"})
    copy.beta.agents.retrieve("agent_test")

    assert len(captured) == 2
    for req in captured:
        assert req.url.host == "parent.example"
        assert req.headers.get("anthropic-workspace-id") == "wrkspc_parent"
        assert req.headers.get_list("authorization") == ["Bearer env-key"]


@pytest.mark.asyncio()
async def test_async_keeps_the_host_and_headers_of_the_parents_credential(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
    captured: list[httpx2.Request] = []

    async def handler(req: httpx2.Request) -> httpx2.Response:
        captured.append(req)
        return httpx2.Response(200, json={"id": "agent_test"})

    parent = AsyncAnthropic(
        config=_config_with_its_own_host_and_workspace(tmp_path),
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(handler)),
    )

    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")
    await scoped.beta.agents.retrieve("agent_test")
    copy = copy_scoped_client(scoped, open_telemetry={**scoped.open_telemetry, "conversation_id": "conv_1"})
    await copy.beta.agents.retrieve("agent_test")

    assert len(captured) == 2
    for req in captured:
        assert req.url.host == "parent.example"
        assert req.headers.get("anthropic-workspace-id") == "wrkspc_parent"
        assert req.headers.get_list("authorization") == ["Bearer env-key"]


def test_aws_client_in_api_key_mode_sends_only_the_bearer() -> None:
    """`AnthropicAWS.copy()` passes the parent's key back in, so the base
    `copy()` cannot drop it. The key would then win over the bearer."""
    captured: list[httpx2.Request] = []

    def handler(req: httpx2.Request) -> httpx2.Response:
        captured.append(req)
        return httpx2.Response(200, json={"id": "agent_test"})

    parent = AnthropicAWS(
        api_key="parent-key",
        aws_region="us-east-1",
        workspace_id="ws-123",
        http_client=httpx2.Client(transport=httpx2.MockTransport(handler)),
    )

    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")
    scoped.beta.agents.retrieve("agent_test")

    assert scoped.api_key is None
    assert parent.api_key == "parent-key"
    assert len(captured) == 1
    assert captured[0].headers.get_list("authorization") == ["Bearer env-key"]
    assert captured[0].headers.get("x-api-key") is None


@pytest.mark.asyncio()
async def test_async_aws_client_in_api_key_mode_sends_only_the_bearer() -> None:
    captured: list[httpx2.Request] = []

    async def handler(req: httpx2.Request) -> httpx2.Response:
        captured.append(req)
        return httpx2.Response(200, json={"id": "agent_test"})

    parent = AsyncAnthropicAWS(
        api_key="parent-key",
        aws_region="us-east-1",
        workspace_id="ws-123",
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(handler)),
    )

    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-worker")
    await scoped.beta.agents.retrieve("agent_test")

    assert scoped.api_key is None
    assert len(captured) == 1
    assert captured[0].headers.get_list("authorization") == ["Bearer env-key"]
    assert captured[0].headers.get("x-api-key") is None


def test_copy_of_a_scoped_client_keeps_its_bearer_alone(monkeypatch: pytest.MonkeyPatch) -> None:
    """A new client reads `ANTHROPIC_CUSTOM_HEADERS` again, and a custom header goes before the client's own
    credentials. A plain `copy()` of the scoped sub-client would send these in place of its Bearer."""
    monkeypatch.setenv(
        "ANTHROPIC_CUSTOM_HEADERS", "authorization: Bearer env-secret\nX-Api-Key: env-api-key\nx-team: a"
    )
    monkeypatch.setenv("ANTHROPIC_API_KEY", "env-account-key")

    def copy_of_scoped(parent: ClientT) -> ClientT:
        scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="session-tool-runner")
        assert scoped.open_telemetry == parent.open_telemetry
        return copy_scoped_client(scoped, open_telemetry={**scoped.open_telemetry, "conversation_id": "conv_1"})

    open_telemetry: OpenTelemetryOptions = {"traces": {"content_mode": "content", "max_content_bytes": 4096}}
    sync_copy = copy_of_scoped(Anthropic(api_key="parent-key", open_telemetry=open_telemetry))
    async_copy = copy_of_scoped(AsyncAnthropic(api_key="parent-key", open_telemetry=open_telemetry))

    assert isinstance(sync_copy, Anthropic) and isinstance(async_copy, AsyncAnthropic)
    for copy in (sync_copy, async_copy):
        # The copy has the option that it is given, whole: the scoped client's own with the conversation ID.
        assert copy.open_telemetry == {
            "propagation": True,
            "traces": {"enabled": True, "content_mode": "content", "max_content_bytes": 4096},
            "conversation_id": "conv_1",
        }
        assert copy.api_key is None
        assert copy.default_headers["Authorization"] == "Bearer env-key"
        assert "X-Api-Key" not in copy.default_headers
        assert {key.lower() for key in copy.default_headers} >= {"x-team", "x-stainless-helper"}
        assert not {"authorization", "x-api-key"} & {key.lower() for key in copy._custom_headers}


def test_scoped_client_and_its_copy_keep_what_the_parent_read_from_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE", "content")
    monkeypatch.setenv("ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES", "4096")
    monkeypatch.setenv("ANTHROPIC_OPEN_TELEMETRY_PROPAGATION", "false")
    sync_parent, async_parent = Anthropic(api_key="parent-key"), AsyncAnthropic(api_key="parent-key")
    resolved = {
        "propagation": False,
        "traces": {"enabled": True, "content_mode": "content", "max_content_bytes": 4096},
    }
    assert sync_parent.open_telemetry == async_parent.open_telemetry == resolved

    # The variables are the parent's alone: no copy reads them again.
    monkeypatch.setenv("ANTHROPIC_OPEN_TELEMETRY", "false")
    monkeypatch.setenv("ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE", "metadata_only")
    monkeypatch.delenv("ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES")
    monkeypatch.delenv("ANTHROPIC_OPEN_TELEMETRY_PROPAGATION")

    def scoped_and_copy(parent: ClientT) -> tuple[ClientT, ClientT]:
        scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="session-tool-runner")
        return scoped, copy_scoped_client(scoped, open_telemetry={**scoped.open_telemetry, "conversation_id": "conv_1"})

    for scoped, copy in (scoped_and_copy(sync_parent), scoped_and_copy(async_parent)):
        assert scoped.open_telemetry == resolved
        assert copy.open_telemetry == {**resolved, "conversation_id": "conv_1"}
