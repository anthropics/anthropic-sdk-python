from __future__ import annotations

import re
from unittest.mock import patch

import httpx
import pytest

from anthropic.lib.aws._auth import get_auth_headers
from anthropic.lib.aws._credentials import (
    resolve_region,
    resolve_api_key,
    resolve_base_url,
    resolve_auth_mode,
    resolve_workspace_id,
    validate_credentials,
)

# --- validate_credentials ---


class TestValidateCredentials:
    def test_both_provided_passes(self) -> None:
        validate_credentials(aws_access_key="AKID", aws_secret_key="secret")

    def test_neither_provided_passes(self) -> None:
        validate_credentials(aws_access_key=None, aws_secret_key=None)

    def test_access_key_only_raises(self) -> None:
        with pytest.raises(ValueError, match="aws_access_key.*without.*aws_secret_key"):
            validate_credentials(aws_access_key="AKID", aws_secret_key=None)

    def test_secret_key_only_raises(self) -> None:
        with pytest.raises(ValueError, match="aws_secret_key.*without.*aws_access_key"):
            validate_credentials(aws_access_key=None, aws_secret_key="secret")


# --- resolve_auth_mode ---


class TestResolveAuthMode:
    def test_api_key_arg_returns_false(self) -> None:
        assert (
            resolve_auth_mode(
                api_key="key",
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
            )
            is False
        )

    def test_explicit_creds_returns_true(self) -> None:
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key="AKID",
                aws_secret_key="secret",
                aws_profile=None,
            )
            is True
        )

    def test_access_key_alone_returns_true(self) -> None:
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key="AKID",
                aws_secret_key=None,
                aws_profile=None,
            )
            is True
        )

    def test_profile_returns_true(self) -> None:
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile="my-profile",
            )
            is True
        )

    def test_env_api_key_returns_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
            )
            is False
        )

    def test_no_args_no_env_defaults_to_sigv4(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AWS_API_KEY", raising=False)
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
            )
            is True
        )

    def test_explicit_creds_suppress_env_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key="AKID",
                aws_secret_key="secret",
                aws_profile=None,
            )
            is True
        )

    def test_profile_suppresses_env_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile="my-profile",
            )
            is True
        )

    def test_api_key_arg_beats_explicit_creds(self) -> None:
        """api_key constructor arg takes highest precedence."""
        assert (
            resolve_auth_mode(
                api_key="key",
                aws_access_key="AKID",
                aws_secret_key="secret",
                aws_profile=None,
            )
            is False
        )

    def test_custom_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "mantle-key")
        monkeypatch.delenv("ANTHROPIC_AWS_API_KEY", raising=False)
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY",),
            )
            is False
        )

    def test_custom_env_var_not_set_defaults_to_sigv4(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_AWS_API_KEY", raising=False)
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY",),
            )
            is True
        )

    def test_env_var_fallback_chain_first_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """First env var in the chain takes priority."""
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "mantle-key")
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "aws-key")
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "ANTHROPIC_AWS_API_KEY"),
            )
            is False
        )

    def test_env_var_fallback_chain_falls_through(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Falls back to second env var when first is not set."""
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", raising=False)
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "aws-key")
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "ANTHROPIC_AWS_API_KEY"),
            )
            is False
        )

    def test_env_var_fallback_chain_none_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Defaults to SigV4 when no env vars in the chain are set."""
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", raising=False)
        monkeypatch.delenv("ANTHROPIC_AWS_API_KEY", raising=False)
        assert (
            resolve_auth_mode(
                api_key=None,
                aws_access_key=None,
                aws_secret_key=None,
                aws_profile=None,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "ANTHROPIC_AWS_API_KEY"),
            )
            is True
        )


# --- resolve_api_key ---


class TestResolveApiKey:
    def test_returns_arg_when_provided(self) -> None:
        assert resolve_api_key(api_key="arg-key", use_sigv4=False) == "arg-key"

    def test_returns_none_for_sigv4(self) -> None:
        assert resolve_api_key(api_key=None, use_sigv4=True) is None

    def test_returns_env_when_not_sigv4(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
        assert resolve_api_key(api_key=None, use_sigv4=False) == "env-key"

    def test_returns_none_when_not_sigv4_and_no_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AWS_API_KEY", raising=False)
        assert resolve_api_key(api_key=None, use_sigv4=False) is None

    def test_arg_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
        assert resolve_api_key(api_key="arg-key", use_sigv4=False) == "arg-key"

    def test_sigv4_ignores_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
        assert resolve_api_key(api_key=None, use_sigv4=True) is None

    def test_custom_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "mantle-key")
        assert (
            resolve_api_key(
                api_key=None,
                use_sigv4=False,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY",),
            )
            == "mantle-key"
        )

    def test_env_var_fallback_chain_first_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "mantle-key")
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "aws-key")
        assert (
            resolve_api_key(
                api_key=None,
                use_sigv4=False,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "ANTHROPIC_AWS_API_KEY"),
            )
            == "mantle-key"
        )

    def test_env_var_fallback_chain_falls_through(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_API_KEY", raising=False)
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "aws-key")
        assert (
            resolve_api_key(
                api_key=None,
                use_sigv4=False,
                api_key_env_vars=("ANTHROPIC_BEDROCK_MANTLE_API_KEY", "ANTHROPIC_AWS_API_KEY"),
            )
            == "aws-key"
        )


# --- resolve_region ---


class TestResolveRegion:
    def test_returns_arg_when_provided(self) -> None:
        assert resolve_region("us-west-2") == "us-west-2"

    def test_returns_aws_region_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AWS_REGION", "eu-west-1")
        assert resolve_region(None) == "eu-west-1"

    def test_returns_aws_default_region_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AWS_REGION", raising=False)
        monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-southeast-1")
        assert resolve_region(None) == "ap-southeast-1"

    def test_aws_region_takes_precedence_over_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AWS_REGION", "us-east-1")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")
        assert resolve_region(None) == "us-east-1"

    def test_arg_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AWS_REGION", "us-east-1")
        assert resolve_region("eu-central-1") == "eu-central-1"

    def test_returns_none_when_no_source(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AWS_REGION", raising=False)
        monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
        assert resolve_region(None) is None


# --- resolve_workspace_id ---


class TestResolveWorkspaceId:
    def test_returns_arg_when_provided(self) -> None:
        assert resolve_workspace_id("ws-123") == "ws-123"

    def test_returns_env_when_no_arg(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_WORKSPACE_ID", "env-ws")
        assert resolve_workspace_id(None) == "env-ws"

    def test_returns_none_when_no_source(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
        assert resolve_workspace_id(None) is None

    def test_arg_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_WORKSPACE_ID", "env-ws")
        assert resolve_workspace_id("arg-ws") == "arg-ws"

    def test_custom_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", "mantle-ws")
        assert (
            resolve_workspace_id(
                None,
                workspace_id_env_vars=("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID",),
            )
            == "mantle-ws"
        )

    def test_env_var_fallback_chain_first_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", "mantle-ws")
        monkeypatch.setenv("ANTHROPIC_AWS_WORKSPACE_ID", "aws-ws")
        assert (
            resolve_workspace_id(
                None,
                workspace_id_env_vars=("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", "ANTHROPIC_AWS_WORKSPACE_ID"),
            )
            == "mantle-ws"
        )

    def test_env_var_fallback_chain_falls_through(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", raising=False)
        monkeypatch.setenv("ANTHROPIC_AWS_WORKSPACE_ID", "aws-ws")
        assert (
            resolve_workspace_id(
                None,
                workspace_id_env_vars=("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", "ANTHROPIC_AWS_WORKSPACE_ID"),
            )
            == "aws-ws"
        )

    def test_env_var_fallback_chain_none_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", raising=False)
        monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
        assert (
            resolve_workspace_id(
                None,
                workspace_id_env_vars=("ANTHROPIC_BEDROCK_MANTLE_WORKSPACE_ID", "ANTHROPIC_AWS_WORKSPACE_ID"),
            )
            is None
        )


# --- get_auth_headers ---


class TestResolveBaseUrl:
    def test_returns_arg_when_provided(self) -> None:
        assert resolve_base_url("https://custom.example.com", region="us-east-1") == "https://custom.example.com"

    def test_returns_env_when_no_arg(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://env-gateway.example.com")
        assert resolve_base_url(None, region="us-east-1") == "https://env-gateway.example.com"

    def test_derives_from_region(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AWS_BASE_URL", raising=False)
        assert resolve_base_url(None, region="us-west-2") == "https://aws-external-anthropic.us-west-2.api.aws"

    def test_returns_none_when_no_source(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AWS_BASE_URL", raising=False)
        assert resolve_base_url(None, region=None) is None

    def test_arg_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://env-gateway.example.com")
        assert resolve_base_url("https://arg.example.com", region="us-east-1") == "https://arg.example.com"

    def test_env_takes_precedence_over_region(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://env-gateway.example.com")
        assert resolve_base_url(None, region="us-east-1") == "https://env-gateway.example.com"

    def test_custom_url_template(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_AWS_BASE_URL", raising=False)
        assert (
            resolve_base_url(
                None,
                region="us-east-1",
                url_template="https://bedrock-mantle.{region}.api.aws/anthropic",
            )
            == "https://bedrock-mantle.us-east-1.api.aws/anthropic"
        )

    def test_custom_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_BASE_URL", "https://mantle.example.com")
        assert (
            resolve_base_url(
                None,
                region="us-east-1",
                base_url_env_vars=("ANTHROPIC_BEDROCK_MANTLE_BASE_URL",),
            )
            == "https://mantle.example.com"
        )

    def test_env_var_fallback_chain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ANTHROPIC_BEDROCK_MANTLE_BASE_URL", raising=False)
        monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://aws-fallback.example.com")
        assert (
            resolve_base_url(
                None,
                region="us-east-1",
                base_url_env_vars=("ANTHROPIC_BEDROCK_MANTLE_BASE_URL", "ANTHROPIC_AWS_BASE_URL"),
            )
            == "https://aws-fallback.example.com"
        )


class TestGetAuthHeaders:
    def test_uses_service_name_parameter(self) -> None:
        """service_name is passed through to SigV4Auth, not hardcoded."""
        headers = get_auth_headers(
            method="POST",
            url="https://gateway.us-east-1.api.aws/v1/messages",
            headers=httpx.Headers({"content-type": "application/json"}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
            service_name="aws-external-anthropic",
        )
        assert "Authorization" in headers
        assert "aws-external-anthropic" in headers["Authorization"]

    def test_different_service_name(self) -> None:
        """Mantle uses a different service name for SigV4 signing."""
        headers = get_auth_headers(
            method="POST",
            url="https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages",
            headers=httpx.Headers({"content-type": "application/json"}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
            service_name="bedrock-mantle",
        )
        assert "Authorization" in headers
        assert "bedrock-mantle" in headers["Authorization"]
        assert "aws-external-anthropic" not in headers["Authorization"]

    def test_returns_authorization_and_date_headers(self) -> None:
        headers = get_auth_headers(
            method="POST",
            url="https://gateway.us-east-1.api.aws/v1/messages",
            headers=httpx.Headers({"content-type": "application/json"}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
            service_name="aws-external-anthropic",
        )
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("AWS4-HMAC-SHA256")
        assert "X-Amz-Date" in headers

    def test_includes_security_token_header(self) -> None:
        headers = get_auth_headers(
            method="POST",
            url="https://gateway.us-east-1.api.aws/v1/messages",
            headers=httpx.Headers({"content-type": "application/json"}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token="FwoGZXIvYXdzEBYaDH7example",
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
            service_name="aws-external-anthropic",
        )
        assert headers.get("X-Amz-Security-Token") == "FwoGZXIvYXdzEBYaDH7example"

    def test_strips_connection_header(self) -> None:
        """Connection header must not be signed (may be stripped by proxies)."""
        headers = get_auth_headers(
            method="POST",
            url="https://gateway.us-east-1.api.aws/v1/messages",
            headers=httpx.Headers({"content-type": "application/json", "connection": "keep-alive"}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
            service_name="aws-external-anthropic",
        )
        # The signed headers in Authorization should not include "connection"
        auth = headers["Authorization"]
        signed_headers_match = re.search(r"SignedHeaders=([^,]+)", auth)
        assert signed_headers_match is not None
        signed_headers = signed_headers_match.group(1).split(";")
        assert "connection" not in signed_headers

    def test_handles_null_body(self) -> None:
        headers = get_auth_headers(
            method="GET",
            url="https://gateway.us-east-1.api.aws/v1/models",
            headers=httpx.Headers({}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data=None,
            service_name="aws-external-anthropic",
        )
        assert "Authorization" in headers

    def test_includes_query_params_in_signing(self) -> None:
        """URL query params must be part of the signed request."""
        headers_with_query = get_auth_headers(
            method="GET",
            url="https://gateway.us-east-1.api.aws/v1/models?limit=10",
            headers=httpx.Headers({}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data=None,
            service_name="aws-external-anthropic",
        )
        headers_without_query = get_auth_headers(
            method="GET",
            url="https://gateway.us-east-1.api.aws/v1/models",
            headers=httpx.Headers({}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data=None,
            service_name="aws-external-anthropic",
        )
        # Different URLs should produce different signatures
        assert headers_with_query["Authorization"] != headers_without_query["Authorization"]

    def test_uppercases_method(self) -> None:
        """Method should be uppercased for signing."""
        headers = get_auth_headers(
            method="post",
            url="https://gateway.us-east-1.api.aws/v1/messages",
            headers=httpx.Headers({}),
            aws_access_key="AKIAIOSFODNN7EXAMPLE",
            aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data="{}",
            service_name="aws-external-anthropic",
        )
        assert "Authorization" in headers

    def test_raises_on_missing_credentials(self) -> None:
        with patch("anthropic.lib.aws._auth._get_session") as mock_session:
            mock_session.return_value.get_credentials.return_value = None
            mock_session.return_value.region_name = "us-east-1"
            with pytest.raises(RuntimeError, match="Could not resolve AWS credentials"):
                get_auth_headers(
                    method="POST",
                    url="https://gateway.us-east-1.api.aws/v1/messages",
                    headers=httpx.Headers({}),
                    aws_access_key=None,
                    aws_secret_key=None,
                    aws_session_token=None,
                    region="us-east-1",
                    profile=None,
                    data="{}",
                    service_name="aws-external-anthropic",
                )
