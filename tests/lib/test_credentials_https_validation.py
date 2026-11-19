from __future__ import annotations

import pytest

from anthropic import AnthropicError
from anthropic.lib.credentials._constants import _require_https


@pytest.mark.parametrize(
    "url",
    [
        "https://api.anthropic.com",
        "HTTPS://example.com/custom",
        "http://localhost:8080",
        "http://localhost.:8080",
        "http://127.0.0.1:8080",
        "http://[::1]:8080",
    ],
)
def test_require_https_allows_https_and_actual_loopback_hosts(url: str) -> None:
    _require_https(url, field="base_url")


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost.evil.example",
        "http://localhost-example.com",
        "http://127.0.0.1.evil.example",
        "http://localhost@evil.example",
        "http://192.168.1.10",
        "http://example.com",
    ],
)
def test_require_https_rejects_cleartext_lookalike_and_non_loopback_hosts(url: str) -> None:
    with pytest.raises(AnthropicError, match="must use https"):
        _require_https(url, field="base_url")
