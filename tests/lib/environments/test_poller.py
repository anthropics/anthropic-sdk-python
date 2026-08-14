from __future__ import annotations

import pytest

from anthropic.lib.environments._poller import _jitter, _backoff


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
