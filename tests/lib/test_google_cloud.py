from __future__ import annotations

import re
import sys
import json
import time
import logging
import pathlib
import threading
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from anthropic._exceptions import AnthropicError
from anthropic.lib.google_cloud import AnthropicGoogleCloud, AsyncAnthropicGoogleCloud, _client as google_cloud_module
from anthropic.lib._extras._common import MissingDependencyError

# httpx normalizes the client base URL with a trailing slash.
DERIVED_BASE_URL = (
    "https://claude.googleapis.com/v1alpha/projects/my-project/locations/us-central1/workspaces/wrkspc_x/invoke/"
)
GLOBAL_DERIVED_BASE_URL = (
    "https://claude.googleapis.com/v1alpha/projects/my-project/locations/global/workspaces/wrkspc_x/invoke/"
)


@pytest.fixture(autouse=True)
def _isolate_environment(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    """Ambient first-party / google-cloud env vars must not leak into these tests."""
    for name in (
        "ANTHROPIC_GOOGLE_CLOUD_PROJECT",
        "ANTHROPIC_GOOGLE_CLOUD_LOCATION",
        "ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID",
        "ANTHROPIC_GOOGLE_CLOUD_BASE_URL",
        "GOOGLE_CLOUD_PROJECT",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL",
        "ANTHROPIC_CUSTOM_HEADERS",
        "ANTHROPIC_WEBHOOK_SIGNING_KEY",
        "ANTHROPIC_CONFIG_DIR",
        "ANTHROPIC_PROFILE",
    ):
        monkeypatch.delenv(name, raising=False)


class _FakeCredentials:
    """Duck-typed stand-in for a `google.auth` Credentials object."""

    def __init__(self, token: str | None, *, expired: bool = False, project_id: str | None = None) -> None:
        self.token = token
        self.expired = expired
        self.project_id = project_id
        self.refresh_calls = 0

    def refresh(self, _request: object) -> None:
        self.refresh_calls += 1
        self.token = "refreshed-token"
        self.expired = False


# ---------------------------------------------------------------------------
# Initialization / base URL / workspace
# ---------------------------------------------------------------------------


class TestAnthropicGoogleCloud:
    def test_init_with_token_provider_and_base_url(self) -> None:
        client = AnthropicGoogleCloud(
            base_url="https://example.test/",
            workspace_id="wrkspc_x",
            token_provider=lambda: "tok",
        )
        assert str(client.base_url) == "https://example.test/"
        assert client.workspace_id == "wrkspc_x"

    def test_explicit_base_url_needs_no_location(self) -> None:
        # No project / location required when base_url is explicit.
        client = AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x")
        assert str(client.base_url) == "https://example.test/"

    def test_base_url_derived_from_project_and_location(self) -> None:
        client = AnthropicGoogleCloud(
            project="my-project",
            location="us-central1",
            workspace_id="wrkspc_x",
            token_provider=lambda: "tok",
        )
        assert str(client.base_url) == DERIVED_BASE_URL

    def test_location_defaults_to_global(self) -> None:
        client = AnthropicGoogleCloud(project="my-project", workspace_id="wrkspc_x", token_provider=lambda: "tok")
        assert str(client.base_url) == GLOBAL_DERIVED_BASE_URL

    def test_missing_project_defers_without_construct_error(self) -> None:
        # The project is back-filled from Google credentials on the first request.
        AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")

    def test_skip_auth_deriving_base_url_requires_project(self) -> None:
        # With skip_auth there are no Google credentials to back-fill the project from.
        with pytest.raises(ValueError, match="project"):
            AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", skip_auth=True)

    def test_skip_auth_deriving_base_url_requires_workspace(self) -> None:
        # The workspace ID is part of the derived URL, so skip_auth alone no longer
        # waives it — only an explicit base_url does.
        with pytest.raises(ValueError, match=r"(?s)workspace_id.*ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID"):
            AnthropicGoogleCloud(project="my-project", skip_auth=True)

    def test_skip_auth_derives_url_with_workspace(self) -> None:
        client = AnthropicGoogleCloud(project="my-project", workspace_id="wrkspc_x", skip_auth=True)
        assert str(client.base_url) == GLOBAL_DERIVED_BASE_URL

    def test_env_resolution(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_GOOGLE_CLOUD_BASE_URL", "https://env.test/")
        monkeypatch.setenv("ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID", "wrkspc_env")
        client = AnthropicGoogleCloud(token_provider=lambda: "tok")
        assert str(client.base_url) == "https://env.test/"
        assert client.workspace_id == "wrkspc_env"

    def test_explicit_project_arg_beats_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_GOOGLE_CLOUD_PROJECT", "env-project")
        client = AnthropicGoogleCloud(
            project="arg-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        assert "/projects/arg-project/" in str(client.base_url)
        assert "env-project" not in str(client.base_url)

    def test_location_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_GOOGLE_CLOUD_LOCATION", "europe-west4")
        client = AnthropicGoogleCloud(project="my-project", workspace_id="wrkspc_x", token_provider=lambda: "tok")
        assert str(client.base_url).startswith("https://claude.googleapis.com/")
        assert "/locations/europe-west4/" in str(client.base_url)

    def test_explicit_location_arg_beats_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_GOOGLE_CLOUD_LOCATION", "env-location")
        client = AnthropicGoogleCloud(
            project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        assert str(client.base_url) == DERIVED_BASE_URL

    def test_project_falls_back_to_google_cloud_project_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "gcp-env-project")
        client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok")
        assert "/projects/gcp-env-project/" in str(client.base_url)

    def test_anthropic_project_env_beats_google_cloud_project(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_GOOGLE_CLOUD_PROJECT", "anthropic-env-project")
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "gcp-env-project")
        client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok")
        assert "/projects/anthropic-env-project/" in str(client.base_url)
        assert "gcp-env-project" not in str(client.base_url)

    def test_workspace_required(self) -> None:
        with pytest.raises(ValueError, match="workspace ID"):
            AnthropicGoogleCloud(base_url="https://example.test/", token_provider=lambda: "tok")

    def test_api_key_and_auth_token_rejected(self) -> None:
        with pytest.raises(TypeError):
            AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x", api_key="sk-ant-x")  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x", auth_token="tok")  # type: ignore[call-arg]

    def test_skip_auth_mutually_exclusive_with_credentials(self) -> None:
        with pytest.raises(ValueError, match="mutually exclusive"):
            AnthropicGoogleCloud(base_url="https://example.test/", skip_auth=True, token_provider=lambda: "tok")
        with pytest.raises(ValueError, match="mutually exclusive"):
            AnthropicGoogleCloud(
                base_url="https://example.test/",
                skip_auth=True,
                credentials=cast(Any, _FakeCredentials(token="tok")),
            )

    def test_project_backfilled_from_explicit_credentials(self) -> None:
        # Service-account-style credentials expose their project; the base URL can
        # then be derived at construction without an explicit `project`.
        creds = _FakeCredentials(token="tok", project_id="creds-project")
        client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", credentials=cast(Any, creds))
        assert "/projects/creds-project/" in str(client.base_url)

    def test_google_credentials_exposed_without_shadowing_base_attribute(self) -> None:
        creds = _FakeCredentials(token="tok")
        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", credentials=cast(Any, creds)
        )
        assert client.google_credentials is creds
        # `.credentials` is the base client's first-party provider slot — never the
        # Google credentials, and never engaged on this client.
        assert client.credentials is None

    def test_completions_is_none(self) -> None:
        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        assert client.completions is None

    def test_full_surface_present(self) -> None:
        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        assert client.messages is not None
        assert client.models is not None
        assert client.beta is not None
        assert client.messages.batches is not None

    def test_no_spurious_env_shadow_warning(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # The base client's "unset ANTHROPIC_API_KEY" credential-precedence warning
        # is about its auto-discovery chain, which never engages for this subclass.
        calls: list[Any] = []

        def _record(**kwargs: object) -> None:
            calls.append(kwargs)

        monkeypatch.setattr("anthropic._client._warn_env_shadow", _record)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-x")
        AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok")
        assert calls == []


# ---------------------------------------------------------------------------
# Auth attachment
# ---------------------------------------------------------------------------


@pytest.mark.respx()
def test_token_provider_attaches_bearer(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(
        base_url="https://example.test/",
        workspace_id="wrkspc_x",
        token_provider=lambda: "provided-token",
    )
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert len(calls) == 1
    req = calls[0].request
    assert req.headers["Authorization"] == "Bearer provided-token"
    # The workspace id travels in the URL path only — never as a header.
    assert "anthropic-workspace-id" not in req.headers


@pytest.mark.respx()
async def test_token_provider_attaches_bearer_async(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    async def provider() -> str:
        return "async-token"

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/",
        workspace_id="wrkspc_x",
        token_provider=provider,
    )
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert len(calls) == 1
    assert calls[0].request.headers["Authorization"] == "Bearer async-token"
    assert "anthropic-workspace-id" not in calls[0].request.headers


@pytest.mark.respx()
async def test_sync_token_provider_on_async_client_runs_off_event_loop(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    offloaded: list[Any] = []
    real_asyncify = google_cloud_module.asyncify

    def spy(fn: Any) -> Any:
        offloaded.append(fn)
        return real_asyncify(fn)

    monkeypatch.setattr("anthropic.lib.google_cloud._client.asyncify", spy)

    def provider() -> str:
        return "sync-token"

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=provider
    )
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer sync-token"
    assert provider in offloaded  # sync providers may block — they must not run inline on the loop


def test_async_token_provider_on_sync_client_rejected_clearly() -> None:
    async def provider() -> str:
        return "tok"

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=cast(Any, provider)
    )
    # Also implicitly asserts no "coroutine was never awaited" RuntimeWarning
    # escapes (filterwarnings=error would fail the test).
    with pytest.raises(AnthropicError, match="AsyncAnthropicGoogleCloud"):
        client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")


@pytest.mark.respx()
def test_credentials_object_attaches_bearer(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    creds = _FakeCredentials(token="cred-token")
    client = AnthropicGoogleCloud(
        base_url="https://example.test/",
        workspace_id="wrkspc_x",
        credentials=cast(Any, creds),
    )
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer cred-token"
    assert creds.refresh_calls == 0  # fresh creds aren't refreshed


@pytest.mark.respx()
def test_expired_credentials_refreshed(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    # Avoid the real google-auth Request import (optional dep, not installed here).
    def _fake_refresh(creds: _FakeCredentials) -> None:
        creds.refresh(None)

    monkeypatch.setattr("anthropic.lib.google_cloud._client._refresh_credentials", _fake_refresh)
    creds = _FakeCredentials(token="stale", expired=True)
    client = AnthropicGoogleCloud(
        base_url="https://example.test/",
        workspace_id="wrkspc_x",
        credentials=cast(Any, creds),
    )
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert creds.refresh_calls == 1
    assert calls[0].request.headers["Authorization"] == "Bearer refreshed-token"


def test_refresh_without_google_auth_raises_actionable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    # `None` in sys.modules makes the import fail even when google-auth is installed.
    monkeypatch.setitem(sys.modules, "google.auth.transport.requests", cast(Any, None))
    with pytest.raises(MissingDependencyError, match=r"anthropic\[google_cloud\]"):
        google_cloud_module._refresh_credentials(cast(Any, _FakeCredentials(token=None)))


@pytest.mark.respx()
def test_adc_path(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    monkeypatch.setattr(
        "anthropic.lib.google_cloud._client._load_adc_credentials",
        lambda: (_FakeCredentials(token="adc-token"), None),
    )
    client = AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x")
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer adc-token"


@pytest.mark.respx()
@pytest.mark.parametrize(
    "kwarg",
    [
        {"token_provider": lambda: "tok"},
        {"credentials": _FakeCredentials(token="tok")},
    ],
    ids=["token_provider", "credentials"],
)
def test_explicit_credential_suppresses_adc(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch, kwarg: dict[str, Any]
) -> None:
    # With any explicit credential source set, ADC discovery must never run.
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    def _fail() -> Any:
        raise AssertionError("ADC discovery must not run when an explicit credential source is set")

    monkeypatch.setattr("anthropic.lib.google_cloud._client._load_adc_credentials", _fail)

    client = AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x", **kwarg)
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer tok"


@pytest.mark.respx()
async def test_explicit_credential_suppresses_adc_async(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    def _fail() -> Any:
        raise AssertionError("ADC discovery must not run when an explicit credential source is set")

    monkeypatch.setattr("anthropic.lib.google_cloud._client._load_adc_credentials", _fail)

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer tok"


def test_concurrent_first_token_resolution_loads_adc_once(monkeypatch: pytest.MonkeyPatch) -> None:
    load_calls = 0

    def slow_load() -> Any:
        nonlocal load_calls
        load_calls += 1
        time.sleep(0.05)
        return _FakeCredentials(token="adc-token"), None

    monkeypatch.setattr("anthropic.lib.google_cloud._client._load_adc_credentials", slow_load)
    client = AnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x")

    tokens: list[str] = []
    threads = [threading.Thread(target=lambda: tokens.append(client._get_token())) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert tokens == ["adc-token"] * 4
    assert load_calls == 1  # the lazy load is serialized, not raced


@pytest.mark.respx()
def test_bearer_token_not_in_debug_logs(respx_mock: MockRouter, caplog: pytest.LogCaptureFixture) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))
    caplog.set_level(logging.DEBUG)

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "super-secret-gcp-token"
    )
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer super-secret-gcp-token"
    assert "super-secret-gcp-token" not in caplog.text


# ---------------------------------------------------------------------------
# Caller-supplied headers win, exactly once, regardless of case / source
# ---------------------------------------------------------------------------


@pytest.mark.respx()
def test_lowercase_authorization_header_respected(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    client.messages.create(
        max_tokens=16,
        messages=[{"role": "user", "content": "hi"}],
        model="claude-haiku-4-5",
        extra_headers={"authorization": "Bearer caller-token"},
    )

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers.get_list("authorization") == ["Bearer caller-token"]


@pytest.mark.respx()
def test_custom_headers_env_flows_through(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    # ANTHROPIC_CUSTOM_HEADERS behaves like it does on other SDK clients.
    monkeypatch.setenv("ANTHROPIC_CUSTOM_HEADERS", "x-custom-header: hello")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert req.headers["x-custom-header"] == "hello"
    assert req.headers["Authorization"] == "Bearer gcp-token"


@pytest.mark.respx()
def test_custom_headers_env_authorization_never_conflicts(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    # An env-supplied Authorization wins under the only-if-absent contract — and
    # exactly one Authorization header goes out, never two conflicting ones.
    monkeypatch.setenv("ANTHROPIC_CUSTOM_HEADERS", "Authorization: Bearer env-token")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers.get_list("authorization") == ["Bearer env-token"]


# ---------------------------------------------------------------------------
# Lazy project back-fill: base URL derived on the first request from the project
# that ADC resolves
# ---------------------------------------------------------------------------

ADC_DERIVED_BASE_URL = (
    "https://claude.googleapis.com/v1alpha/projects/adc-project/locations/us-central1/workspaces/wrkspc_x/invoke/"
)


@pytest.mark.respx()
def test_project_backfilled_from_adc_on_first_request(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    respx_mock.post(re.compile(r"https://claude\.googleapis\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    load_calls = 0

    def fake_load() -> Any:
        nonlocal load_calls
        load_calls += 1
        return _FakeCredentials(token="adc-token"), "adc-project"

    monkeypatch.setattr("anthropic.lib.google_cloud._client._load_adc_credentials", fake_load)

    client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert len(calls) == 2
    for call in calls:
        assert str(call.request.url).startswith(ADC_DERIVED_BASE_URL.rstrip("/"))
        assert call.request.headers["Authorization"] == "Bearer adc-token"
        # The derived URL carries the workspace in its path; still no header.
        assert "anthropic-workspace-id" not in call.request.headers
    assert str(client.base_url) == ADC_DERIVED_BASE_URL
    assert load_calls == 1  # the ADC load (and the back-fill) happens once


@pytest.mark.respx()
def test_backfill_happens_even_with_caller_authorization(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The back-fill is decoupled from token attachment: a first request carrying
    # its own Authorization header must still resolve the deferred base URL.
    respx_mock.post(re.compile(r"https://claude\.googleapis\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )
    monkeypatch.setattr(
        "anthropic.lib.google_cloud._client._load_adc_credentials",
        lambda: (_FakeCredentials(token="adc-token"), "adc-project"),
    )

    client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")
    client.messages.create(
        max_tokens=16,
        messages=[{"role": "user", "content": "hi"}],
        model="claude-haiku-4-5",
        extra_headers={"Authorization": "Bearer caller-token"},
    )

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert str(req.url).startswith(ADC_DERIVED_BASE_URL.rstrip("/"))
    assert req.headers.get_list("authorization") == ["Bearer caller-token"]


def test_adc_without_project_raises_on_first_request(monkeypatch: pytest.MonkeyPatch) -> None:
    # Plain user ADC resolves no project; the error surfaces on the first request.
    monkeypatch.setattr(
        "anthropic.lib.google_cloud._client._load_adc_credentials",
        lambda: (_FakeCredentials(token="adc-token"), None),
    )
    client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")
    with pytest.raises(AnthropicError, match="ANTHROPIC_GOOGLE_CLOUD_PROJECT"):
        client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")


def test_token_provider_without_project_raises_on_first_request() -> None:
    # A token provider bypasses ADC entirely, so there is nothing to back-fill from.
    client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok")
    with pytest.raises(AnthropicError, match="project"):
        client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")


@pytest.mark.respx()
def test_post_construction_base_url_assignment_wins(respx_mock: MockRouter) -> None:
    # Assigning base_url on a deferred-project client cancels the pending back-fill
    # instead of being clobbered (or raising a spurious missing-project error).
    respx_mock.post(re.compile(r"https://my-gateway\.test/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok")
    client.base_url = "https://my-gateway.test/"
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert req.url.host == "my-gateway.test"
    assert req.headers["Authorization"] == "Bearer tok"


@pytest.mark.respx()
def test_copy_of_deferred_client_still_backfills_and_shares_adc(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    respx_mock.post(re.compile(r"https://claude\.googleapis\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )
    load_calls = 0

    def fake_load() -> Any:
        nonlocal load_calls
        load_calls += 1
        return _FakeCredentials(token="adc-token"), "adc-project"

    monkeypatch.setattr("anthropic.lib.google_cloud._client._load_adc_credentials", fake_load)

    client = AnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")
    clone = client.with_options(timeout=10)
    clone.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert len(calls) == 2
    for call in calls:
        assert str(call.request.url).startswith(ADC_DERIVED_BASE_URL.rstrip("/"))
    assert load_calls == 1  # clones share the lazily-loaded ADC credentials


@pytest.mark.respx()
async def test_project_backfilled_from_adc_on_first_request_async(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    respx_mock.post(re.compile(r"https://claude\.googleapis\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )
    monkeypatch.setattr(
        "anthropic.lib.google_cloud._client._load_adc_credentials",
        lambda: (_FakeCredentials(token="adc-token"), "adc-project"),
    )

    client = AsyncAnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert str(calls[0].request.url).startswith(ADC_DERIVED_BASE_URL.rstrip("/"))
    assert "anthropic-workspace-id" not in calls[0].request.headers
    assert str(client.base_url) == ADC_DERIVED_BASE_URL


async def test_adc_without_project_raises_on_first_request_async(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "anthropic.lib.google_cloud._client._load_adc_credentials",
        lambda: (_FakeCredentials(token="adc-token"), None),
    )
    client = AsyncAnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")
    with pytest.raises(AnthropicError, match="ANTHROPIC_GOOGLE_CLOUD_PROJECT"):
        await client.messages.create(
            max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5"
        )


# ---------------------------------------------------------------------------
# copy() / with_options() coherence
# ---------------------------------------------------------------------------


class TestCopy:
    def test_copy_project_rederives_base_url(self) -> None:
        client = AnthropicGoogleCloud(
            project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        clone = client.copy(project="other-project")
        assert "/projects/other-project/" in str(clone.base_url)

    def test_copy_location_rederives_base_url(self) -> None:
        client = AnthropicGoogleCloud(
            project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        clone = client.copy(location="europe-west4")
        assert str(clone.base_url).startswith("https://claude.googleapis.com/")
        assert "/locations/europe-west4/" in str(clone.base_url)

    def test_copy_keeps_user_supplied_base_url(self) -> None:
        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        clone = client.copy(project="other-project")
        assert str(clone.base_url) == "https://example.test/"

    def test_copy_plain_roundtrip_keeps_derived_base_url(self) -> None:
        client = AnthropicGoogleCloud(
            project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        clone = client.copy()
        assert str(clone.base_url) == DERIVED_BASE_URL

    @pytest.mark.respx()
    def test_copy_lower_tier_credential_takes_effect(self, respx_mock: MockRouter) -> None:
        # copy(credentials=...) on a token_provider client must not keep calling
        # the inherited (higher-precedence) provider.
        respx_mock.post(re.compile(r"https://example\.test/.*")).mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        def provider() -> str:
            raise AssertionError("inherited token_provider must not be used after copy(credentials=...)")

        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=provider
        )
        clone = client.copy(credentials=cast(Any, _FakeCredentials(token="cred-token")))
        clone.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

        calls = cast("list[Any]", respx_mock.calls)
        assert calls[0].request.headers["Authorization"] == "Bearer cred-token"

    @pytest.mark.respx()
    def test_copy_token_provider_replaces_credentials(self, respx_mock: MockRouter) -> None:
        respx_mock.post(re.compile(r"https://example\.test/.*")).mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        client = AnthropicGoogleCloud(
            base_url="https://example.test/",
            workspace_id="wrkspc_x",
            credentials=cast(Any, _FakeCredentials(token="stale")),
        )
        clone = client.copy(token_provider=lambda: "fresh-token")
        clone.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

        calls = cast("list[Any]", respx_mock.calls)
        assert calls[0].request.headers["Authorization"] == "Bearer fresh-token"

    @pytest.mark.respx()
    def test_copy_skip_auth_clears_workspace_and_credentials(self, respx_mock: MockRouter) -> None:
        # The documented pre-authenticated-proxy derivation: no bearer, and the
        # workspace ID is clearable on the clone.
        respx_mock.post(re.compile(r"https://proxy\.test/.*")).mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        proxy = client.copy(skip_auth=True, workspace_id=None, base_url="https://proxy.test/")
        proxy.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

        calls = cast("list[Any]", respx_mock.calls)
        req = calls[0].request
        assert "Authorization" not in req.headers
        assert "anthropic-workspace-id" not in req.headers

    def test_copy_workspace_required_when_cleared_without_skip_auth(self) -> None:
        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        with pytest.raises(ValueError, match="workspace ID"):
            client.copy(workspace_id=None)

    def test_copy_rejects_first_party_kwargs(self) -> None:
        client = AnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        with pytest.raises(TypeError):
            client.copy(auth_token="environment-key")  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            client.copy(api_key="sk-ant-x")  # type: ignore[call-arg]

    def test_async_copy_parity(self) -> None:
        client = AsyncAnthropicGoogleCloud(
            project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        clone = client.copy(project="other-project")
        assert "/projects/other-project/" in str(clone.base_url)
        proxy = client.copy(skip_auth=True, workspace_id=None, base_url="https://proxy.test/")
        assert proxy.workspace_id is None
        with pytest.raises(TypeError):
            client.copy(auth_token="environment-key")  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# skip_auth
# ---------------------------------------------------------------------------


@pytest.mark.respx()
def test_skip_auth_sends_neither_header(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(base_url="https://example.test/", skip_auth=True)
    assert client.workspace_id is None
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert "Authorization" not in req.headers
    assert "anthropic-workspace-id" not in req.headers


# ---------------------------------------------------------------------------
# Credential isolation: the first-party ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN /
# ANTHROPIC_BASE_URL environment variables and the base SDK credential-discovery
# chain must never affect requests made by this client.
# ---------------------------------------------------------------------------


@pytest.mark.respx()
def test_no_api_key_leak(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-leak")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    assert client.api_key is None
    assert client.auth_headers == {}
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert "x-api-key" not in {k.lower() for k in req.headers.keys()}
    assert req.headers["Authorization"] == "Bearer tok"


@pytest.mark.respx()
async def test_no_api_key_leak_async(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-leak")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    assert client.api_key is None
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert "x-api-key" not in {k.lower() for k in req.headers.keys()}


@pytest.mark.respx()
def test_no_auth_token_leak(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    # An ANTHROPIC_AUTH_TOKEN in the env must never become the Authorization header —
    # the bearer token sent is always the one this client resolved itself.
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "first-party-leak")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    assert client.auth_token is None
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer gcp-token"


@pytest.mark.respx()
async def test_no_auth_token_leak_async(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "first-party-leak")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    assert client.auth_token is None
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert calls[0].request.headers["Authorization"] == "Bearer gcp-token"


@pytest.mark.respx()
def test_env_base_url_does_not_override_derived_url(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    # ANTHROPIC_BASE_URL configures the first-party client only; the gateway URL
    # derived from project/location always wins here.
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://first-party.test/")
    respx_mock.post(re.compile(r"https://claude\.googleapis\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    client = AnthropicGoogleCloud(
        project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    assert str(client.base_url) == DERIVED_BASE_URL
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    assert str(calls[0].request.url).startswith(DERIVED_BASE_URL.rstrip("/"))


async def test_env_base_url_does_not_override_derived_url_async(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://first-party.test/")
    client = AsyncAnthropicGoogleCloud(
        project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    assert str(client.base_url) == DERIVED_BASE_URL


def _assert_credential_chain_off(client: AnthropicGoogleCloud | AsyncAnthropicGoogleCloud) -> None:
    from anthropic._client import _is_base_client

    assert _is_base_client(client) is False
    assert client.credentials is None
    assert client.api_key is None
    assert client.auth_token is None


def test_base_credential_chain_never_engages(monkeypatch: pytest.MonkeyPatch) -> None:
    # The base client's credential auto-discovery (profiles / workload identity /
    # token cache) is gated on `_is_base_client()`; pin that it never runs for
    # this subclass even when no other credential source is configured.
    def _fail(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("base credential-discovery chain must not engage for AnthropicGoogleCloud")

    monkeypatch.setattr("anthropic._client.default_credentials", _fail)

    client = AnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    _assert_credential_chain_off(client)


async def test_base_credential_chain_never_engages_async(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("base credential-discovery chain must not engage for AsyncAnthropicGoogleCloud")

    monkeypatch.setattr("anthropic._client.default_credentials", _fail)

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
    )
    _assert_credential_chain_off(client)


@pytest.fixture
def profile_config_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    """A fully-resolvable Anthropic profile (config + oauth credentials + base_url)
    that the base client's credential chain would adopt if it ever ran."""
    (tmp_path / "configs").mkdir()
    (tmp_path / "credentials").mkdir()
    (tmp_path / "configs" / "default.json").write_text(
        json.dumps(
            {
                "version": "1.0",
                "organization_id": "org_profile_should_not_leak",
                "base_url": "https://profile-gateway.example.com",
                "authentication": {"type": "user_oauth"},
            }
        )
    )
    (tmp_path / "credentials" / "default.json").write_text(
        json.dumps(
            {
                "version": "1.0",
                "type": "oauth_token",
                "access_token": "profile-oauth-token-should-not-leak",
                "refresh_token": "profile-refresh-token",
                "expires_at": 4102444800000,
            }
        )
    )
    return tmp_path


@pytest.mark.respx()
def test_resolvable_profile_cannot_leak(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch, profile_config_dir: pathlib.Path
) -> None:
    # An ANTHROPIC_PROFILE / ANTHROPIC_CONFIG_DIR pointing at a real on-disk profile
    # must not be able to attach its base_url or oauth token to this client's requests.
    monkeypatch.setenv("ANTHROPIC_CONFIG_DIR", str(profile_config_dir))
    monkeypatch.setenv("ANTHROPIC_PROFILE", "default")
    respx_mock.post(re.compile(r"https://claude\.googleapis\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    client = AnthropicGoogleCloud(
        project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    _assert_credential_chain_off(client)
    client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert req.url.host == "claude.googleapis.com"
    assert "profile-gateway.example.com" not in str(req.url)
    assert req.headers.get_list("authorization") == ["Bearer gcp-token"]
    assert "profile-oauth-token-should-not-leak" not in repr(req.headers)


@pytest.mark.respx()
async def test_resolvable_profile_cannot_leak_async(
    respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch, profile_config_dir: pathlib.Path
) -> None:
    monkeypatch.setenv("ANTHROPIC_CONFIG_DIR", str(profile_config_dir))
    monkeypatch.setenv("ANTHROPIC_PROFILE", "default")
    respx_mock.post(re.compile(r"https://example\.test/.*")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    client = AsyncAnthropicGoogleCloud(
        base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "gcp-token"
    )
    _assert_credential_chain_off(client)
    await client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "hi"}], model="claude-haiku-4-5")

    calls = cast("list[Any]", respx_mock.calls)
    req = calls[0].request
    assert req.headers.get_list("authorization") == ["Bearer gcp-token"]
    assert "profile-oauth-token-should-not-leak" not in repr(req.headers)


# ---------------------------------------------------------------------------
# Async init parity
# ---------------------------------------------------------------------------


class TestAsyncAnthropicGoogleCloud:
    async def test_workspace_required(self) -> None:
        with pytest.raises(ValueError, match="workspace ID"):
            AsyncAnthropicGoogleCloud(base_url="https://example.test/", token_provider=lambda: "tok")

    async def test_api_key_and_auth_token_rejected(self) -> None:
        with pytest.raises(TypeError):
            AsyncAnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x", api_key="sk-ant-x")  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            AsyncAnthropicGoogleCloud(base_url="https://example.test/", workspace_id="wrkspc_x", auth_token="tok")  # type: ignore[call-arg]

    async def test_skip_auth_mutually_exclusive_with_credentials(self) -> None:
        with pytest.raises(ValueError, match="mutually exclusive"):
            AsyncAnthropicGoogleCloud(base_url="https://example.test/", skip_auth=True, token_provider=lambda: "tok")

    async def test_completions_is_none(self) -> None:
        client = AsyncAnthropicGoogleCloud(
            base_url="https://example.test/", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        assert client.completions is None

    async def test_base_url_derived(self) -> None:
        client = AsyncAnthropicGoogleCloud(
            project="my-project", location="us-central1", workspace_id="wrkspc_x", token_provider=lambda: "tok"
        )
        assert str(client.base_url) == DERIVED_BASE_URL

    async def test_location_defaults_to_global(self) -> None:
        client = AsyncAnthropicGoogleCloud(project="my-project", workspace_id="wrkspc_x", token_provider=lambda: "tok")
        assert str(client.base_url) == GLOBAL_DERIVED_BASE_URL

    async def test_missing_project_defers_without_construct_error(self) -> None:
        AsyncAnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x")

    async def test_skip_auth_deriving_base_url_requires_project(self) -> None:
        with pytest.raises(ValueError, match="project"):
            AsyncAnthropicGoogleCloud(location="us-central1", workspace_id="wrkspc_x", skip_auth=True)

    async def test_skip_auth_deriving_base_url_requires_workspace(self) -> None:
        with pytest.raises(ValueError, match=r"(?s)workspace_id.*ANTHROPIC_GOOGLE_CLOUD_WORKSPACE_ID"):
            AsyncAnthropicGoogleCloud(project="my-project", skip_auth=True)

    async def test_skip_auth_derives_url_with_workspace(self) -> None:
        client = AsyncAnthropicGoogleCloud(project="my-project", workspace_id="wrkspc_x", skip_auth=True)
        assert str(client.base_url) == GLOBAL_DERIVED_BASE_URL
