from __future__ import annotations

from typing import Any

import botocore.auth
import httpx
import pytest

from anthropic.lib.aws import _auth


class _RefreshableCredentials:
    def __init__(self) -> None:
        self.frozen = object()
        self.freeze_calls = 0

    def get_frozen_credentials(self) -> object:
        self.freeze_calls += 1
        return self.frozen


class _Session:
    def __init__(self, credentials: object) -> None:
        self._credentials = credentials
        self.region_name = "us-east-1"

    def get_credentials(self) -> object:
        return self._credentials


def test_sigv4_signing_uses_one_frozen_credential_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    credentials = _RefreshableCredentials()
    session = _Session(credentials)
    captured: dict[str, Any] = {}

    monkeypatch.setattr(_auth, "_get_session", lambda **_kwargs: session)

    class _Signer:
        def __init__(self, signing_credentials: object, service_name: str, region_name: str) -> None:
            captured["credentials"] = signing_credentials
            captured["service_name"] = service_name
            captured["region_name"] = region_name

        def add_auth(self, request: Any) -> None:
            request.headers["Authorization"] = "signed"

    monkeypatch.setattr(botocore.auth, "SigV4Auth", _Signer)

    headers = _auth.get_auth_headers(
        method="post",
        url="https://example.amazonaws.com/v1/messages",
        headers=httpx.Headers({"content-type": "application/json"}),
        aws_access_key=None,
        aws_secret_key=None,
        aws_session_token=None,
        region="us-east-1",
        profile=None,
        data="{}",
        service_name="bedrock",
    )

    assert credentials.freeze_calls == 1
    assert captured["credentials"] is credentials.frozen
    assert captured["service_name"] == "bedrock"
    assert captured["region_name"] == "us-east-1"
    assert headers["Authorization"] == "signed"
