from __future__ import annotations

import httpx
import pytest

from anthropic.lib._retry import is_fatal_status_error
from anthropic._exceptions import APIError, APIStatusError, APIConnectionError


def _status_error(status_code: int, headers: dict[str, str] | None = None) -> APIStatusError:
    response = httpx.Response(
        status_code,
        headers=headers or {},
        request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"),
    )
    return APIStatusError("boom", response=response, body=None)


class TestIsFatalStatusError:
    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 422])
    def test_plain_4xx_is_fatal(self, status_code: int) -> None:
        assert is_fatal_status_error(_status_error(status_code)) is True

    @pytest.mark.parametrize("status_code", [408, 409, 429])
    def test_transient_4xx_is_not_fatal(self, status_code: int) -> None:
        assert is_fatal_status_error(_status_error(status_code)) is False

    @pytest.mark.parametrize("status_code", [500, 502, 503])
    def test_5xx_is_not_fatal(self, status_code: int) -> None:
        assert is_fatal_status_error(_status_error(status_code)) is False

    def test_x_should_retry_true_overrides_fatal_4xx(self) -> None:
        # the server explicitly asks to retry a status that would otherwise be fatal
        assert is_fatal_status_error(_status_error(400, {"x-should-retry": "true"})) is False

    def test_x_should_retry_false_overrides_transient_4xx(self) -> None:
        # the server explicitly asks NOT to retry a status that would otherwise be transient
        assert is_fatal_status_error(_status_error(429, {"x-should-retry": "false"})) is True

    def test_x_should_retry_false_makes_5xx_fatal(self) -> None:
        assert is_fatal_status_error(_status_error(503, {"x-should-retry": "false"})) is True

    def test_non_status_errors_are_not_fatal(self) -> None:
        # transport-level errors are retryable, not fatal
        request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        assert is_fatal_status_error(APIConnectionError(request=request)) is False
        assert is_fatal_status_error(APIError("x", request=request, body=None)) is False
        assert is_fatal_status_error(ValueError("not an api error")) is False
