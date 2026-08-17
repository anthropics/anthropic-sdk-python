from anthropic.lib._retry import backoff


def test_backoff_preserves_normal_exponential_values() -> None:
    assert backoff(1, cap=60.0) == 2.0
    assert backoff(4, cap=60.0) == 16.0
    assert backoff(6, cap=60.0) == 60.0


def test_backoff_large_attempt_stays_at_cap_instead_of_overflowing() -> None:
    assert backoff(10_000, cap=60.0) == 60.0


def test_backoff_overflow_respects_custom_cap() -> None:
    assert backoff(10_000, cap=3.5) == 3.5
