from __future__ import annotations

import re

import httpx

from anthropic.lib.bedrock._auth import get_auth_headers

_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


class TestGetAuthHeaders:
    def test_returns_authorization_and_date_headers(self) -> None:
        headers = get_auth_headers(
            method="POST",
            url="https://bedrock-runtime.us-east-1.amazonaws.com/model/m/invoke",
            headers=httpx.Headers({"content-type": "application/json"}),
            aws_access_key=_ACCESS_KEY,
            aws_secret_key=_SECRET_KEY,
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
        )
        assert headers["Authorization"].startswith("AWS4-HMAC-SHA256")
        assert "X-Amz-Date" in headers

    def test_strips_connection_header_from_signing(self) -> None:
        """A present connection header must not be part of the signed set."""
        headers = get_auth_headers(
            method="POST",
            url="https://bedrock-runtime.us-east-1.amazonaws.com/model/m/invoke",
            headers=httpx.Headers({"content-type": "application/json", "Connection": "keep-alive"}),
            aws_access_key=_ACCESS_KEY,
            aws_secret_key=_SECRET_KEY,
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
        )
        signed = re.search(r"SignedHeaders=([^,]+)", headers["Authorization"])
        assert signed is not None
        assert "connection" not in signed.group(1).split(";")

    def test_missing_connection_header_does_not_raise(self) -> None:
        """Regression: signing must not require a connection header to be present.

        A custom ``http_client`` may omit or strip ``Connection`` before the
        request reaches signing; the previous ``del headers["connection"]`` raised
        ``KeyError`` in that case.
        """
        headers = get_auth_headers(
            method="POST",
            url="https://bedrock-runtime.us-east-1.amazonaws.com/model/m/invoke",
            headers=httpx.Headers({"content-type": "application/json"}),
            aws_access_key=_ACCESS_KEY,
            aws_secret_key=_SECRET_KEY,
            aws_session_token=None,
            region="us-east-1",
            profile=None,
            data='{"hello": "world"}',
        )
        assert "Authorization" in headers
