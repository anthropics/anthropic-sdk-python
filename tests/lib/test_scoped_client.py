"""Direct unit tests for :func:`_copy_client_with_bearer_auth`.

These verify the load-bearing invariants of the util — auth replaced, parent
not mutated, helper-telemetry header set — without re-exercising ``copy()``'s
own inheritance contract (which is the SDK's job to keep working). Both sync
and async client paths are covered so the ``ClientT`` generic threads through.
"""

from __future__ import annotations

import httpx
import pytest

from anthropic import Anthropic, AsyncAnthropic
from anthropic.lib._scoped_client import _copy_client_with_bearer_auth


def test_sets_bearer_auth_token_on_copy() -> None:
    parent = Anthropic(api_key="parent-key")
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="environments-work-poller")
    assert scoped.auth_token == "env-key"


def test_clears_parent_api_key_on_copy() -> None:
    """The post-hoc ``scoped.api_key = None`` mutation is the only thing
    keeping the parent's ``X-Api-Key`` off the sub-client's wire. If this ever
    starts returning a sub-client with ``api_key`` set, the parent's API
    credential would silently authenticate every helper request."""
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

    parent = Anthropic(api_key="parent-key", credentials=fake_provider)
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
    """An empty ``auth_token`` would silently fall back to the parent's
    ``auth_token`` via ``copy()``'s truthy-or, producing a sub-client with no
    intentional credential set."""
    parent = Anthropic(api_key="parent-key")
    with pytest.raises(ValueError, match="auth_token"):
        _copy_client_with_bearer_auth(parent, auth_token="", helper="environments-work-poller")


@pytest.mark.asyncio()
async def test_async_client_path_clears_api_key_and_sets_bearer() -> None:
    """The same invariants hold for ``AsyncAnthropic`` — verifies the
    ``ClientT`` typevar threads sync/async correctly through ``copy()``."""
    parent = AsyncAnthropic(api_key="parent-key")
    scoped = _copy_client_with_bearer_auth(parent, auth_token="env-key", helper="session-tool-runner")
    assert isinstance(scoped, AsyncAnthropic)
    assert scoped.api_key is None
    assert scoped.auth_token == "env-key"
    assert scoped._custom_headers.get("x-stainless-helper") == "session-tool-runner"


def test_strips_inherited_authorization_from_parent_default_headers() -> None:
    """If the parent client was configured with a custom
    ``default_headers={"Authorization": ...}`` (or ``X-Api-Key``), those would
    otherwise win over the bearer we just set because
    :meth:`AsyncAnthropic.default_headers` merges ``_custom_headers`` after
    ``auth_headers``. The helper strips them from the sub-client's custom
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
    sub-client (via ``httpx.MockTransport``) and inspect the headers actually
    on the wire. Asserts exactly one auth credential is sent — the bearer —
    and the parent's ``X-Api-Key`` doesn't leak.

    This is the surface that the case-mismatch bug fixed by this whole
    refactor lived on. The unit tests above check the sub-client's *state*;
    this one checks the request the SDK builds *from* that state. If a future
    change to ``_build_headers`` reverses the merge order or
    ``_copy_client_with_bearer_auth`` stops stripping the parent's
    ``X-Api-Key``, this is the test that catches it."""
    captured: list[httpx.Request] = []

    async def handler(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return httpx.Response(200, json={"id": "agent_test"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport)
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
    # ``httpx.Headers`` is case-insensitive, so .get() catches any casing.
    assert req.headers.get("authorization") == "Bearer env-key"
    # The parent's ``X-Api-Key`` must NOT be on the wire — that was the bug.
    assert req.headers.get("x-api-key") is None
    # Helper telemetry is on every scoped request.
    assert req.headers.get("x-stainless-helper") == "environments-worker"
