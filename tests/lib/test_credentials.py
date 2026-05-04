from __future__ import annotations

import os
import json
import time
import logging
import pathlib
from typing import Any, Dict, List, Optional, cast
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

import anthropic
from anthropic import (
    EnvToken,
    Anthropic,
    TokenCache,
    AccessToken,
    StaticToken,
    AnthropicError,
    AsyncAnthropic,
    InMemoryConfig,
    CredentialsFile,
    IdentityTokenFile,
    WorkloadIdentityError,
    WorkloadIdentityCredentials,
    default_credentials,
    exchange_federation_assertion,
)
from anthropic._version import __version__
from anthropic._base_client import FinalRequestOptions
from anthropic.lib.credentials._constants import (
    TOKEN_ENDPOINT,
    GRANT_TYPE_JWT_BEARER,
    OAUTH_API_BETA_HEADER,
    FEDERATION_BETA_HEADER,
)

BASE_URL = "https://api.anthropic.com"
TOKEN_URL = f"{BASE_URL}{TOKEN_ENDPOINT}"

_ALL_ENV = [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_CONFIG_DIR",
    "ANTHROPIC_PROFILE",
    "ANTHROPIC_IDENTITY_TOKEN",
    "ANTHROPIC_IDENTITY_TOKEN_FILE",
    "ANTHROPIC_FEDERATION_RULE_ID",
    "ANTHROPIC_ORGANIZATION_ID",
    "ANTHROPIC_SERVICE_ACCOUNT_ID",
    "ANTHROPIC_SCOPE",
]


class MockRequestCall(Protocol):
    request: httpx.Request


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    for var in _ALL_ENV:
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


@pytest.fixture
def no_default_creds_file(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    """Point the config directory at an empty location so a real
    ~/.config/anthropic/ on the dev machine doesn't leak into tests.

    Patches ``_config_dir`` directly rather than setting ``ANTHROPIC_CONFIG_DIR``
    so that ``clean_env`` (which deletes that env var) can't clobber the isolation.
    """
    empty = tmp_path / "empty-config-dir"
    empty.mkdir()
    monkeypatch.setattr("anthropic.lib.credentials._constants._config_dir", lambda: empty)


# Field names that live at the top level of the new nested config shape
# (outside the ``authentication`` object).
_TOP_LEVEL_CONFIG_KEYS = {"base_url", "organization_id", "workspace_id"}


def _migrate_legacy_config(flat: Dict[str, Any]) -> Dict[str, Any]:
    """Adapter: convert a flat legacy config dict into the new nested shape.

    Many tests in this file predate the schema migration and pass legacy
    flat configs like ``{"type": "workload_identity", "federation_rule_id": ...}``.
    Rather than churn every caller, this helper translates at the test-helper
    layer — tests that want to assert against the new shape directly can
    pass a config dict that already contains an ``"authentication"`` key.
    """
    result: Dict[str, Any] = {}
    auth: Dict[str, Any] = {}
    for key, value in flat.items():
        if key == "type":
            continue
        if key in _TOP_LEVEL_CONFIG_KEYS:
            result[key] = value
        else:
            auth[key] = value

    # "external" used to mean "token already in credentials file, no
    # refresh" — the new schema expresses this as user_oauth without a
    # client_id (the key "external → user_oauth" both preserves the daemon
    # semantics and keeps auth-only fields like credentials_path intact).
    # "workload_identity" / "authorized_user" were renamed.
    auth["type"] = {
        "external": "user_oauth",
        "workload_identity": "oidc_federation",
        "authorized_user": "user_oauth",
    }.get(flat["type"], flat["type"])

    result["authentication"] = auth
    return result


def _write_profile(
    config_dir: pathlib.Path,
    profile: str,
    config: Dict[str, Any],
    credentials: Optional[Dict[str, Any]] = None,
) -> None:
    """Test helper: lay out ``configs/<profile>.json`` and optionally
    ``credentials/<profile>.json`` under ``config_dir``.

    Accepts either the new nested ``{"authentication": {...}}`` shape or a
    legacy flat shape (``{"type": "workload_identity", ...}``) for backwards
    compatibility with the tests that predate the schema migration. Legacy
    inputs are translated via :func:`_migrate_legacy_config` before being
    written to disk.

    Prepends ``"type": "oauth_token"`` to the credentials dict unless the
    caller already supplied a ``type`` key (so negative tests can override).
    """
    if "type" in config and "authentication" not in config:
        config = _migrate_legacy_config(config)
    (config_dir / "configs").mkdir(parents=True, exist_ok=True)
    (config_dir / "configs" / f"{profile}.json").write_text(json.dumps(config))
    if credentials is not None:
        if "type" not in credentials:
            credentials = {"type": "oauth_token", **credentials}
        (config_dir / "credentials").mkdir(parents=True, exist_ok=True)
        creds_path = config_dir / "credentials" / f"{profile}.json"
        creds_path.write_text(json.dumps(credentials))
        # Match the 0o600 invariant the real credentials reader now enforces.
        creds_path.chmod(0o600)


# --------------------------------------------------------------------------- #
# Basic providers
# --------------------------------------------------------------------------- #


class TestAccessToken:
    def test_defaults(self) -> None:
        tok = AccessToken("abc")
        assert tok.token == "abc"
        assert tok.expires_at is None

    def test_with_expiry(self) -> None:
        tok = AccessToken("abc", expires_at=123)
        assert tok.expires_at == 123


class TestStaticToken:
    def test_returns_token(self) -> None:
        p = StaticToken("sk-ant-oat01-static")
        assert p() == AccessToken("sk-ant-oat01-static", None)
        assert p().expires_at is None


class TestEnvToken:
    def test_reads_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "env-token")
        assert EnvToken()().token == "env-token"

    def test_raises_when_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
        with pytest.raises(AnthropicError, match="ANTHROPIC_AUTH_TOKEN"):
            EnvToken()()


class TestIdentityTokenFile:
    def test_rereads_on_each_call(self, tmp_path: pathlib.Path) -> None:
        f = tmp_path / "token"
        f.write_text("jwt-one\n")
        provider = IdentityTokenFile(f)
        assert provider() == "jwt-one"

        f.write_text("jwt-two\n")
        assert provider() == "jwt-two"

    def test_reads_env_var_path(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        f = tmp_path / "token"
        f.write_text("from-env")
        monkeypatch.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(f))
        assert IdentityTokenFile()() == "from-env"

    def test_raises_when_no_path(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_IDENTITY_TOKEN_FILE", raising=False)
        with pytest.raises(AnthropicError, match="ANTHROPIC_IDENTITY_TOKEN_FILE"):
            IdentityTokenFile()

    def test_raises_when_file_missing(self, tmp_path: pathlib.Path) -> None:
        with pytest.raises(AnthropicError, match="not found"):
            IdentityTokenFile(tmp_path / "nope")()


class TestCredentialsFile:
    """All tests use ``ANTHROPIC_CONFIG_DIR`` to point at a tmp directory laid
    out as ``configs/<profile>.json`` + ``credentials/<profile>.json``."""

    @pytest.fixture(autouse=True)
    def _isolate(self, monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        for var in _ALL_ENV:
            monkeypatch.delenv(var, raising=False)
        monkeypatch.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))

    # -- "type": "external" ------------------------------------------------

    def test_external(self, tmp_path: pathlib.Path) -> None:
        _write_profile(
            tmp_path,
            "default",
            config={"type": "external"},
            credentials={"access_token": "sk-ant-oat01-x", "expires_at": 1775000000},
        )
        tok = CredentialsFile()()
        assert tok.token == "sk-ant-oat01-x"
        assert tok.expires_at == 1775000000

    def test_external_no_expiry(self, tmp_path: pathlib.Path) -> None:
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "sk-ant-oat01-x"})
        assert CredentialsFile()().expires_at is None

    def test_external_rereads_credentials_on_each_call(self, tmp_path: pathlib.Path) -> None:
        """An external process rotates the credentials file; config stays fixed."""
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "first"})
        provider = CredentialsFile()
        assert provider().token == "first"

        # External rotation: rewrite credentials only.
        (tmp_path / "credentials" / "default.json").write_text(json.dumps({"access_token": "second"}))
        assert provider().token == "second"

    def test_external_missing_credentials_file(self, tmp_path: pathlib.Path) -> None:
        _write_profile(tmp_path, "default", {"type": "external"})  # no credentials file
        with pytest.raises(AnthropicError, match="Credentials file not found"):
            CredentialsFile()()

    def test_credentials_file_wrong_type_raises(self, tmp_path: pathlib.Path) -> None:
        _write_profile(
            tmp_path,
            "default",
            config={"type": "external"},
            credentials={"type": "something_else", "access_token": "x"},
        )
        with pytest.raises(
            AnthropicError,
            match="credentials file has type 'something_else'; expected 'oauth_token' for authentication.type 'user_oauth'",
        ):
            CredentialsFile()()

    def test_credentials_file_absent_type_is_lenient(self, tmp_path: pathlib.Path) -> None:
        """Hand-written credentials files without ``type`` are accepted."""
        _write_profile(tmp_path, "default", {"type": "external"})
        # Write credentials directly (bypass helper's type injection).
        (tmp_path / "credentials").mkdir(exist_ok=True)
        creds_path = tmp_path / "credentials" / "default.json"
        creds_path.write_text(json.dumps({"access_token": "no-type-field"}))
        creds_path.chmod(0o600)
        assert CredentialsFile()().token == "no-type-field"

    def test_unrecognized_top_level_keys_ignored(self, tmp_path: pathlib.Path) -> None:
        """Unknown top-level keys in both files are silently ignored (forward compat)."""
        _write_profile(
            tmp_path,
            "default",
            config={
                "type": "external",
                "_note": "test comment",
                "future_field": 123,
                "nested_future": {"a": [1, 2]},
            },
            credentials={
                "access_token": "tolerant",
                "expires_at": 1775000000,
                "_note": "creds comment",
                "future_field": 123,
            },
        )
        tok = CredentialsFile()()
        assert tok.token == "tolerant"
        assert tok.expires_at == 1775000000

    # -- "type": "workload_identity" --------------------------------------

    @pytest.mark.respx(base_url=BASE_URL)
    def test_workload_identity_dispatch(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt-from-file")

        # workload_identity needs no credentials file — config is sufficient.
        _write_profile(
            tmp_path,
            "default",
            config={
                "type": "workload_identity",
                "identity_token": {"source": "file", "path": str(jwt_path)},
                "federation_rule_id": "fdrl_file",
                "organization_id": "org-from-file",
                "service_account_id": "svac_file",
            },
        )

        token_route = respx_mock.post(TOKEN_ENDPOINT).mock(
            return_value=httpx.Response(200, json={"access_token": "exch_tok", "expires_in": 3600})
        )

        provider = CredentialsFile()
        tok = provider()
        assert tok.token == "exch_tok"
        assert tok.expires_at is not None and tok.expires_at > time.time()

        assert token_route.call_count == 1
        body = json.loads(cast("list[MockRequestCall]", token_route.calls)[0].request.content)
        assert body["grant_type"] == GRANT_TYPE_JWT_BEARER
        assert body["assertion"] == "ext-jwt-from-file"
        assert body["federation_rule_id"] == "fdrl_file"
        assert body["organization_id"] == "org-from-file"
        assert body["service_account_id"] == "svac_file"
        assert "scope" not in body

        # Disk cache: the exchange wrote credentials/<profile>.json with 0600
        # perms, so the second call returns the cached token without hitting
        # the network. Delegate is still cached on the provider.
        provider()
        assert token_route.call_count == 1
        assert provider._workload_delegate is not None  # pyright: ignore[reportPrivateUsage]
        cached = json.loads((tmp_path / "credentials" / "default.json").read_text())
        assert cached["version"] == "1.0"
        assert cached["type"] == "oauth_token"
        assert cached["access_token"] == "exch_tok"
        assert isinstance(cached["expires_at"], int)

    @pytest.mark.respx()
    def test_bind_base_url_precedence(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """``bind_base_url`` slots between the config file's own ``base_url``
        field and the hard-coded default: config → bound → default."""
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("j")
        bound = "https://bound.example"

        def write(profile: str, *, with_base_url: Optional[str]) -> None:
            cfg: Dict[str, Any] = {
                "type": "workload_identity",
                "identity_token": {"source": "file", "path": str(jwt_path)},
                "federation_rule_id": "fdrl_x",
                "organization_id": "org",
            }
            if with_base_url is not None:
                cfg["base_url"] = with_base_url
            _write_profile(tmp_path, profile, config=cfg)

        # config omits base_url, no bind → DEFAULT_BASE_URL
        write("p0", with_base_url=None)
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60}))
        CredentialsFile("p0")()
        assert str(cast("list[MockRequestCall]", respx_mock.calls)[-1].request.url) == TOKEN_URL

        # config omits base_url + bound → bound
        write("p1", with_base_url=None)
        respx_mock.post(f"{bound}{TOKEN_ENDPOINT}").mock(
            return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60})
        )
        creds = CredentialsFile("p1")
        creds.bind_base_url(bound)
        creds()
        assert str(cast("list[MockRequestCall]", respx_mock.calls)[-1].request.url) == f"{bound}{TOKEN_ENDPOINT}"

        # config has base_url + bound → config wins
        write("p2", with_base_url="https://from-config.example")
        respx_mock.post(f"https://from-config.example{TOKEN_ENDPOINT}").mock(
            return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60})
        )
        creds = CredentialsFile("p2")
        creds.bind_base_url(bound)
        creds()
        assert (
            str(cast("list[MockRequestCall]", respx_mock.calls)[-1].request.url)
            == f"https://from-config.example{TOKEN_ENDPOINT}"
        )

        # re-entrancy: bind_base_url called *after* _load_config() re-resolves
        # in place — the last bind wins when the config file doesn't pin a host.
        write("p3", with_base_url=None)
        creds = CredentialsFile("p3")
        creds.extra_headers()  # forces _load_config()
        creds.bind_base_url("https://first.example")
        creds.bind_base_url("https://second.example")
        assert creds._base_url == "https://second.example"  # type: ignore[attr-defined]
        # eager scheme validation — http:// rejected at bind time, before load
        with pytest.raises(AnthropicError, match="https"):
            CredentialsFile("p3").bind_base_url("http://evil.example")

    @pytest.mark.respx(base_url=BASE_URL)
    def test_workload_identity_disk_cache_stale_reexchange(
        self, respx_mock: MockRouter, tmp_path: pathlib.Path
    ) -> None:
        """A stale on-disk credentials file is ignored — fresh exchange happens
        and the file is rewritten."""
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt")
        _write_profile(
            tmp_path,
            "default",
            config={
                "type": "workload_identity",
                "identity_token": {"source": "file", "path": str(jwt_path)},
                "federation_rule_id": "fdrl_x",
                "organization_id": "org_x",
            },
            credentials={"access_token": "stale-tok", "expires_at": int(time.time()) - 1},
        )
        token_route = respx_mock.post(TOKEN_ENDPOINT).mock(
            return_value=httpx.Response(200, json={"access_token": "fresh-tok", "expires_in": 600})
        )
        tok = CredentialsFile()()
        assert tok.token == "fresh-tok"
        assert token_route.call_count == 1
        rewritten = json.loads((tmp_path / "credentials" / "default.json").read_text())
        assert rewritten["access_token"] == "fresh-tok"

    @pytest.mark.respx(base_url=BASE_URL)
    def test_workload_identity_disk_cache_corrupt_expires_at_reexchange(
        self, respx_mock: MockRouter, tmp_path: pathlib.Path
    ) -> None:
        """A non-numeric expires_at in the on-disk credentials file falls
        through to re-exchange instead of raising."""
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt")
        _write_profile(
            tmp_path,
            "default",
            config={
                "type": "workload_identity",
                "identity_token": {"source": "file", "path": str(jwt_path)},
                "federation_rule_id": "fdrl_x",
                "organization_id": "org_x",
            },
            credentials={"access_token": "stale-tok", "expires_at": "not-a-number"},
        )
        token_route = respx_mock.post(TOKEN_ENDPOINT).mock(
            return_value=httpx.Response(200, json={"access_token": "fresh-tok", "expires_in": 600})
        )
        tok = CredentialsFile()()
        assert tok.token == "fresh-tok"
        assert token_route.call_count == 1

    def test_workload_identity_missing_required_fields(self, tmp_path: pathlib.Path) -> None:
        _write_profile(tmp_path, "default", {"type": "workload_identity", "federation_rule_id": "fdrl_x"})
        with pytest.raises(
            WorkloadIdentityError, match="'authentication.federation_rule_id' and top-level 'organization_id'"
        ):
            CredentialsFile()()

    @pytest.mark.respx(base_url=BASE_URL)
    def test_workload_delegate_borrows_parent_http_client(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """The workload delegate must borrow CredentialsFile's owned httpx.Client
        rather than creating its own. CredentialsFile.close() then has a single
        client to release; if a refactor regresses this and the delegate creates
        its own pool, this test catches it before close() starts leaking sockets."""
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt")
        _write_profile(
            tmp_path,
            "default",
            config={
                "type": "workload_identity",
                "identity_token": {"source": "file", "path": str(jwt_path)},
                "federation_rule_id": "fdrl_x",
                "organization_id": "00000000-0000-0000-0000-000000000000",
            },
        )
        respx_mock.post(TOKEN_ENDPOINT).mock(
            return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60})
        )
        provider = CredentialsFile()
        provider()
        delegate = provider._workload_delegate  # pyright: ignore[reportPrivateUsage]
        assert delegate is not None
        # The delegate must NOT own its httpx.Client — that would mean we have
        # two pools to track and close().
        assert delegate._owns_http_client is False  # pyright: ignore[reportPrivateUsage]
        # Both objects share the same client instance.
        assert delegate._http_client is provider._get_http_client()  # pyright: ignore[reportPrivateUsage]
        provider.close()

    def test_workload_identity_unknown_source_raises(self, tmp_path: pathlib.Path) -> None:
        _write_profile(
            tmp_path,
            "default",
            {
                "type": "workload_identity",
                "federation_rule_id": "f",
                "organization_id": "o",
                "identity_token": {"source": "url", "url": "https://example.com/token"},
            },
        )
        with pytest.raises(AnthropicError, match="identity_token source 'url' is not supported"):
            CredentialsFile()()

    def test_workload_identity_token_omitted_uses_env(
        self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("via-env-chain")
        monkeypatch.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(jwt_path))

        _write_profile(
            tmp_path, "default", {"type": "workload_identity", "federation_rule_id": "f", "organization_id": "o"}
        )

        provider = CredentialsFile()
        # Building the delegate succeeds (provider resolved via env); we don't
        # need to exercise the HTTP call here.
        provider._load_config()  # pyright: ignore[reportPrivateUsage]
        delegate = provider._build_workload_delegate(  # pyright: ignore[reportPrivateUsage]
            provider._auth_block()  # pyright: ignore[reportPrivateUsage]
        )
        assert delegate._identity_token_provider() == "via-env-chain"  # pyright: ignore[reportPrivateUsage]

    # -- "type": "authorized_user" ----------------------------------------

    @pytest.mark.respx(base_url=BASE_URL)
    def test_authorized_user_refresh_and_writeback(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """Refresh writes back to credentials/ only — configs/ stays untouched."""
        _write_profile(
            tmp_path,
            "default",
            config={"type": "authorized_user", "client_id": "cid", "scope": "x:y"},
            credentials={
                "access_token": "old-tok",
                "expires_at": int(time.time()) - 1,
                "refresh_token": "refresh-old",
            },
        )

        refresh_route = respx_mock.post(TOKEN_ENDPOINT).mock(
            return_value=httpx.Response(
                200, json={"access_token": "new-tok", "expires_in": 3600, "refresh_token": "refresh-new"}
            )
        )

        tok = CredentialsFile()()
        assert tok.token == "new-tok"
        assert tok.expires_at is not None and tok.expires_at > time.time()

        assert refresh_route.call_count == 1
        body = json.loads(cast("list[MockRequestCall]", refresh_route.calls)[0].request.content)
        assert body == {"grant_type": "refresh_token", "refresh_token": "refresh-old", "client_id": "cid"}

        # Credentials file was rewritten — expires_at is unix int seconds
        creds_file = tmp_path / "credentials" / "default.json"
        rewritten = json.loads(creds_file.read_text())
        assert rewritten["version"] == "1.0"
        assert rewritten["type"] == "oauth_token"
        assert rewritten["access_token"] == "new-tok"
        assert rewritten["refresh_token"] == "refresh-new"
        assert isinstance(rewritten["expires_at"], int)
        assert rewritten["expires_at"] > time.time()
        assert not creds_file.with_suffix(".json.tmp").exists()

        # Config file was NOT touched
        config_after = json.loads((tmp_path / "configs" / "default.json").read_text())
        assert config_after == {
            "authentication": {
                "type": "user_oauth",
                "client_id": "cid",
                "scope": "x:y",
            }
        }

    def test_authorized_user_fresh_token_no_refresh(self, tmp_path: pathlib.Path) -> None:
        _write_profile(
            tmp_path,
            "default",
            config={"type": "authorized_user"},
            credentials={
                "access_token": "still-good",
                "expires_at": int(time.time()) + 3600,
                "refresh_token": "refresh-old",
            },
        )
        tok = CredentialsFile()()
        assert tok.token == "still-good"

    @pytest.mark.respx(base_url=BASE_URL)
    def test_authorized_user_refresh_failure(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        _write_profile(
            tmp_path,
            "default",
            config={"type": "authorized_user", "client_id": "cid"},
            credentials={"access_token": "old", "expires_at": int(time.time()) - 1, "refresh_token": "rt"},
        )
        respx_mock.post(TOKEN_ENDPOINT).mock(return_value=httpx.Response(400, json={"error": "invalid_grant"}))
        with pytest.raises(WorkloadIdentityError, match="refresh failed"):
            CredentialsFile()()

    def test_user_oauth_without_client_id_is_static(self, tmp_path: pathlib.Path) -> None:
        """user_oauth without a client_id is the ``external`` pattern: the
        credentials file is externally rotated, the SDK re-reads it on every
        call, no refresh grant is attempted. The spec merged this use case
        into user_oauth — a client_id is the opt-in signal for refresh."""
        _write_profile(
            tmp_path,
            "default",
            config={"type": "authorized_user"},  # migrates to user_oauth, no client_id
            credentials={
                "access_token": "daemon-minted",
                "expires_at": int(time.time()) + 3600,
            },
        )
        tok = CredentialsFile()()
        assert tok.token == "daemon-minted"

    @pytest.mark.respx(base_url=BASE_URL)
    def test_authorized_user_refresh_beta_headers(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """refresh_token POST must carry oauth-2025-04-20 (unlocks the token
        endpoint family) but NOT oidc-federation-2026-04-01 (that header is a
        routing switch that would send this POST to the Go userauth handler,
        which only accepts jwt-bearer grants)."""
        _write_profile(
            tmp_path,
            "default",
            config={"type": "authorized_user", "client_id": "cid"},
            credentials={
                "access_token": "old",
                "expires_at": int(time.time()) - 1,
                "refresh_token": "refresh-old",
            },
        )
        refresh_route = respx_mock.post(TOKEN_ENDPOINT).mock(
            return_value=httpx.Response(200, json={"access_token": "new-tok", "expires_in": 3600})
        )
        CredentialsFile()()
        req = cast("list[MockRequestCall]", refresh_route.calls)[0].request
        beta_flags = {f.strip() for f in req.headers["anthropic-beta"].split(",")}
        assert OAUTH_API_BETA_HEADER in beta_flags
        assert FEDERATION_BETA_HEADER not in beta_flags
        assert req.headers["User-Agent"] == f"anthropic-python/{__version__}"

    def test_user_oauth_with_client_id_missing_refresh_token(self, tmp_path: pathlib.Path) -> None:
        """A user_oauth profile that has a client_id (refresh mode) but no
        refresh_token in the credentials file can't actually refresh — raise
        a clear error rather than 401-looping."""
        _write_profile(
            tmp_path,
            "default",
            config={"type": "authorized_user", "client_id": "cid"},
            credentials={"access_token": "x", "expires_at": int(time.time()) - 1},
        )
        with pytest.raises(WorkloadIdentityError, match="'refresh_token'"):
            CredentialsFile()()

    # -- common error paths -----------------------------------------------

    def test_unknown_type(self, tmp_path: pathlib.Path) -> None:
        _write_profile(tmp_path, "default", {"type": "mystery"})
        with pytest.raises(AnthropicError, match="Unknown authentication.type"):
            CredentialsFile()()

    def test_missing_config_file(self, tmp_path: pathlib.Path) -> None:
        # configs/ dir exists but profile file doesn't
        (tmp_path / "configs").mkdir()
        with pytest.raises(AnthropicError, match="Config file not found"):
            CredentialsFile("nonexistent")()

    def test_default_credentials_explicit_env_propagates_error(
        self, tmp_path: pathlib.Path, clean_env: pytest.MonkeyPatch
    ) -> None:
        """When ANTHROPIC_PROFILE or ANTHROPIC_CONFIG_DIR is set explicitly, a
        broken config file surfaces immediately — not swallowed into a 'no auth
        configured' misdirection."""
        clean_env.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))
        clean_env.setenv("ANTHROPIC_PROFILE", "broken")
        (tmp_path / "configs").mkdir()
        (tmp_path / "configs" / "broken.json").write_text("this is not JSON")
        with pytest.raises(AnthropicError, match="not valid JSON"):
            default_credentials()

    # -- security: HTTPS enforcement --------------------------------------

    def test_config_base_url_http_rejected(self, tmp_path: pathlib.Path) -> None:
        """A config file that specifies base_url=http://evil is rejected so a
        malicious config can't exfiltrate the assertion or refresh token."""
        _write_profile(
            tmp_path,
            "default",
            {"type": "external", "base_url": "http://evil.example.com"},
            {"access_token": "x"},
        )
        with pytest.raises(AnthropicError, match="must use https"):
            CredentialsFile()()

    def test_config_base_url_localhost_http_allowed(self, tmp_path: pathlib.Path) -> None:
        """Localhost HTTP is allowed for local oauth_server testing."""
        _write_profile(
            tmp_path,
            "default",
            {"type": "external", "base_url": "http://localhost:8080"},
            {"access_token": "x", "expires_at": int(time.time()) + 3600},
        )
        assert CredentialsFile()().token == "x"

    def test_workload_identity_http_rejected(self) -> None:
        from anthropic.lib.credentials import WorkloadIdentityCredentials

        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="fdrl_x",
            organization_id="00000000-0000-0000-0000-000000000000",
        )
        with pytest.raises(AnthropicError, match="must use https"):
            creds.bind_base_url("http://evil.example.com")

    # -- security: profile-name validation --------------------------------

    def test_profile_name_path_traversal_rejected(self) -> None:
        with pytest.raises(AnthropicError, match="path separators"):
            CredentialsFile(profile="evil/shadow")()

    def test_profile_name_leading_dot_rejected(self) -> None:
        with pytest.raises(AnthropicError, match="must not start with a dot"):
            CredentialsFile(profile=".hidden")()

    def test_profile_name_empty_rejected(self) -> None:
        with pytest.raises(AnthropicError, match="must not be empty"):
            CredentialsFile(profile="")()

    # -- security: credentials file permissions ---------------------------

    def test_credentials_file_world_readable_rejected(self, tmp_path: pathlib.Path) -> None:
        if os.name != "posix":
            pytest.skip("POSIX mode bits only")
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "x"})
        (tmp_path / "credentials" / "default.json").chmod(0o644)
        with pytest.raises(AnthropicError, match="world-readable"):
            CredentialsFile()()

    def test_credentials_file_group_readable_warns(
        self, tmp_path: pathlib.Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        if os.name != "posix":
            pytest.skip("POSIX mode bits only")
        _write_profile(
            tmp_path,
            "default",
            {"type": "external"},
            {"access_token": "x", "expires_at": int(time.time()) + 3600},
        )
        (tmp_path / "credentials" / "default.json").chmod(0o640)
        with caplog.at_level("WARNING", logger="anthropic.lib.credentials._providers"):
            CredentialsFile()()
        assert any("group-readable" in rec.message for rec in caplog.records)

    def test_credentials_file_symlink_rejected(self, tmp_path: pathlib.Path) -> None:
        if os.name != "posix":
            pytest.skip("symlink semantics")
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "x"})
        real = tmp_path / "credentials" / "default.json"
        target = tmp_path / "real-secret.json"
        target.write_text(real.read_text())
        target.chmod(0o600)
        real.unlink()
        real.symlink_to(target)
        with pytest.raises(AnthropicError, match="symlink"):
            CredentialsFile()()

    # -- security: redacted error bodies ----------------------------------

    def test_workload_identity_error_body_redacted(self) -> None:
        from anthropic.lib.credentials._workload import _redact_body

        # Long string truncated.
        long = "sensitive_" * 100
        result = _redact_body(long)
        assert isinstance(result, str)
        assert len(result) < len(long)
        assert "... <" in result

        # Dict keeps only OAuth standard error fields; the assertion is dropped.
        dirty = {
            "error": "invalid_grant",
            "error_description": "token expired",
            "assertion": "eyJleHAmple.jwt.sensitive",
            "refresh_token": "rt_sensitive",
        }
        cleaned = _redact_body(dirty)
        assert cleaned == {"error": "invalid_grant", "error_description": "token expired"}

    def test_bad_config_json(self, tmp_path: pathlib.Path) -> None:
        (tmp_path / "configs").mkdir()
        (tmp_path / "configs" / "default.json").write_text("{not json")
        with pytest.raises(AnthropicError, match="not valid JSON"):
            CredentialsFile()()

    # -- profiles & paths --------------------------------------------------

    def test_explicit_profile(self, tmp_path: pathlib.Path) -> None:
        _write_profile(tmp_path, "work", {"type": "external"}, {"access_token": "work-tok"})
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "default-tok"})
        assert CredentialsFile("work")().token == "work-tok"
        assert CredentialsFile()().token == "default-tok"

    def test_profile_from_env(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_profile(tmp_path, "from-env", {"type": "external"}, {"access_token": "env-tok"})
        monkeypatch.setenv("ANTHROPIC_PROFILE", "from-env")
        assert CredentialsFile()().token == "env-tok"

    def test_profile_from_active_config(self, tmp_path: pathlib.Path) -> None:
        _write_profile(tmp_path, "pointed-at", {"type": "external"}, {"access_token": "active-tok"})
        (tmp_path / "active_config").write_text("pointed-at\n")
        assert CredentialsFile()().token == "active-tok"

    def test_env_overrides_active_config(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        _write_profile(tmp_path, "from-env", {"type": "external"}, {"access_token": "env-tok"})
        _write_profile(tmp_path, "from-file", {"type": "external"}, {"access_token": "file-tok"})
        (tmp_path / "active_config").write_text("from-file")
        monkeypatch.setenv("ANTHROPIC_PROFILE", "from-env")
        assert CredentialsFile()().token == "env-tok"

    def test_credentials_path_override(self, tmp_path: pathlib.Path) -> None:
        """Config's ``credentials_path`` field redirects to a custom location."""
        custom = tmp_path / "elsewhere" / "secrets.json"
        custom.parent.mkdir()
        custom.write_text(json.dumps({"access_token": "redirected"}))
        custom.chmod(0o600)

        _write_profile(tmp_path, "default", {"type": "external", "credentials_path": str(custom)})
        assert CredentialsFile()().token == "redirected"

    @pytest.mark.respx(base_url="https://from-config.example.com")
    def test_base_url_from_config(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """Config ``base_url`` is used when no ctor override is given."""
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("x")
        _write_profile(
            tmp_path,
            "default",
            {
                "type": "workload_identity",
                "base_url": "https://from-config.example.com",
                "identity_token": {"source": "file", "path": str(jwt_path)},
                "federation_rule_id": "f",
                "organization_id": "o",
            },
        )
        token_route = respx_mock.post("/v1/oauth/token").mock(
            return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
        )
        CredentialsFile()()  # no base_url ctor arg → config wins
        assert str(cast("list[MockRequestCall]", token_route.calls)[0].request.url).startswith(
            "https://from-config.example.com/"
        )

    # -- review fixes -----------------------------------------------------

    def test_chain_and_class_agree_on_profile(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """default_credentials() and CredentialsFile() resolve to the same profile."""
        _write_profile(tmp_path, "agreed", {"type": "external"}, {"access_token": "x"})
        monkeypatch.setenv("ANTHROPIC_PROFILE", "agreed")

        result = default_credentials()
        assert result is not None
        chain = result.provider
        direct = CredentialsFile()
        assert isinstance(chain, CredentialsFile)
        assert chain.profile == direct.profile == "agreed"
        assert chain.config_path == direct.config_path


# --------------------------------------------------------------------------- #
# WorkloadIdentityCredentials
# --------------------------------------------------------------------------- #


class TestWorkloadIdentityCredentials:
    @pytest.mark.respx()
    def test_exchange(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "sk-ant-oat01-test", "token_type": "Bearer", "expires_in": 600},
            )
        )

        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "ext.jwt.value",
            federation_rule_id="fdrl_01abc",
            organization_id="00000000-0000-0000-0000-000000000000",
        )

        before = time.time()
        token = creds()
        after = time.time()

        assert token.token == "sk-ant-oat01-test"
        assert token.expires_at is not None
        assert before + 600 - 2 <= token.expires_at <= after + 600 + 2

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 1
        req = calls[0].request
        # jwt-bearer exchange must carry BOTH: oauth-2025-04-20 unlocks the
        # token endpoint, oidc-federation-2026-04-01 routes to the federation
        # handler.
        beta_flags = {f.strip() for f in req.headers["anthropic-beta"].split(",")}
        assert OAUTH_API_BETA_HEADER in beta_flags
        assert FEDERATION_BETA_HEADER in beta_flags
        assert req.headers["User-Agent"] == f"anthropic-python/{__version__}"
        body = json.loads(req.content)
        assert body["grant_type"] == GRANT_TYPE_JWT_BEARER
        assert body["assertion"] == "ext.jwt.value"
        assert body["federation_rule_id"] == "fdrl_01abc"
        assert body["organization_id"] == "00000000-0000-0000-0000-000000000000"
        assert "service_account_id" not in body
        assert "scope" not in body

    @pytest.mark.respx()
    def test_service_account_included(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60}))
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="fdrl_01abc",
            organization_id="org",
            service_account_id="svac_01xyz",
        )
        creds()
        body = json.loads(cast("list[MockRequestCall]", respx_mock.calls)[0].request.content)
        assert body["service_account_id"] == "svac_01xyz"
        assert "scope" not in body

    @pytest.mark.respx()
    def test_scope_is_display_only(self, respx_mock: MockRouter) -> None:
        """``scope`` is stored on the provider for parity but never sent on the
        wire — the server derives effective scope from the federation rule."""
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60}))
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="fdrl_x",
            organization_id="org",
            scope="api:read api:write",
        )
        creds()
        assert creds.scope == "api:read api:write"
        body = json.loads(cast("list[MockRequestCall]", respx_mock.calls)[0].request.content)
        assert "scope" not in body

    @pytest.mark.respx()
    def test_exchange_federation_assertion_helper(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "sk-ant-oat01-one", "expires_in": 600})
        )
        token = exchange_federation_assertion(
            assertion="ext.jwt.value",
            federation_rule_id="fdrl_x",
            organization_id="org_x",
        )
        assert token.token == "sk-ant-oat01-one"
        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        body = json.loads(req.content)
        assert body["assertion"] == "ext.jwt.value"
        assert body["federation_rule_id"] == "fdrl_x"

    @pytest.mark.respx()
    def test_bind_base_url(self, respx_mock: MockRouter) -> None:
        """``bind_base_url`` sets the token-exchange URL; unbound → ``DEFAULT_BASE_URL``."""
        bound = "https://bound.example"

        # No bind → DEFAULT_BASE_URL
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60}))
        WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j", federation_rule_id="fdrl_x", organization_id="org"
        )()
        assert str(cast("list[MockRequestCall]", respx_mock.calls)[-1].request.url) == TOKEN_URL

        # bound → bound
        respx_mock.post(f"{bound}{TOKEN_ENDPOINT}").mock(
            return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60})
        )
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j", federation_rule_id="fdrl_x", organization_id="org"
        )
        creds.bind_base_url(bound)
        creds()
        assert str(cast("list[MockRequestCall]", respx_mock.calls)[-1].request.url) == f"{bound}{TOKEN_ENDPOINT}"

    def test_bind_base_url_http_rejected(self) -> None:
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j", federation_rule_id="fdrl_x", organization_id="org"
        )
        with pytest.raises(AnthropicError, match="must use https"):
            creds.bind_base_url("http://evil.example")

    def test_exchange_federation_assertion_http_rejected(self) -> None:
        with pytest.raises(AnthropicError, match="must use https"):
            exchange_federation_assertion(
                assertion="j",
                federation_rule_id="fdrl_x",
                organization_id="org_x",
                base_url="http://example.com",
            )

    @pytest.mark.respx()
    def test_reinvokes_identity_provider(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60}))
        calls: List[int] = []

        def jwt_provider() -> str:
            calls.append(1)
            return f"jwt-{len(calls)}"

        creds = WorkloadIdentityCredentials(
            identity_token_provider=jwt_provider,
            federation_rule_id="f",
            organization_id="o",
        )
        creds()
        creds()
        assert len(calls) == 2
        bodies = [json.loads(c.request.content) for c in cast("list[MockRequestCall]", respx_mock.calls)]
        assert bodies[0]["assertion"] == "jwt-1"
        assert bodies[1]["assertion"] == "jwt-2"

    @pytest.mark.respx()
    def test_403_raises(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(403, json={"error": "assertion rejected"}))
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="f",
            organization_id="o",
        )
        with pytest.raises(WorkloadIdentityError) as exc_info:
            creds()
        assert exc_info.value.status_code == 403
        assert "assertion rejected" in str(exc_info.value)

    @pytest.mark.respx()
    def test_503_raises(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(503, text="overloaded"))
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="f",
            organization_id="o",
        )
        with pytest.raises(WorkloadIdentityError) as exc_info:
            creds()
        assert exc_info.value.status_code == 503

    @pytest.mark.respx()
    def test_request_id_surfaced_on_error(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(400, json={"error": "invalid_grant"}, headers={"Request-Id": "req_abc123"})
        )
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="f",
            organization_id="o",
        )
        with pytest.raises(WorkloadIdentityError) as exc_info:
            creds()
        assert exc_info.value.request_id == "req_abc123"
        assert "[request_id=req_abc123]" in str(exc_info.value)

    def test_oversized_assertion_rejected(self) -> None:
        big_jwt = "x" * (16 * 1024 + 1)
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: big_jwt,
            federation_rule_id="f",
            organization_id="o",
        )
        with pytest.raises(WorkloadIdentityError, match="exceeds the 16384-byte limit"):
            creds()

    @pytest.mark.respx()
    def test_non_bearer_token_type_rejected(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60, "token_type": "MAC"})
        )
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="f",
            organization_id="o",
        )
        with pytest.raises(WorkloadIdentityError, match="unsupported token_type 'MAC'"):
            creds()

    @pytest.mark.respx()
    def test_bearer_token_type_case_insensitive(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "t", "expires_in": 60, "token_type": "bearer"})
        )
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="f",
            organization_id="o",
        )
        assert creds().token == "t"

    @pytest.mark.respx()
    def test_oversized_response_body_rejected(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, content=b"x" * ((1 << 20) + 1)))
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "j",
            federation_rule_id="f",
            organization_id="o",
        )
        with pytest.raises(WorkloadIdentityError, match="response body exceeds"):
            creds()


# --------------------------------------------------------------------------- #
# Profile env-var fill (PY-01) + identity_token validation (PY-06)
# --------------------------------------------------------------------------- #


class TestProfileEnvFill:
    """PY-01: profile fields left empty are filled from ANTHROPIC_* env vars,
    matching Go's ``fillMissingFromEnv`` precedence (file wins, env fills gaps)."""

    @pytest.fixture(autouse=True)
    def _isolate(self, monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        for var in _ALL_ENV:
            monkeypatch.delenv(var, raising=False)
        monkeypatch.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))

    def test_env_fills_missing_organization_id(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_ORGANIZATION_ID", "org_from_env")
        monkeypatch.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(tmp_path / "tok"))
        (tmp_path / "tok").write_text("jwt")
        # Profile omits organization_id; env supplies it.
        _write_profile(
            tmp_path,
            "default",
            config={
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_01abc",
                }
            },
        )
        provider = CredentialsFile()
        # Trigger _load_config via the workload-build path.
        delegate = provider._build_workload_delegate(provider._auth_block())  # pyright: ignore[reportPrivateUsage]
        assert delegate._organization_id == "org_from_env"  # pyright: ignore[reportPrivateUsage]

    def test_profile_value_wins_over_env(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_ORGANIZATION_ID", "org_from_env")
        monkeypatch.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(tmp_path / "tok"))
        (tmp_path / "tok").write_text("jwt")
        _write_profile(
            tmp_path,
            "default",
            config={
                "organization_id": "org_from_file",
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_01abc",
                },
            },
        )
        provider = CredentialsFile()
        delegate = provider._build_workload_delegate(provider._auth_block())  # pyright: ignore[reportPrivateUsage]
        assert delegate._organization_id == "org_from_file"  # pyright: ignore[reportPrivateUsage]


class TestIdentityTokenValidation:
    """PY-06: identity_token.source 'file' with empty path is a config bug,
    not an env-var fallback signal."""

    @pytest.fixture(autouse=True)
    def _isolate(self, monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        for var in _ALL_ENV:
            monkeypatch.delenv(var, raising=False)
        monkeypatch.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))

    def test_empty_path_raises(self, tmp_path: pathlib.Path) -> None:
        _write_profile(
            tmp_path,
            "default",
            config={
                "organization_id": "org",
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_01abc",
                    "identity_token": {"source": "file", "path": ""},
                },
            },
        )
        provider = CredentialsFile()
        with pytest.raises(AnthropicError, match="non-empty path"):
            provider._build_workload_delegate(provider._auth_block())  # pyright: ignore[reportPrivateUsage]


# --------------------------------------------------------------------------- #
# TokenCache
# --------------------------------------------------------------------------- #


class FakeClock:
    def __init__(self, now: float = 1000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


class CountingProvider:
    def __init__(self, tokens: List[AccessToken]) -> None:
        self.tokens = tokens
        self.calls = 0

    def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
        self.calls += 1
        return self.tokens[min(self.calls - 1, len(self.tokens) - 1)]


class TestTokenCache:
    def test_first_call_fetches(self) -> None:
        provider = CountingProvider([AccessToken("a", expires_at=2000)])
        cache = TokenCache(provider, time_source=FakeClock(1000))
        assert cache.get_token() == "a"
        assert provider.calls == 1

    def test_no_expiry_never_refreshes(self) -> None:
        provider = CountingProvider([AccessToken("a", expires_at=None)])
        clock = FakeClock(1000)
        cache = TokenCache(provider, time_source=clock)
        cache.get_token()
        clock.now = 999999
        cache.get_token()
        cache.get_token()
        assert provider.calls == 1

    def test_fresh_token_not_refetched(self) -> None:
        clock = FakeClock(1000)
        provider = CountingProvider([AccessToken("a", expires_at=1000 + 600)])
        cache = TokenCache(provider, time_source=clock)
        cache.get_token()
        cache.get_token()
        cache.get_token()
        assert provider.calls == 1

    def test_advisory_refresh_success(self) -> None:
        clock = FakeClock(1000)
        provider = CountingProvider([AccessToken("a", expires_at=1000 + 600), AccessToken("b", expires_at=1000 + 1200)])
        cache = TokenCache(provider, time_source=clock)
        assert cache.get_token() == "a"
        clock.now = 1000 + 600 - 60  # 60s remaining: advisory window (30 < 60 < 120)
        assert cache.get_token() == "b"
        assert provider.calls == 2

    def test_advisory_refresh_failure_serves_stale(self, caplog: pytest.LogCaptureFixture) -> None:
        clock = FakeClock(1000)
        first = AccessToken("a", expires_at=1000 + 600)

        class P:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                if self.calls == 1:
                    return first
                raise WorkloadIdentityError("backend down")

        provider = P()
        cache = TokenCache(provider, time_source=clock)
        assert cache.get_token() == "a"
        clock.now = 1000 + 600 - 60  # advisory window
        with caplog.at_level(logging.WARNING):
            assert cache.get_token() == "a"  # stale served
        assert any("Advisory token refresh failed" in r.message for r in caplog.records)
        assert provider.calls == 2

    def test_mandatory_refresh_failure_raises(self) -> None:
        clock = FakeClock(1000)
        first = AccessToken("a", expires_at=1000 + 600)

        class P:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                if self.calls == 1:
                    return first
                raise WorkloadIdentityError("backend down")

        provider = P()
        cache = TokenCache(provider, time_source=clock)
        cache.get_token()
        clock.now = 1000 + 600 - 10  # 10s remaining: mandatory window
        with pytest.raises(WorkloadIdentityError, match="backend down"):
            cache.get_token()

    def test_expired_is_mandatory(self) -> None:
        clock = FakeClock(1000)
        provider = CountingProvider([AccessToken("a", expires_at=1000 + 600), AccessToken("b", expires_at=1000 + 1200)])
        cache = TokenCache(provider, time_source=clock)
        cache.get_token()
        clock.now = 1000 + 700  # already expired
        assert cache.get_token() == "b"
        assert provider.calls == 2

    def test_invalidate(self) -> None:
        provider = CountingProvider([AccessToken("a", None), AccessToken("b", None)])
        cache = TokenCache(provider)
        assert cache.get_token() == "a"
        assert cache.get_token() == "a"
        assert provider.calls == 1
        cache.invalidate()
        assert cache.get_token() == "b"
        assert provider.calls == 2

    def test_retries_once_on_401_from_token_endpoint(self) -> None:
        """If the provider raises a 401 WorkloadIdentityError, the cache retries once."""

        class Provider401ThenSuccess:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                if self.calls == 1:
                    raise WorkloadIdentityError("token exchange failed", status_code=401, body="unauthorized")
                return AccessToken("fresh", expires_at=None)

        provider = Provider401ThenSuccess()
        cache = TokenCache(provider)
        assert cache.get_token() == "fresh"
        assert provider.calls == 2

    def test_no_retry_on_non_401_error(self) -> None:
        """Non-401 errors from the provider are not retried."""

        class Provider400:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                raise WorkloadIdentityError("bad request", status_code=400, body="invalid")

        provider = Provider400()
        cache = TokenCache(provider)
        with pytest.raises(WorkloadIdentityError, match="bad request"):
            cache.get_token()
        assert provider.calls == 1

    def test_retry_on_401_still_fails_raises(self) -> None:
        """If both attempts return 401, the second error propagates."""

        class AlwaysFails401:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                raise WorkloadIdentityError("still unauthorized", status_code=401, body="unauthorized")

        provider = AlwaysFails401()
        cache = TokenCache(provider)
        with pytest.raises(WorkloadIdentityError, match="still unauthorized"):
            cache.get_token()
        assert provider.calls == 2

    def test_concurrent_mandatory_refresh_single_flight(self) -> None:
        """N concurrent callers in the mandatory (expired) window trigger
        exactly one provider call — waiters block on the leader's event."""
        import threading as _threading

        provider_calls: List[int] = []
        barrier = _threading.Barrier(8)

        def slow_provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append(1)
            # Hold the refresh long enough for the other threads to queue up.
            time.sleep(0.1)
            return AccessToken(token="fresh", expires_at=None)

        cache = TokenCache(slow_provider)
        results: List[str] = []
        lock = _threading.Lock()

        def worker() -> None:
            barrier.wait()
            tok = cache.get_token()
            with lock:
                results.append(tok)

        threads = [_threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(provider_calls) == 1
        assert results == ["fresh"] * 8

    def test_advisory_caller_skips_when_refresh_in_flight(self) -> None:
        """A caller in the advisory window does NOT start a second refresh and
        does NOT wait on a running one — it just returns the cached token."""
        import threading as _threading

        clock = FakeClock(1000)
        tokens = [AccessToken("a", expires_at=1000 + 600), AccessToken("b", expires_at=1000 + 1800)]
        provider_calls: List[int] = []
        refresh_started = _threading.Event()
        release_refresh = _threading.Event()

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append(1)
            refresh_started.set()
            release_refresh.wait(timeout=2)
            return tokens[len(provider_calls) - 1]

        cache = TokenCache(provider, time_source=clock)
        # Prime the cache with token 'a'.
        assert cache.get_token() == "a"

        # Move into the advisory window and kick off a refresh on a background
        # thread. It will block in the provider until we release it.
        clock.now = 1000 + 600 - 60
        leader = _threading.Thread(target=cache.get_token)
        leader.start()
        assert refresh_started.wait(timeout=2)

        # A second caller in the advisory window should see the in-flight
        # refresh and return the cached token immediately — without waiting.
        t0 = time.monotonic()
        observed = cache.get_token()
        elapsed = time.monotonic() - t0
        assert observed == "a"
        assert elapsed < 0.1, f"advisory caller waited for leader ({elapsed:.3f}s)"

        release_refresh.set()
        leader.join()
        # Two provider calls total: the priming call + the leader's advisory
        # refresh. The bystander did NOT call the provider.
        assert len(provider_calls) == 2

    def test_invalidate_forces_provider_refresh(self) -> None:
        """PY-02: after invalidate(), the next provider call receives
        force_refresh=True so providers with on-disk caches bypass their
        freshness short-circuit. Without this, a 401 retry would re-read
        the same expired token from disk and serve it again."""
        force_seen: List[bool] = []
        tokens = iter([AccessToken("a", expires_at=None), AccessToken("b", expires_at=None)])

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            force_seen.append(force_refresh)
            return next(tokens)

        cache = TokenCache(provider)
        assert cache.get_token() == "a"
        cache.invalidate()
        assert cache.get_token() == "b"
        assert force_seen == [False, True], "force_refresh must be True on the post-invalidate call"

    def test_zero_arg_provider_backward_compat(self) -> None:
        """Providers from before the force_refresh kwarg was added (the old
        ``Callable[[], AccessToken]`` shape) must still work — the kwarg-
        binding TypeError is caught and the provider is re-invoked
        positionally."""
        calls: List[int] = []

        def legacy_provider() -> AccessToken:
            calls.append(1)
            return AccessToken("legacy", expires_at=None)

        cache = TokenCache(legacy_provider)  # type: ignore[arg-type]
        assert cache.get_token() == "legacy"
        # invalidate() sets _next_force; the zero-arg fallback must still fire.
        cache.invalidate()
        assert cache.get_token() == "legacy"
        assert len(calls) == 2

    def test_next_force_preserved_on_provider_failure(self) -> None:
        """If invalidate() set the force flag and the provider then raises,
        the flag must NOT be consumed — a subsequent retry must still see
        force_refresh=True. Otherwise the retry serves the stale disk token
        PY-02 was added to bypass."""
        force_seen: List[bool] = []
        attempts = iter([RuntimeError("transient"), AccessToken("ok", expires_at=None)])

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            force_seen.append(force_refresh)
            v = next(attempts)
            if isinstance(v, BaseException):
                raise v
            return v

        cache = TokenCache(provider)
        cache.invalidate()
        with pytest.raises(RuntimeError):
            cache.get_token()
        # Retry: force flag must still be set.
        assert cache.get_token() == "ok"
        assert force_seen == [True, True], "force flag must survive provider failure"

    def test_advisory_refresh_backoff_after_failure(self) -> None:
        """PY-07: after an advisory refresh failure, subsequent advisory
        callers within ADVISORY_REFRESH_BACKOFF_SECONDS reuse the cached
        token instead of re-attempting the provider — preventing an
        outage during the advisory window from being hammered at request rate."""
        from anthropic.lib.credentials._workload import WorkloadIdentityError as _WIE

        clock = FakeClock(1000)
        provider_calls: List[int] = []

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append(1)
            if len(provider_calls) == 1:
                return AccessToken("a", expires_at=1000 + 600)
            raise _WIE("token endpoint down", status_code=503)

        cache = TokenCache(provider, time_source=clock)
        assert cache.get_token() == "a"
        # Step into the advisory window.
        clock.now = 1000 + 600 - 60
        # First advisory call: fires the provider, fails, serves cached.
        assert cache.get_token() == "a"
        assert len(provider_calls) == 2

        # Second advisory call within backoff window: must reuse cached
        # WITHOUT calling the provider.
        clock.now += 3
        assert cache.get_token() == "a"
        assert len(provider_calls) == 2, "provider must not be retried within backoff window"

        # After the backoff window, the next advisory call retries.
        clock.now += 3  # total +6 since failure, > 5s backoff
        assert cache.get_token() == "a"  # still serves cached after retry fails
        assert len(provider_calls) == 3, "provider must be retried after backoff window"


# --------------------------------------------------------------------------- #
# default_credentials chain
# --------------------------------------------------------------------------- #


@pytest.mark.usefixtures("no_default_creds_file")
class TestDefaultCredentials:
    def test_api_key_returns_none(self, clean_env: pytest.MonkeyPatch) -> None:
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-ant-api-key")
        assert default_credentials() is None

    def test_auth_token_returns_static(self, clean_env: pytest.MonkeyPatch) -> None:
        clean_env.setenv("ANTHROPIC_AUTH_TOKEN", "bearer-tok")
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, StaticToken)
        assert result.provider().token == "bearer-tok"

    def test_config_dir_env_triggers_tier1(self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        """ANTHROPIC_CONFIG_DIR set → tier 1 fires even if dir is empty (explicit opt-in)."""
        # Re-point _config_dir at tmp_path (the no_default_creds_file fixture
        # already patched it to an empty dir; override that here).
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "from-file"})
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, CredentialsFile)
        assert result.provider().token == "from-file"

    def test_profile_env_triggers_tier1(self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        """ANTHROPIC_PROFILE set → tier 1 fires."""
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_PROFILE", "work")
        _write_profile(tmp_path, "work", {"type": "external"}, {"access_token": "from-work"})
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, CredentialsFile)
        assert result.provider().token == "from-work"

    def test_default_dir_with_configs_triggers_tier1(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        """No env vars but configs/ has files → tier 1 fires via _has_any_config()."""
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "from-default"})
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, CredentialsFile)

    def test_workload_identity_tier(self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        f = tmp_path / "jwt"
        f.write_text("ext-jwt")
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(f))
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "org-uuid")
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, WorkloadIdentityCredentials)

    def test_workload_identity_literal_token(self, clean_env: pytest.MonkeyPatch) -> None:
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "literal-jwt")
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "org-uuid")
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, WorkloadIdentityCredentials)

    def test_workload_identity_scope_env(self, clean_env: pytest.MonkeyPatch) -> None:
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "literal-jwt")
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "org-uuid")
        clean_env.setenv("ANTHROPIC_SCOPE", "api:read api:write")
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, WorkloadIdentityCredentials)
        assert result.provider.scope == "api:read api:write"

    def test_workload_identity_literal_token_reads_fresh(self, clean_env: pytest.MonkeyPatch) -> None:
        """Fix 4: ANTHROPIC_IDENTITY_TOKEN must be re-read on every provider
        invocation, not captured into a closure at chain-construction time."""
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "jwt-v1")
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "org-uuid")
        result = default_credentials()
        assert result is not None
        provider = result.provider
        assert isinstance(provider, WorkloadIdentityCredentials)
        assert provider._identity_token_provider() == "jwt-v1"  # pyright: ignore[reportPrivateUsage]

        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "jwt-v2")
        assert provider._identity_token_provider() == "jwt-v2"  # pyright: ignore[reportPrivateUsage]

    def test_workload_identity_requires_all_three(self, clean_env: pytest.MonkeyPatch) -> None:
        # only two of three set
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "literal-jwt")
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        assert default_credentials() is None

    def test_env_federation_beats_fallback_on_disk_profile(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        """Step 4 (env federation trio) sits above step 5 (fallback on-disk
        profile) in the precedence spec: a machine with WIF env vars wired
        up must use WIF even if a leftover ``default`` profile exists on
        disk. A user who wants the on-disk profile must set
        ``ANTHROPIC_PROFILE`` explicitly (step 3), which would win.
        """
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "from-on-disk-profile"})
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "literal-jwt")
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "00000000-0000-0000-0000-000000000000")
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, WorkloadIdentityCredentials)

    def test_explicit_profile_beats_env_federation(self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        """Step 3 (ANTHROPIC_PROFILE) sits above step 4 (env federation).
        An explicit profile selection wins over a federation-configured
        environment.
        """
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(tmp_path, "dev", {"type": "external"}, {"access_token": "from-dev-profile"})
        clean_env.setenv("ANTHROPIC_PROFILE", "dev")
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN", "literal-jwt")
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "00000000-0000-0000-0000-000000000000")
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, CredentialsFile)
        assert result.provider().token == "from-dev-profile"

    @pytest.mark.usefixtures("clean_env")
    def test_nothing_set_returns_none(self) -> None:
        assert default_credentials() is None


# --------------------------------------------------------------------------- #
# Anthropic(credentials=...) integration
# --------------------------------------------------------------------------- #


def _mock_token_endpoint(respx_mock: MockRouter) -> None:
    respx_mock.post(TOKEN_URL).mock(
        return_value=httpx.Response(
            200,
            json={"access_token": "sk-ant-oat01-test", "token_type": "Bearer", "expires_in": 600},
        )
    )


def _mock_messages_endpoint(respx_mock: MockRouter) -> None:
    respx_mock.post(f"{BASE_URL}/v1/messages").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "msg_01",
                "type": "message",
                "role": "assistant",
                "model": "claude-opus-4-5",
                "content": [{"type": "text", "text": "hi"}],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 1, "output_tokens": 1},
            },
        )
    )


def _send_message(client: Anthropic) -> None:
    client.messages.create(
        max_tokens=1,
        model="claude-opus-4-5",
        messages=[{"role": "user", "content": "hi"}],
    )


@pytest.mark.usefixtures("clean_env", "no_default_creds_file")
class TestAnthropicCredentials:
    @pytest.mark.respx()
    def test_messages_request_has_bearer_and_beta(self, respx_mock: MockRouter) -> None:
        _mock_token_endpoint(respx_mock)
        _mock_messages_endpoint(respx_mock)

        client = Anthropic(
            credentials=WorkloadIdentityCredentials(
                identity_token_provider=lambda: "ext-jwt",
                federation_rule_id="fdrl_01abc",
                organization_id="org-uuid",
            ),
        )
        _send_message(client)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        msg_calls = [c for c in calls if str(c.request.url).endswith("/v1/messages")]
        assert len(msg_calls) == 1
        req = msg_calls[0].request
        assert req.headers["Authorization"] == "Bearer sk-ant-oat01-test"
        # Authenticated API requests carry oauth-2025-04-20 (API beta) —
        # NOT the federation routing switch, which is only for jwt-bearer
        # exchanges at /v1/oauth/token.
        msg_flags = {f.strip() for f in req.headers["anthropic-beta"].split(",")}
        assert OAUTH_API_BETA_HEADER in msg_flags
        assert FEDERATION_BETA_HEADER not in msg_flags
        assert "X-Api-Key" not in req.headers

    @pytest.mark.respx()
    def test_workload_identity_inherits_client_base_url(self, respx_mock: MockRouter) -> None:
        """An explicitly-passed WorkloadIdentityCredentials with no ``base_url``
        adopts the client's ``base_url`` for the token exchange, so the user
        doesn't have to pass the same URL twice."""
        custom_base = "https://api-staging.example"
        respx_mock.post(f"{custom_base}{TOKEN_ENDPOINT}").mock(
            return_value=httpx.Response(200, json={"access_token": "tok-staging", "expires_in": 600})
        )
        respx_mock.post(f"{custom_base}/v1/messages").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_01",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-opus-4-5",
                    "content": [{"type": "text", "text": "hi"}],
                    "stop_reason": "end_turn",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 1, "output_tokens": 1},
                },
            )
        )

        client = Anthropic(
            credentials=WorkloadIdentityCredentials(
                identity_token_provider=lambda: "ext-jwt",
                federation_rule_id="fdrl_01abc",
                organization_id="org-uuid",
            ),
            base_url=custom_base,
        )
        _send_message(client)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        token_calls = [c for c in calls if TOKEN_ENDPOINT in str(c.request.url)]
        assert len(token_calls) == 1
        assert str(token_calls[0].request.url) == f"{custom_base}{TOKEN_ENDPOINT}"
        msg_calls = [c for c in calls if str(c.request.url).endswith("/v1/messages")]
        assert msg_calls[0].request.headers["Authorization"] == "Bearer tok-staging"

    @pytest.mark.respx()
    def test_token_endpoint_called_once_across_requests(self, respx_mock: MockRouter) -> None:
        _mock_token_endpoint(respx_mock)
        _mock_messages_endpoint(respx_mock)

        client = Anthropic(
            credentials=WorkloadIdentityCredentials(
                identity_token_provider=lambda: "ext-jwt",
                federation_rule_id="fdrl_01abc",
                organization_id="org-uuid",
            ),
        )

        _send_message(client)
        _send_message(client)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        token_calls = [c for c in calls if TOKEN_ENDPOINT in str(c.request.url)]
        msg_calls = [c for c in calls if str(c.request.url).endswith("/v1/messages")]
        assert len(token_calls) == 1
        assert len(msg_calls) == 2

    @pytest.mark.respx()
    def test_static_token_credentials(self, respx_mock: MockRouter) -> None:
        _mock_messages_endpoint(respx_mock)
        client = Anthropic(credentials=StaticToken("static-bearer"))
        _send_message(client)

        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        assert req.headers["Authorization"] == "Bearer static-bearer"
        assert OAUTH_API_BETA_HEADER in req.headers["anthropic-beta"]

    @pytest.mark.respx()
    def test_beta_header_not_duplicated(self, respx_mock: MockRouter) -> None:
        _mock_messages_endpoint(respx_mock)
        client = Anthropic(credentials=StaticToken("static-bearer"))
        client.messages.create(
            max_tokens=1,
            model="claude-opus-4-5",
            messages=[{"role": "user", "content": "hi"}],
            extra_headers={"anthropic-beta": OAUTH_API_BETA_HEADER},
        )
        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        assert req.headers["anthropic-beta"] == OAUTH_API_BETA_HEADER

    @pytest.mark.respx()
    def test_beta_header_dedupe_is_token_based(self, respx_mock: MockRouter) -> None:
        """The dedupe check matches whole comma-separated flags, not substrings.
        A pre-existing flag containing the OAuth beta as a prefix (e.g. a future
        suffixed variant) must NOT prevent the SDK from adding its own flag."""
        _mock_token_endpoint(respx_mock)
        _mock_messages_endpoint(respx_mock)
        client = Anthropic(
            credentials=WorkloadIdentityCredentials(
                identity_token_provider=lambda: "ext-jwt",
                federation_rule_id="fdrl_x",
                organization_id="org-uuid",
            ),
        )
        client.messages.create(
            max_tokens=1,
            model="claude-opus-4-5",
            messages=[{"role": "user", "content": "hi"}],
            extra_headers={"anthropic-beta": f"{OAUTH_API_BETA_HEADER}-future-variant"},
        )
        msg_calls = [
            c for c in cast("list[MockRequestCall]", respx_mock.calls) if str(c.request.url).endswith("/v1/messages")
        ]
        flags = [f.strip() for f in msg_calls[0].request.headers["anthropic-beta"].split(",")]
        assert OAUTH_API_BETA_HEADER in flags
        assert f"{OAUTH_API_BETA_HEADER}-future-variant" in flags

    @pytest.mark.respx()
    def test_zero_config_workload_identity_from_env(
        self, respx_mock: MockRouter, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        f = tmp_path / "jwt"
        f.write_text("env-jwt")
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(f))
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "org-uuid")

        _mock_token_endpoint(respx_mock)
        _mock_messages_endpoint(respx_mock)

        client = Anthropic()
        assert isinstance(client.credentials, WorkloadIdentityCredentials)
        _send_message(client)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        token_calls = [c for c in calls if TOKEN_ENDPOINT in str(c.request.url)]
        msg_calls = [c for c in calls if str(c.request.url).endswith("/v1/messages")]
        assert len(token_calls) == 1
        assert json.loads(token_calls[0].request.content)["assertion"] == "env-jwt"
        assert msg_calls[0].request.headers["Authorization"] == "Bearer sk-ant-oat01-test"

    @pytest.mark.respx()
    def test_zero_config_credentials_file_from_env(
        self, respx_mock: MockRouter, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        # no_default_creds_file patched _config_dir → empty dir; re-point at tmp_path
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "sk-ant-oat01-file"})

        _mock_messages_endpoint(respx_mock)

        client = Anthropic()
        assert isinstance(client.credentials, CredentialsFile)
        _send_message(client)

        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        assert req.headers["Authorization"] == "Bearer sk-ant-oat01-file"

    def test_profile_base_url_adopted_by_client(self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        """Outbound: a zero-arg ``Anthropic()`` adopts the active profile's
        ``base_url`` when the user supplied neither ``base_url=`` nor
        ``ANTHROPIC_BASE_URL``. Precedence: kwarg > env > profile > default."""
        clean_env.delenv("ANTHROPIC_BASE_URL", raising=False)
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))
        _write_profile(
            tmp_path,
            "default",
            {"type": "external", "base_url": "https://staging.example"},
            {"access_token": "sk-ant-oat01-x"},
        )

        # profile base_url → client.base_url
        assert str(Anthropic().base_url).rstrip("/") == "https://staging.example"
        assert str(AsyncAnthropic().base_url).rstrip("/") == "https://staging.example"

        # ANTHROPIC_BASE_URL beats profile
        clean_env.setenv("ANTHROPIC_BASE_URL", "https://env.example")
        assert str(Anthropic().base_url).rstrip("/") == "https://env.example"
        clean_env.delenv("ANTHROPIC_BASE_URL", raising=False)

        # base_url= kwarg beats profile
        assert str(Anthropic(base_url="https://kwarg.example").base_url).rstrip("/") == "https://kwarg.example"

        # profile without base_url → hardcoded default
        _write_profile(
            tmp_path,
            "default",
            {"type": "external"},
            {"access_token": "sk-ant-oat01-x"},
        )
        assert str(Anthropic().base_url).rstrip("/") == "https://api.anthropic.com"

    def test_config_dict_base_url_adopted_by_client(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        """Outbound, ``config=`` path: ``Anthropic(config={"base_url": ...})``
        adopts the dict's ``base_url`` for API requests when no kwarg/env is
        set, mirroring the disk-profile behaviour."""
        clean_env.delenv("ANTHROPIC_BASE_URL", raising=False)
        creds_path = tmp_path / "creds.json"
        creds_path.write_text(json.dumps({"type": "oauth_token", "access_token": "sk-ant-oat01-x"}))
        creds_path.chmod(0o600)
        cfg = {
            "base_url": "https://staging.example",
            "authentication": {"type": "user_oauth", "credentials_path": str(creds_path)},
        }

        assert str(Anthropic(config=cfg).base_url).rstrip("/") == "https://staging.example"
        assert str(AsyncAnthropic(config=cfg).base_url).rstrip("/") == "https://staging.example"

        # explicit base_url= still wins over config dict
        assert (
            str(Anthropic(config=cfg, base_url="https://kwarg.example").base_url).rstrip("/") == "https://kwarg.example"
        )

    @pytest.mark.respx()
    def test_workspace_id_header_from_config(
        self, respx_mock: MockRouter, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        """workspace_id in the config file → anthropic-workspace-id header on API requests."""
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))
        _write_profile(
            tmp_path,
            "default",
            {"type": "external", "workspace_id": "wrkspc_01abc"},
            {"access_token": "sk-ant-oat01-file"},
        )

        _mock_messages_endpoint(respx_mock)

        client = Anthropic()
        _send_message(client)

        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        assert req.headers["anthropic-workspace-id"] == "wrkspc_01abc"

    @pytest.mark.respx()
    def test_401_invalidates_cache_and_retries_once(self, respx_mock: MockRouter) -> None:
        """On 401 we invalidate the cache and retry the current request once
        with a freshly minted token. A second 401 is not retried (single-shot
        guard via x-stainless-retry-count)."""
        provider_calls: List[str] = []

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append("called")
            return AccessToken(token=f"tok-{len(provider_calls)}", expires_at=None)

        # 401 then 200 — the retry should succeed transparently.
        respx_mock.post(f"{BASE_URL}/v1/messages").mock(
            side_effect=[
                httpx.Response(401, json={"error": "unauthorized"}),
                httpx.Response(
                    200,
                    json={
                        "id": "msg_01",
                        "type": "message",
                        "role": "assistant",
                        "model": "claude-opus-4-5",
                        "content": [{"type": "text", "text": "hi"}],
                        "stop_reason": "end_turn",
                        "stop_sequence": None,
                        "usage": {"input_tokens": 1, "output_tokens": 1},
                    },
                ),
            ],
        )
        client = Anthropic(credentials=provider, max_retries=2)
        _send_message(client)
        assert len(provider_calls) == 2
        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert calls[0].request.headers["Authorization"] == "Bearer tok-1"
        assert calls[1].request.headers["Authorization"] == "Bearer tok-2"

    @pytest.mark.respx()
    def test_401_retry_is_single_shot(self, respx_mock: MockRouter) -> None:
        """Two consecutive 401s → exactly one retry, then the error surfaces
        even with max_retries > 1 remaining."""
        respx_mock.post(f"{BASE_URL}/v1/messages").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"}),
        )
        provider_calls: List[str] = []

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append("called")
            return AccessToken(token=f"tok-{len(provider_calls)}", expires_at=None)

        client = Anthropic(credentials=provider, max_retries=3)
        with pytest.raises(anthropic.AuthenticationError):
            _send_message(client)
        assert len(provider_calls) == 2  # initial + one retry
        assert len(cast("list[MockRequestCall]", respx_mock.calls)) == 2

    @pytest.mark.respx()
    def test_api_key_precedence_preserved(
        self, respx_mock: MockRouter, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        # ANTHROPIC_API_KEY takes precedence over the credential chain — credentials
        # stays None and X-Api-Key is used (existing behavior preserved).
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-ant-api-key")
        # also set chain env vars; they should be ignored
        clean_env.setenv("ANTHROPIC_CONFIG_DIR", str(tmp_path))
        _write_profile(tmp_path, "default", {"type": "external"}, {"access_token": "should-not-be-used"})

        _mock_messages_endpoint(respx_mock)

        client = Anthropic()
        assert client.credentials is None
        assert client._token_cache is None
        _send_message(client)

        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        assert req.headers["X-Api-Key"] == "sk-ant-api-key"
        assert "Authorization" not in req.headers

    def test_copy_propagates_credentials(self) -> None:
        creds = StaticToken("a")
        client = Anthropic(credentials=creds)
        copied = client.copy()
        assert copied.credentials is creds
        # The TokenCache instance is shared so a with_options() copy doesn't
        # trigger an independent token exchange.
        assert copied._token_cache is client._token_cache

        other = StaticToken("b")
        copied2 = client.copy(credentials=other)
        assert copied2.credentials is other
        assert copied2._token_cache is not client._token_cache

        cleared = client.copy(credentials=None, api_key="x")
        assert cleared.credentials is None
        assert cleared._token_cache is None

    def test_with_options_alias(self) -> None:
        client = Anthropic(credentials=StaticToken("a"))
        copied = client.with_options(max_retries=7)
        assert copied.max_retries == 7
        assert copied.credentials is client.credentials

    @pytest.mark.respx()
    def test_config_param_builds_in_memory_federation(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """``Anthropic(config={...})`` accepts a config-file-shaped dict and
        wires it through to a federation provider, including ``workspace_id``
        as a default header."""
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt-value")
        _mock_token_endpoint(respx_mock)
        _mock_messages_endpoint(respx_mock)

        client = Anthropic(
            config={
                "organization_id": "org_x",
                "workspace_id": "wrkspc_x",
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_x",
                    "identity_token": {"source": "file", "path": str(jwt_path)},
                },
            }
        )
        assert isinstance(client.credentials, InMemoryConfig)
        _send_message(client)
        msg_req = cast("list[MockRequestCall]", respx_mock.calls)[-1].request
        assert msg_req.headers["Authorization"] == "Bearer sk-ant-oat01-test"
        # Federation tokens are workspace-scoped server-side; header is suppressed.
        assert "anthropic-workspace-id" not in msg_req.headers

    def test_config_and_credentials_mutually_exclusive(self) -> None:
        with pytest.raises(TypeError, match="at most one of"):
            Anthropic(
                credentials=StaticToken("a"),
                config={"authentication": {"type": "oidc_federation"}},
            )

    def test_explicit_api_key_shadows_explicit_config(self, tmp_path: pathlib.Path) -> None:
        """Explicit ``api_key=`` + explicit ``config=`` is an explicit-explicit
        shadow case: the static api_key wins at the header level and the
        config-derived credentials provider is silently disabled.
        """
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt.ext-jwt.ext-jwt")
        cfg = {
            "organization_id": "org_x",
            "authentication": {
                "type": "oidc_federation",
                "federation_rule_id": "fdrl_x",
                "identity_token": {"source": "file", "path": str(jwt_path)},
            },
        }
        explicit = Anthropic(api_key="sk-explicit", config=cfg)
        assert explicit.api_key == "sk-explicit"
        assert isinstance(explicit.credentials, InMemoryConfig)

    def test_explicit_config_beats_env_api_key(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit ``config=`` is step 1 and beats env ``ANTHROPIC_API_KEY``
        (step 2). The env api_key is ignored entirely and the config-derived
        credentials provider wins.
        """
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt.ext-jwt.ext-jwt")
        client = Anthropic(
            config={
                "organization_id": "org_x",
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_x",
                    "identity_token": {"source": "file", "path": str(jwt_path)},
                },
            }
        )
        assert client.api_key is None
        assert isinstance(client.credentials, InMemoryConfig)

    def test_profile_param_loads_named_profile(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """``Anthropic(profile="staging")`` loads ``configs/staging.json`` from
        the config directory, equivalent to setting ``ANTHROPIC_PROFILE``."""
        monkeypatch.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(
            tmp_path,
            "staging",
            config={"type": "external", "base_url": "https://staging.example"},
            credentials={"access_token": "sk-ant-oat01-staging"},
        )
        client = Anthropic(profile="staging")
        assert isinstance(client.credentials, CredentialsFile)
        assert client.credentials.profile == "staging"
        assert str(client.base_url).rstrip("/") == "https://staging.example"

    def test_profile_and_config_mutually_exclusive(self) -> None:
        with pytest.raises(TypeError, match="at most one of"):
            Anthropic(profile="x", config={"authentication": {"type": "oidc_federation"}})

    def test_profile_and_credentials_mutually_exclusive(self) -> None:
        with pytest.raises(TypeError, match="at most one of"):
            Anthropic(profile="x", credentials=StaticToken("a"))

    def test_explicit_profile_beats_env_api_key(self, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit ``profile=`` is a constructor argument and beats env
        ``ANTHROPIC_API_KEY`` — the env var is not consulted."""
        monkeypatch.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        _write_profile(tmp_path, "dev", config={"type": "external"}, credentials={"access_token": "sk-ant-oat01-dev"})
        client = Anthropic(profile="dev")
        assert client.api_key is None
        assert isinstance(client.credentials, CredentialsFile)
        assert client.credentials.profile == "dev"

    def test_workload_identity_error_propagates_through_request_flow(self) -> None:
        """A WorkloadIdentityError raised from the credential provider must
        bubble out of messages.create() as-is, not wrapped in
        APIConnectionError, and must not trigger retries."""
        provider_calls: List[str] = []

        def failing_provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append("called")
            raise WorkloadIdentityError(
                "simulated 403",
                status_code=403,
                body={"error": {"type": "permission_error", "message": "Permission denied"}},
            )

        client = Anthropic(credentials=failing_provider, max_retries=3)
        with pytest.raises(WorkloadIdentityError) as exc_info:
            _send_message(client)
        assert exc_info.value.status_code == 403
        body = cast("Dict[str, Any]", exc_info.value.body)
        assert body["error"]["type"] == "permission_error"
        assert len(provider_calls) == 1


class TestInMemoryConfig:
    @pytest.mark.respx()
    def test_oidc_federation(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        jwt_path = tmp_path / "jwt"
        jwt_path.write_text("ext-jwt")
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 600})
        )
        provider = InMemoryConfig(
            {
                "organization_id": "org_x",
                "workspace_id": "wrkspc_x",
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_x",
                    "service_account_id": "svac_x",
                    "identity_token": {"source": "file", "path": str(jwt_path)},
                },
            }
        )
        token = provider()
        assert token.token == "tok"
        # Federation tokens are workspace-scoped server-side; header suppressed.
        assert provider.extra_headers() == {}
        body = json.loads(cast("list[MockRequestCall]", respx_mock.calls)[0].request.content)
        assert body["federation_rule_id"] == "fdrl_x"
        assert body["organization_id"] == "org_x"
        assert body["service_account_id"] == "svac_x"

    def test_identity_token_provider_override(self, respx_mock: MockRouter) -> None:
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 600})
        )
        provider = InMemoryConfig(
            {
                "organization_id": "org_x",
                "authentication": {"type": "oidc_federation", "federation_rule_id": "fdrl_x"},
            },
            identity_token_provider=lambda: "programmatic-jwt",
        )
        provider()
        body = json.loads(cast("list[MockRequestCall]", respx_mock.calls)[0].request.content)
        assert body["assertion"] == "programmatic-jwt"

    @pytest.mark.respx()
    def test_oidc_federation_no_credentials_path_no_disk_cache(
        self, respx_mock: MockRouter, tmp_path: pathlib.Path
    ) -> None:
        """Without ``authentication.credentials_path``, every call exchanges
        fresh — nothing is written to disk."""
        token_route = respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 600})
        )
        provider = InMemoryConfig(
            {
                "organization_id": "org_x",
                "authentication": {"type": "oidc_federation", "federation_rule_id": "fdrl_x"},
            },
            identity_token_provider=lambda: "jwt",
        )
        provider()
        provider()
        assert token_route.call_count == 2
        assert not list(tmp_path.glob("**/*.json"))

    @pytest.mark.respx()
    def test_oidc_federation_with_credentials_path_disk_cache(
        self, respx_mock: MockRouter, tmp_path: pathlib.Path
    ) -> None:
        """With ``authentication.credentials_path`` set, the exchanged token is
        written to that path and a second call returns it without re-exchanging."""
        creds_path = tmp_path / "cache.json"
        token_route = respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "cached-tok", "expires_in": 600})
        )
        provider = InMemoryConfig(
            {
                "organization_id": "org_x",
                "authentication": {
                    "type": "oidc_federation",
                    "federation_rule_id": "fdrl_x",
                    "credentials_path": str(creds_path),
                },
            },
            identity_token_provider=lambda: "jwt",
        )
        assert provider().token == "cached-tok"
        assert token_route.call_count == 1
        on_disk = json.loads(creds_path.read_text())
        assert on_disk["access_token"] == "cached-tok"
        assert on_disk["type"] == "oauth_token"
        if os.name == "posix":
            assert (creds_path.stat().st_mode & 0o777) == 0o600
        # Second call hits disk cache, not network.
        assert provider().token == "cached-tok"
        assert token_route.call_count == 1

    def test_user_oauth_requires_credentials_path(self) -> None:
        with pytest.raises(AnthropicError, match="requires 'authentication.credentials_path'"):
            InMemoryConfig({"authentication": {"type": "user_oauth", "client_id": "cid"}})

    @pytest.mark.respx()
    def test_user_oauth_refresh_and_writeback(self, respx_mock: MockRouter, tmp_path: pathlib.Path) -> None:
        """user_oauth with ``credentials_path`` runs the refresh-token grant on
        expiry and writes the new tokens back, exactly like a file-backed
        ``CredentialsFile`` profile."""
        creds_path = tmp_path / "creds.json"
        creds_path.write_text(
            json.dumps(
                {
                    "type": "oauth_token",
                    "access_token": "old-tok",
                    "expires_at": int(time.time()) - 1,
                    "refresh_token": "refresh-old",
                }
            )
        )
        creds_path.chmod(0o600)
        refresh_route = respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(
                200, json={"access_token": "new-tok", "expires_in": 3600, "refresh_token": "refresh-new"}
            )
        )
        provider = InMemoryConfig(
            {
                "workspace_id": "wrkspc_x",
                "authentication": {
                    "type": "user_oauth",
                    "client_id": "cid",
                    "credentials_path": str(creds_path),
                },
            }
        )
        tok = provider()
        assert tok.token == "new-tok"
        assert refresh_route.call_count == 1
        rewritten = json.loads(creds_path.read_text())
        assert rewritten["access_token"] == "new-tok"
        assert rewritten["refresh_token"] == "refresh-new"
        # workspace-id header IS set for user_oauth (federation suppresses it).
        assert provider.extra_headers() == {"anthropic-workspace-id": "wrkspc_x"}

    def test_unknown_type_rejected(self) -> None:
        with pytest.raises(AnthropicError, match="Unknown authentication.type"):
            InMemoryConfig({"authentication": {"type": "something_else"}})

    def test_missing_authentication(self) -> None:
        with pytest.raises(AnthropicError, match="missing the 'authentication' object"):
            InMemoryConfig({"organization_id": "org_x"})

    def test_missing_required_fields(self) -> None:
        provider = InMemoryConfig(
            {"authentication": {"type": "oidc_federation"}},
            identity_token_provider=lambda: "j",
        )
        with pytest.raises(WorkloadIdentityError, match="federation_rule_id"):
            provider()

    def test_http_base_url_rejected(self) -> None:
        with pytest.raises(AnthropicError, match="must use https"):
            InMemoryConfig(
                {
                    "organization_id": "org_x",
                    "base_url": "http://example.com",
                    "authentication": {"type": "oidc_federation", "federation_rule_id": "fdrl_x"},
                },
                identity_token_provider=lambda: "j",
            )


async def _send_message_async(client: AsyncAnthropic) -> None:
    await client.messages.create(
        max_tokens=1,
        model="claude-opus-4-5",
        messages=[{"role": "user", "content": "hi"}],
    )


@pytest.mark.usefixtures("clean_env", "no_default_creds_file")
class TestAsyncAnthropicCredentials:
    @pytest.mark.respx()
    async def test_async_static_token(self, respx_mock: MockRouter) -> None:
        _mock_messages_endpoint(respx_mock)
        client = AsyncAnthropic(credentials=StaticToken("async-bearer"))
        await _send_message_async(client)
        req = cast("list[MockRequestCall]", respx_mock.calls)[0].request
        assert req.headers["Authorization"] == "Bearer async-bearer"
        assert OAUTH_API_BETA_HEADER in req.headers["anthropic-beta"]

    @pytest.mark.respx()
    async def test_async_workload_identity_exchange(self, respx_mock: MockRouter) -> None:
        """Async client exchanges the OIDC JWT via the token endpoint and
        attaches the resulting Bearer token to the request."""
        _mock_token_endpoint(respx_mock)
        _mock_messages_endpoint(respx_mock)
        client = AsyncAnthropic(
            credentials=WorkloadIdentityCredentials(
                identity_token_provider=lambda: "ext-jwt",
                federation_rule_id="fdrl_01abc",
                organization_id="org-uuid",
            ),
        )
        await _send_message_async(client)
        msg_calls = [
            c for c in cast("list[MockRequestCall]", respx_mock.calls) if str(c.request.url).endswith("/v1/messages")
        ]
        assert len(msg_calls) == 1
        assert msg_calls[0].request.headers["Authorization"] == "Bearer sk-ant-oat01-test"

    @pytest.mark.respx()
    async def test_async_authorized_user_refresh_flow(
        self,
        respx_mock: MockRouter,
        tmp_path: pathlib.Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Async client calling a CredentialsFile(authorized_user) provider: the
        blocking refresh_token POST runs on the worker thread via asyncify."""
        monkeypatch.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(
            tmp_path,
            "default",
            {"type": "authorized_user", "client_id": "cid"},
            {"access_token": "old", "expires_at": int(time.time()) - 1, "refresh_token": "rt"},
        )
        respx_mock.post(TOKEN_URL).mock(
            return_value=httpx.Response(200, json={"access_token": "refreshed", "expires_in": 3600})
        )
        _mock_messages_endpoint(respx_mock)
        client = AsyncAnthropic(credentials=CredentialsFile())
        await _send_message_async(client)
        msg_calls = [
            c for c in cast("list[MockRequestCall]", respx_mock.calls) if str(c.request.url).endswith("/v1/messages")
        ]
        assert msg_calls[0].request.headers["Authorization"] == "Bearer refreshed"

    @pytest.mark.respx()
    async def test_async_concurrent_requests_single_flight(self, respx_mock: MockRouter) -> None:
        """Concurrent async requests sharing a TokenCache cause at most one
        provider call — the single-flight guarantee holds across async workers."""
        _mock_messages_endpoint(respx_mock)
        calls: List[int] = []

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            calls.append(1)
            time.sleep(0.05)  # widen the window for racing workers
            return AccessToken(token=f"tok-{len(calls)}", expires_at=None)

        import asyncio

        client = AsyncAnthropic(credentials=provider)
        await asyncio.gather(*(_send_message_async(client) for _ in range(8)))
        # Exactly one provider call across eight concurrent requests.
        assert len(calls) == 1

    @pytest.mark.respx()
    async def test_async_401_invalidates_and_retries_once(self, respx_mock: MockRouter) -> None:
        """Async client 401 behavior mirrors sync: invalidate the cache and
        retry the current request once with a freshly minted token."""
        respx_mock.post(f"{BASE_URL}/v1/messages").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"}),
        )
        provider_calls: List[str] = []

        def provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append("called")
            return AccessToken(token=f"tok-{len(provider_calls)}", expires_at=None)

        client = AsyncAnthropic(credentials=provider, max_retries=2)
        with pytest.raises(anthropic.AuthenticationError):
            await _send_message_async(client)
        assert len(provider_calls) == 2

    async def test_async_close_cascades_to_credentials(self) -> None:
        """AsyncAnthropic.close() cascades to self.credentials.close()."""

        class TrackedProvider:
            closed = False

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                return AccessToken(token="t", expires_at=None)

            def close(self) -> None:
                self.closed = True

        tracked = TrackedProvider()
        client = AsyncAnthropic(credentials=tracked)
        await client.close()
        assert tracked.closed

    async def test_async_aclose_via_context_manager(self) -> None:
        """`async with AsyncAnthropic(...)` exits cleanly and cascades close."""

        class TrackedProvider:
            closed = False

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                return AccessToken(token="t", expires_at=None)

            def close(self) -> None:
                self.closed = True

        tracked = TrackedProvider()
        async with AsyncAnthropic(credentials=tracked) as _client:
            pass
        assert tracked.closed

    @pytest.mark.respx()
    async def test_async_max_retries_zero_honored_on_401(self, respx_mock: MockRouter) -> None:
        """max_retries=0 means a 401 surfaces immediately — no implicit retry."""
        respx_mock.post(f"{BASE_URL}/v1/messages").mock(
            return_value=httpx.Response(401, json={"error": "unauthorized"}),
        )
        client = AsyncAnthropic(credentials=StaticToken("t"), max_retries=0)
        with pytest.raises(anthropic.AuthenticationError):
            await _send_message_async(client)
        # Exactly one request attempt, not two.
        assert len(cast("list[MockRequestCall]", respx_mock.calls)) == 1

    async def test_async_workload_identity_error_propagates_through_request_flow(self) -> None:
        """Async counterpart of the sync regression test: a WorkloadIdentityError
        raised by the credential provider must bubble out of the async
        messages.create() as-is, not wrapped in APIConnectionError, and must
        not trigger retries."""
        provider_calls: List[str] = []

        def failing_provider(*, force_refresh: bool = False) -> AccessToken:  # noqa: ARG001
            provider_calls.append("called")
            raise WorkloadIdentityError(
                "simulated 403",
                status_code=403,
                body={"error": {"type": "permission_error", "message": "Permission denied"}},
            )

        client = AsyncAnthropic(credentials=failing_provider, max_retries=3)
        with pytest.raises(WorkloadIdentityError) as exc_info:
            await _send_message_async(client)
        assert exc_info.value.status_code == 403
        body = cast("Dict[str, Any]", exc_info.value.body)
        assert body["error"]["type"] == "permission_error"
        assert len(provider_calls) == 1


@pytest.mark.usefixtures("clean_env", "no_default_creds_file")
class TestTypedCredentialErrors:
    """Every exit point in the credentials subsystem raises an ``AnthropicError``
    (or subclass). Anything outside that hierarchy is wrapped as
    ``APIConnectionError`` and retried by the base client's ``except Exception``
    handler, hiding the real cause and amplifying load.
    """

    def test_invalid_profile_name_raises_anthropic_error(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_PROFILE", "work/dev")
        with pytest.raises(AnthropicError, match="ANTHROPIC_PROFILE"):
            Anthropic()

    def test_profile_name_with_dot_prefix_raises_anthropic_error(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        clean_env.setenv("ANTHROPIC_PROFILE", ".hidden")
        with pytest.raises(AnthropicError, match="start with a dot"):
            Anthropic()

    def test_http_base_url_on_workload_provider_raises_anthropic_error(self) -> None:
        creds = WorkloadIdentityCredentials(
            identity_token_provider=lambda: "jwt",
            federation_rule_id="fdrl_x",
            organization_id="org_x",
        )
        with pytest.raises(AnthropicError, match="https"):
            creds.bind_base_url("http://evil.example/")

    def test_http_base_url_in_config_file_raises_anthropic_error(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(
            tmp_path,
            "default",
            {
                "base_url": "http://api.example/",
                "authentication": {"type": "user_oauth"},
            },
            {"access_token": "tok"},
        )
        with pytest.raises(AnthropicError, match="https"):
            CredentialsFile("default")()

    def test_identity_token_file_permission_error_raises_anthropic_error(self, tmp_path: pathlib.Path) -> None:
        if os.name != "posix":
            pytest.skip("chmod semantics only apply on POSIX")
        if os.geteuid() == 0:
            pytest.skip("root bypasses POSIX mode bits")
        f = tmp_path / "token"
        f.write_text("jwt")
        f.chmod(0o000)
        try:
            provider = IdentityTokenFile(f)
            with pytest.raises(AnthropicError, match="not readable|Permission"):
                provider()
        finally:
            f.chmod(0o600)

    def test_identity_token_file_directory_raises_anthropic_error(self, tmp_path: pathlib.Path) -> None:
        provider = IdentityTokenFile(tmp_path)
        with pytest.raises(AnthropicError):
            provider()

    def test_identity_token_file_binary_content_raises_anthropic_error(self, tmp_path: pathlib.Path) -> None:
        f = tmp_path / "token"
        f.write_bytes(b"\xff\xfe\xfd\x00not-utf8")
        provider = IdentityTokenFile(f)
        with pytest.raises(AnthropicError):
            provider()

    def test_identity_token_file_empty_raises_anthropic_error(self, tmp_path: pathlib.Path) -> None:
        f = tmp_path / "token"
        f.write_text("")
        provider = IdentityTokenFile(f)
        with pytest.raises(AnthropicError, match="empty"):
            provider()

    def test_user_oauth_malformed_expires_at_raises_anthropic_error(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        """An ISO8601 string in ``expires_at`` must raise AnthropicError naming the expected shape."""
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        _write_profile(
            tmp_path,
            "default",
            {"authentication": {"type": "user_oauth"}},
            {"access_token": "tok", "expires_at": "2030-01-01T00:00:00Z"},
        )
        with pytest.raises(AnthropicError, match="expires_at"):
            CredentialsFile("default")()


class TestTokenCacheDeadlock:
    def test_non_anthropic_error_from_provider_releases_waiters(self) -> None:
        """A non-``AnthropicError`` / non-``httpx.HTTPError`` from the leader
        provider must still release ``_refresh_event`` so concurrent waiters
        don't deadlock."""
        import threading as _threading

        ready = _threading.Event()
        release_leader = _threading.Event()

        class FlakyProvider:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                if self.calls == 1:
                    ready.set()
                    release_leader.wait(timeout=2)
                    raise RuntimeError("programmer error from a custom provider")
                return AccessToken("fresh", expires_at=None)

        provider = FlakyProvider()
        cache = TokenCache(provider)

        leader_error: List[BaseException] = []

        def run_leader() -> None:
            try:
                cache.get_token()
            except BaseException as err:
                leader_error.append(err)

        leader = _threading.Thread(target=run_leader, daemon=True)
        leader.start()
        assert ready.wait(timeout=2)

        waiter_error: List[BaseException] = []
        waiter_result: List[str] = []

        def run_waiter() -> None:
            try:
                waiter_result.append(cache.get_token())
            except BaseException as err:
                waiter_error.append(err)

        waiter = _threading.Thread(target=run_waiter, daemon=True)
        waiter.start()

        release_leader.set()
        leader.join(timeout=5)
        assert not leader.is_alive(), "leader deadlocked after provider raised"
        waiter.join(timeout=5)
        assert not waiter.is_alive(), "waiter deadlocked after leader failed"

        assert len(leader_error) == 1
        assert isinstance(leader_error[0], RuntimeError)

        assert cache.get_token() == "fresh"

    def test_value_error_from_provider_propagates_cleanly(self) -> None:
        """A ``ValueError`` (e.g. from a provider that parses a JWT) escapes
        but the cache state is clean — the next call succeeds without hanging."""

        class P:
            calls = 0

            def __call__(self, *, force_refresh: bool = False) -> AccessToken:  # noqa: ARG002
                self.calls += 1
                if self.calls == 1:
                    raise ValueError("malformed assertion")
                return AccessToken("ok", expires_at=None)

        cache = TokenCache(P())
        with pytest.raises(ValueError, match="malformed assertion"):
            cache.get_token()
        assert cache.get_token() == "ok"


@pytest.mark.usefixtures("clean_env", "no_default_creds_file")
class TestCredentialPrecedence:
    """Credential precedence per the WIF user guide and the credential-
    resolution spec: explicit ctor args (step 1) beat env vars (step 2),
    which beat profile / federation auto-discovery (steps 3-5).

    A static env credential (step 2) shadows auto-discovery (steps 3-5),
    silently disabling profile / federation — we warn about that. It does
    NOT shadow an explicit ``credentials=`` argument (step 1): an explicit
    credentials provider wins over env ``ANTHROPIC_API_KEY`` /
    ``ANTHROPIC_AUTH_TOKEN`` outright.

    Passing an explicit ``api_key=`` or ``auth_token=`` *argument* alongside
    an explicit ``credentials=`` is a separate shadow case: the static
    credential wins at the header level and we warn.
    """

    @pytest.fixture(autouse=True)
    def _reset_shadow_one_shot(self) -> None:
        from anthropic.lib.credentials import _auth

        _auth._warn_once_seen.clear()

    @staticmethod
    def _walk_sync_auth(client: Anthropic) -> httpx.Request:
        request = client._build_request(FinalRequestOptions(method="get", url="/foo"))
        auth = client.custom_auth
        flow = auth.sync_auth_flow(request) if auth is not None else None
        if flow is None:
            return request
        modified = next(flow)
        try:
            flow.send(httpx.Response(200))
        except StopIteration:
            pass
        return modified

    # -- step 1 beats step 2: explicit credentials= beats env static --------

    def test_explicit_credentials_beats_env_api_key(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Per spec, explicit ``credentials=`` is step 1 and beats env
        ``ANTHROPIC_API_KEY`` (step 2). The credentials provider wins, env
        api_key is ignored entirely, no X-Api-Key on the wire, no warning."""
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic(credentials=StaticToken("bearer-from-creds"))
        assert client.api_key is None
        assert client.auth_token is None
        assert client.credentials is not None
        req = self._walk_sync_auth(client)
        assert req.headers.get("X-Api-Key") is None
        assert req.headers.get("Authorization") == "Bearer bearer-from-creds"
        assert not any("takes precedence" in r.message for r in caplog.records)

    def test_explicit_credentials_beats_env_auth_token(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        clean_env.setenv("ANTHROPIC_AUTH_TOKEN", "env-auth-token")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic(credentials=StaticToken("bearer-from-creds"))
        assert client.auth_token is None
        assert client.credentials is not None
        req = self._walk_sync_auth(client)
        assert req.headers.get("Authorization") == "Bearer bearer-from-creds"
        assert not any("takes precedence" in r.message for r in caplog.records)

    def test_explicit_config_beats_env_api_key(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture, tmp_path: pathlib.Path
    ) -> None:
        """Explicit ``config=`` is also step 1 and beats env api_key."""
        jwt = tmp_path / "jwt"
        jwt.write_text("ext-jwt.ext-jwt.ext-jwt")
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic(
                config={
                    "organization_id": "org_x",
                    "authentication": {
                        "type": "oidc_federation",
                        "federation_rule_id": "fdrl_x",
                        "identity_token": {"source": "file", "path": str(jwt)},
                    },
                }
            )
        assert client.api_key is None
        assert isinstance(client.credentials, InMemoryConfig)

    # -- step 1 ∩ step 1: explicit static arg + explicit credentials= --------

    def test_explicit_api_key_shadows_explicit_credentials_with_warning(self, caplog: pytest.LogCaptureFixture) -> None:
        """When both explicit ``api_key=`` AND explicit ``credentials=`` are
        passed, the static api_key wins at the header level and credentials
        is silently disabled. Warn."""
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic(api_key="sk-explicit", credentials=StaticToken("bearer-from-creds"))
        req = self._walk_sync_auth(client)
        assert req.headers.get("X-Api-Key") == "sk-explicit"
        assert req.headers.get("Authorization") is None
        assert any("`api_key=`" in r.message for r in caplog.records)

    def test_explicit_auth_token_shadows_explicit_credentials_with_warning(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic(auth_token="static-bearer", credentials=StaticToken("bearer-from-creds"))
        req = self._walk_sync_auth(client)
        assert req.headers.get("Authorization") == "Bearer static-bearer"
        assert req.headers.get("X-Api-Key") is None
        assert any("`auth_token=`" in r.message for r in caplog.records)

    def test_async_explicit_api_key_shadows_explicit_credentials(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = AsyncAnthropic(api_key="sk-explicit", credentials=StaticToken("bearer-from-creds"))
        assert client.api_key == "sk-explicit"
        assert client.credentials is not None
        assert any("`api_key=`" in r.message for r in caplog.records)

    def test_copy_with_explicit_api_key_shadows_inherited_credentials(self, caplog: pytest.LogCaptureFixture) -> None:
        """Reviewer ask: copy() should warn when a new explicit ``api_key=``
        shadows an inherited ``credentials=`` provider from the parent."""
        parent = Anthropic(credentials=StaticToken("bearer-parent"))
        assert parent.api_key is None
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            shadowed = parent.copy(api_key="sk-new")
        assert shadowed.api_key == "sk-new"
        assert shadowed.credentials is parent.credentials
        req = self._walk_sync_auth(shadowed)
        assert req.headers.get("X-Api-Key") == "sk-new"
        assert req.headers.get("Authorization") is None
        assert any("`api_key=`" in r.message for r in caplog.records)

    # -- step 2 shadows steps 3-5: env static shadows auto-discovery ---------

    def test_env_api_key_shadows_env_federation_trio_with_warning(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture, tmp_path: pathlib.Path
    ) -> None:
        """Env ``ANTHROPIC_API_KEY`` + env federation trio → api_key wins
        (step 2 beats step 4), warn so the user knows WIF is being shadowed."""
        jwt = tmp_path / "jwt"
        jwt.write_text("ext-jwt.ext-jwt.ext-jwt")
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        clean_env.setenv("ANTHROPIC_IDENTITY_TOKEN_FILE", str(jwt))
        clean_env.setenv("ANTHROPIC_FEDERATION_RULE_ID", "fdrl_01abc")
        clean_env.setenv("ANTHROPIC_ORGANIZATION_ID", "00000000-0000-0000-0000-000000000000")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic()
        assert client.api_key == "sk-from-env"
        assert client.credentials is None
        assert any("ANTHROPIC_API_KEY" in r.message and "profile / federation" in r.message for r in caplog.records)

    def test_env_api_key_shadows_env_profile_with_warning(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        clean_env.setenv("ANTHROPIC_PROFILE", "dev")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic()
        assert client.api_key == "sk-from-env"
        assert client.credentials is None
        assert any("ANTHROPIC_API_KEY" in r.message and "profile / federation" in r.message for r in caplog.records)

    def test_env_api_key_alone_does_not_warn(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        """No shadow if there's nothing to shadow — env api_key alone (no
        auto-discoverable credential signals) is just the normal path."""
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic()
        assert client.api_key == "sk-from-env"
        assert not any("takes precedence" in r.message for r in caplog.records)

    # -- step 1 alone: credentials= works normally --------------------------

    def test_credentials_only_still_works(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            client = Anthropic(credentials=StaticToken("bearer-from-creds"))
        req = self._walk_sync_auth(client)
        assert req.headers.get("X-Api-Key") is None
        assert req.headers.get("Authorization") == "Bearer bearer-from-creds"
        assert not any("takes precedence" in r.message for r in caplog.records)

    # -- one-shot warning ---------------------------------------------------

    def test_shadow_warning_is_one_shot_per_process(
        self, clean_env: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        """The shadow warning is emitted once per shadow-key per process so
        repeated client construction doesn't spam logs."""
        clean_env.setenv("ANTHROPIC_API_KEY", "sk-from-env")
        clean_env.setenv("ANTHROPIC_PROFILE", "dev")
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.credentials._auth"):
            Anthropic()
            Anthropic()
            Anthropic()
        shadow_records = [r for r in caplog.records if "takes precedence" in r.message]
        assert len(shadow_records) == 1


@pytest.mark.usefixtures("clean_env", "no_default_creds_file")
class TestDanglingActiveConfig:
    """``active_config`` pointer file naming a profile with no matching
    ``configs/<profile>.json`` should surface a clear error rather than
    silently falling through to "no auth configured".
    """

    def test_pointer_at_missing_profile_raises(self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        (tmp_path / "active_config").write_text("prod")
        with pytest.raises(AnthropicError, match="prod"):
            default_credentials()

    def test_pointer_at_missing_profile_raises_via_client(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        (tmp_path / "active_config").write_text("prod")
        with pytest.raises(AnthropicError, match="prod"):
            Anthropic()

    def test_empty_pointer_file_is_silent_fallthrough(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        (tmp_path / "active_config").write_text("")
        assert default_credentials() is None

    def test_pointer_at_present_profile_loads_normally(
        self, clean_env: pytest.MonkeyPatch, tmp_path: pathlib.Path
    ) -> None:
        clean_env.setattr("anthropic.lib.credentials._constants._config_dir", lambda: tmp_path)
        (tmp_path / "active_config").write_text("prod")
        _write_profile(tmp_path, "prod", {"type": "external"}, {"access_token": "from-prod"})
        result = default_credentials()
        assert result is not None
        assert isinstance(result.provider, CredentialsFile)
        assert result.provider().token == "from-prod"
