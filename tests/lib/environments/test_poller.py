from __future__ import annotations

import pytest

from anthropic.lib._retry import is_fatal_status_error
from anthropic.lib.environments._poller import _jitter, _backoff

from .test_poller_method import _api_status_error


@pytest.mark.parametrize(
    ("description", "attempt", "want"),
    [
        ("first failure backs off two seconds", 1, 2.0),
        ("second failure doubles to four seconds", 2, 4.0),
        ("very large attempt is capped at sixty seconds", 100, 60.0),
    ],
)
def test_backoff(description: str, attempt: int, want: float) -> None:
    assert _backoff(attempt) == want, description


def test_jitter_within_bounds() -> None:
    for _ in range(100):
        v = _jitter(1.0, 3.0)
        assert 1.0 <= v < 3.0


@pytest.mark.parametrize(
    ("status", "fatal"),
    [
        (400, True),
        (401, True),
        (403, True),
        (404, True),
        (408, False),
        (409, False),
        (412, True),
        (422, True),
        (429, False),
        (500, False),
    ],
)
def test_is_fatal_status_error(status: int, fatal: bool) -> None:
    assert is_fatal_status_error(_api_status_error(status)) is fatal


def test_is_fatal_status_error_ignores_non_api_errors() -> None:
    assert is_fatal_status_error(KeyError("bug")) is False
