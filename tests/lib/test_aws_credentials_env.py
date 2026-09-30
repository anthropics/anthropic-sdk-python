from __future__ import annotations

import pytest

from anthropic.lib.aws._credentials import (
    _read_env,
    resolve_api_key,
    resolve_auth_mode,
    resolve_base_url,
    resolve_workspace_id,
)


def test_read_env_skips_empty_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_TEST_FIRST", "")
    monkeypatch.setenv("ANTHROPIC_TEST_SECOND", "configured")

    assert _read_env("ANTHROPIC_TEST_FIRST", "ANTHROPIC_TEST_SECOND") == "configured"


def test_empty_aws_api_key_env_does_not_disable_sigv4(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_TEST_AWS_API_KEY", "")

    use_sigv4 = resolve_auth_mode(
        api_key=None,
        aws_access_key=None,
        aws_secret_key=None,
        aws_profile=None,
        api_key_env_vars=("ANTHROPIC_TEST_AWS_API_KEY",),
    )

    assert use_sigv4 is True
    assert resolve_api_key(
        api_key=None,
        use_sigv4=use_sigv4,
        api_key_env_vars=("ANTHROPIC_TEST_AWS_API_KEY",),
    ) is None


def test_empty_workspace_env_is_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_TEST_AWS_WORKSPACE", "")

    assert resolve_workspace_id(None, workspace_id_env_vars=("ANTHROPIC_TEST_AWS_WORKSPACE",)) is None


def test_empty_base_url_env_falls_back_to_region(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_TEST_AWS_BASE_URL", "")

    assert (
        resolve_base_url(
            None,
            region="eu-west-1",
            base_url_env_vars=("ANTHROPIC_TEST_AWS_BASE_URL",),
        )
        == "https://aws-external-anthropic.eu-west-1.api.aws"
    )
