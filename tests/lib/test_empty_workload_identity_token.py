from __future__ import annotations

import pathlib

import pytest

from anthropic import AnthropicError
from anthropic.lib.credentials import _chain
from anthropic.lib.credentials._constants import (
    ENV_IDENTITY_TOKEN,
    ENV_IDENTITY_TOKEN_FILE,
    ENV_ORGANIZATION_ID,
    ENV_FEDERATION_RULE_ID,
)


def test_empty_literal_identity_token_does_not_select_federation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_FEDERATION_RULE_ID, "fdrl_test")
    monkeypatch.setenv(ENV_ORGANIZATION_ID, "org_test")
    monkeypatch.setenv(ENV_IDENTITY_TOKEN, "")
    monkeypatch.delenv(ENV_IDENTITY_TOKEN_FILE, raising=False)

    assert _chain._build_federation_result(base_url="https://api.anthropic.com") is None


def test_literal_identity_token_cleared_after_discovery_fails_before_exchange(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_FEDERATION_RULE_ID, "fdrl_test")
    monkeypatch.setenv(ENV_ORGANIZATION_ID, "org_test")
    monkeypatch.setenv(ENV_IDENTITY_TOKEN, "initial-jwt")
    monkeypatch.delenv(ENV_IDENTITY_TOKEN_FILE, raising=False)

    result = _chain._build_federation_result(base_url="https://api.anthropic.com")
    assert result is not None

    monkeypatch.setenv(ENV_IDENTITY_TOKEN, "")
    try:
        with pytest.raises(AnthropicError, match="not set or is empty"):
            result.provider()
    finally:
        close = getattr(result.provider, "close", None)
        if close is not None:
            close()


def test_empty_literal_token_does_not_mask_identity_token_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    token_file = tmp_path / "identity-token"
    token_file.write_text("file-jwt")

    monkeypatch.setenv(ENV_FEDERATION_RULE_ID, "fdrl_test")
    monkeypatch.setenv(ENV_ORGANIZATION_ID, "org_test")
    monkeypatch.setenv(ENV_IDENTITY_TOKEN, "")
    monkeypatch.setenv(ENV_IDENTITY_TOKEN_FILE, str(token_file))

    result = _chain._build_federation_result(base_url="https://api.anthropic.com")
    assert result is not None
    try:
        provider = result.provider
        identity_provider = getattr(provider, "_identity_token_provider")
        assert identity_provider() == "file-jwt"
    finally:
        close = getattr(result.provider, "close", None)
        if close is not None:
            close()
