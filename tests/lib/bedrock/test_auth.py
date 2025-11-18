"""Tests for Bedrock authentication."""

from __future__ import annotations

from unittest import mock

import httpx
import pytest

# Only run these tests if boto3 is available
boto3 = pytest.importorskip("boto3")
botocore = pytest.importorskip("botocore")

from anthropic.lib.bedrock._auth import get_auth_headers, _get_session


class TestBedrockAuth:
    """Test Bedrock authentication functionality."""

    def test_get_session_with_explicit_credentials(self) -> None:
        """Test creating a boto3 session with explicit credentials."""
        session = _get_session(
            aws_access_key="test-access-key",
            aws_secret_key="test-secret-key",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
        )

        assert session is not None
        assert session.region_name == "us-east-1"

    def test_get_session_with_profile(self) -> None:
        """Test creating a boto3 session with a profile."""
        # This will try to load from AWS config, but won't fail
        session = _get_session(
            aws_access_key=None,
            aws_secret_key=None,
            aws_session_token=None,
            region="us-west-2",
            profile="default",
        )

        assert session is not None

    def test_get_session_with_session_token(self) -> None:
        """Test creating a boto3 session with temporary credentials."""
        session = _get_session(
            aws_access_key="test-access-key",
            aws_secret_key="test-secret-key",
            aws_session_token="test-session-token",
            region="eu-west-1",
            profile=None,
        )

        assert session is not None
        assert session.region_name == "eu-west-1"

    def test_get_session_caching(self) -> None:
        """Test that _get_session caches sessions with the same parameters."""
        session1 = _get_session(
            aws_access_key="test-key",
            aws_secret_key="test-secret",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
        )

        session2 = _get_session(
            aws_access_key="test-key",
            aws_secret_key="test-secret",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
        )

        # Should be the exact same object due to caching
        assert session1 is session2

    def test_get_session_different_params_creates_new_session(self) -> None:
        """Test that different parameters create different sessions."""
        session1 = _get_session(
            aws_access_key="test-key-1",
            aws_secret_key="test-secret-1",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
        )

        session2 = _get_session(
            aws_access_key="test-key-2",
            aws_secret_key="test-secret-2",
            aws_session_token=None,
            region="us-east-1",
            profile=None,
        )

        # Should be different objects
        assert session1 is not session2

    def test_get_auth_headers_removes_connection_header(self) -> None:
        """Test that the connection header is removed before signing."""
        from botocore.credentials import Credentials

        headers = httpx.Headers(
            {
                "connection": "keep-alive",
                "content-type": "application/json",
            }
        )

        with mock.patch("anthropic.lib.bedrock._auth._get_session") as mock_session:
            mock_boto_session = mock.Mock()
            mock_credentials = Credentials(
                access_key="test-access-key",
                secret_key="test-secret-key",
            )
            mock_boto_session.get_credentials.return_value = mock_credentials
            mock_boto_session.region_name = "us-east-1"
            mock_session.return_value = mock_boto_session

            auth_headers = get_auth_headers(
                method="POST",
                url="https://bedrock-runtime.us-east-1.amazonaws.com/model/test/invoke",
                headers=headers,
                aws_access_key="test-access-key",
                aws_secret_key="test-secret-key",
                aws_session_token=None,
                region="us-east-1",
                profile=None,
                data='{"test": "data"}',
            )

            # Connection header should not be in auth headers
            assert "connection" not in auth_headers
            # Should have AWS signature headers
            assert "Authorization" in auth_headers or "authorization" in auth_headers

    def test_get_auth_headers_with_post_data(self) -> None:
        """Test generating auth headers with POST data."""
        from botocore.credentials import Credentials

        headers = httpx.Headers(
            {
                "content-type": "application/json",
            }
        )

        with mock.patch("anthropic.lib.bedrock._auth._get_session") as mock_session:
            mock_boto_session = mock.Mock()
            mock_credentials = Credentials(
                access_key="AKIAIOSFODNN7EXAMPLE",
                secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            )
            mock_boto_session.get_credentials.return_value = mock_credentials
            mock_boto_session.region_name = "us-east-1"
            mock_session.return_value = mock_boto_session

            auth_headers = get_auth_headers(
                method="POST",
                url="https://bedrock-runtime.us-east-1.amazonaws.com/model/test/invoke",
                headers=headers,
                aws_access_key="AKIAIOSFODNN7EXAMPLE",
                aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                aws_session_token=None,
                region="us-east-1",
                profile=None,
                data='{"max_tokens": 1024}',
            )

            assert auth_headers is not None
            assert isinstance(auth_headers, dict)
            # AWS SigV4 headers
            assert any(
                key.lower() in ["authorization", "x-amz-date", "x-amz-security-token"]
                for key in auth_headers.keys()
            )

    def test_get_auth_headers_without_data(self) -> None:
        """Test generating auth headers for GET request without data."""
        from botocore.credentials import Credentials

        headers = httpx.Headers({})

        with mock.patch("anthropic.lib.bedrock._auth._get_session") as mock_session:
            mock_boto_session = mock.Mock()
            mock_credentials = Credentials(
                access_key="test-access-key",
                secret_key="test-secret-key",
            )
            mock_boto_session.get_credentials.return_value = mock_credentials
            mock_boto_session.region_name = "us-west-2"
            mock_session.return_value = mock_boto_session

            auth_headers = get_auth_headers(
                method="GET",
                url="https://bedrock.us-west-2.amazonaws.com/model-invocations",
                headers=headers,
                aws_access_key="test-access-key",
                aws_secret_key="test-secret-key",
                aws_session_token=None,
                region="us-west-2",
                profile=None,
                data=None,
            )

            assert auth_headers is not None
            assert isinstance(auth_headers, dict)

    def test_get_auth_headers_raises_on_no_credentials(self) -> None:
        """Test that RuntimeError is raised when credentials cannot be resolved."""
        headers = httpx.Headers({"content-type": "application/json"})

        with mock.patch("anthropic.lib.bedrock._auth._get_session") as mock_session:
            mock_boto_session = mock.Mock()
            mock_boto_session.get_credentials.return_value = None
            mock_boto_session.region_name = "us-east-1"
            mock_session.return_value = mock_boto_session

            with pytest.raises(RuntimeError, match="could not resolve credentials from session"):
                get_auth_headers(
                    method="POST",
                    url="https://bedrock-runtime.us-east-1.amazonaws.com/model/test/invoke",
                    headers=headers,
                    aws_access_key=None,
                    aws_secret_key=None,
                    aws_session_token=None,
                    region="us-east-1",
                    profile="nonexistent",
                    data='{"test": "data"}',
                )

    def test_get_auth_headers_with_session_token(self) -> None:
        """Test generating auth headers with temporary session token."""
        from botocore.credentials import Credentials

        headers = httpx.Headers({"content-type": "application/json"})

        with mock.patch("anthropic.lib.bedrock._auth._get_session") as mock_session:
            mock_boto_session = mock.Mock()
            mock_credentials = Credentials(
                access_key="test-access-key",
                secret_key="test-secret-key",
                token="test-session-token",
            )
            mock_boto_session.get_credentials.return_value = mock_credentials
            mock_boto_session.region_name = "ap-southeast-1"
            mock_session.return_value = mock_boto_session

            auth_headers = get_auth_headers(
                method="POST",
                url="https://bedrock-runtime.ap-southeast-1.amazonaws.com/model/test/invoke",
                headers=headers,
                aws_access_key="test-access-key",
                aws_secret_key="test-secret-key",
                aws_session_token="test-session-token",
                region="ap-southeast-1",
                profile=None,
                data='{"test": "data"}',
            )

            assert auth_headers is not None
            # Should include session token in headers
            assert any("amz" in key.lower() for key in auth_headers.keys())

    def test_get_auth_headers_filters_none_values(self) -> None:
        """Test that None values are filtered from auth headers."""
        from botocore.credentials import Credentials

        headers = httpx.Headers({"content-type": "application/json"})

        with mock.patch("anthropic.lib.bedrock._auth._get_session") as mock_session:
            mock_boto_session = mock.Mock()
            mock_credentials = Credentials(
                access_key="test-access-key",
                secret_key="test-secret-key",
            )
            mock_boto_session.get_credentials.return_value = mock_credentials
            mock_boto_session.region_name = "us-east-1"
            mock_session.return_value = mock_boto_session

            auth_headers = get_auth_headers(
                method="POST",
                url="https://bedrock-runtime.us-east-1.amazonaws.com/model/test/invoke",
                headers=headers,
                aws_access_key="test-access-key",
                aws_secret_key="test-secret-key",
                aws_session_token=None,
                region="us-east-1",
                profile=None,
                data='{"test": "data"}',
            )

            # All values should be non-None
            assert all(value is not None for value in auth_headers.values())
