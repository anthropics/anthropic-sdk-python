from __future__ import annotations

import threading

from anthropic import AccessToken, AnthropicError, TokenCache


def test_invalidate_during_refresh_discards_result_and_preserves_singleflight() -> None:
    first_started = threading.Event()
    release_first = threading.Event()
    forced_started = threading.Event()
    release_forced = threading.Event()
    calls_lock = threading.Lock()
    force_seen: list[bool] = []

    def provider(*, force_refresh: bool = False) -> AccessToken:
        with calls_lock:
            index = len(force_seen)
            force_seen.append(force_refresh)

        if index == 0:
            first_started.set()
            assert release_first.wait(timeout=5)
            return AccessToken("pre-invalidation", expires_at=None)
        if index == 1:
            forced_started.set()
            assert release_forced.wait(timeout=5)
            return AccessToken("post-invalidation", expires_at=None)
        raise AssertionError(f"unexpected provider call {index + 1}")

    cache = TokenCache(provider)
    results: list[str] = []
    errors: list[BaseException] = []

    def get_token() -> None:
        try:
            results.append(cache.get_token())
        except BaseException as exc:  # pragma: no cover - assertion below reports the failure
            errors.append(exc)

    first = threading.Thread(target=get_token, daemon=True)
    second = threading.Thread(target=get_token, daemon=True)
    first.start()
    assert first_started.wait(timeout=5)

    # The second caller must join the same in-flight refresh rather than start a
    # parallel provider call. Invalidate while both callers depend on that
    # refresh, then let its pre-invalidation result return.
    second.start()
    cache.invalidate()
    release_first.set()

    # The stale result must be discarded. Exactly one caller becomes the next
    # single-flight leader and performs a forced refresh; the other waits.
    assert forced_started.wait(timeout=5)

    # Another request may now report a 401 for the same revoked token. That
    # duplicate invalidation is already represented by the pending forced
    # refresh and must not invalidate the replacement refresh itself.
    cache.invalidate()
    release_forced.set()

    first.join(timeout=5)
    second.join(timeout=5)
    assert not first.is_alive()
    assert not second.is_alive()
    assert errors == []
    assert sorted(results) == ["post-invalidation", "post-invalidation"]
    assert force_seen == [False, True]

    # The forced result was published as the cache value; no third provider
    # call is needed.
    assert cache.get_token() == "post-invalidation"
    assert force_seen == [False, True]


def test_invalidate_during_failed_advisory_refresh_does_not_serve_stale_fallback() -> None:
    refresh_started = threading.Event()
    release_refresh = threading.Event()
    calls_lock = threading.Lock()
    force_seen: list[bool] = []

    def provider(*, force_refresh: bool = False) -> AccessToken:
        with calls_lock:
            index = len(force_seen)
            force_seen.append(force_refresh)

        if index == 0:
            # At t=100 this sits in the advisory window: 50s remaining, with
            # mandatory=10 and advisory=100.
            return AccessToken("cached", expires_at=150)
        if index == 1:
            refresh_started.set()
            assert release_refresh.wait(timeout=5)
            raise AnthropicError("refresh failed")
        if index == 2:
            return AccessToken("forced-fresh", expires_at=None)
        raise AssertionError(f"unexpected provider call {index + 1}")

    cache = TokenCache(
        provider,
        advisory_refresh_seconds=100,
        mandatory_refresh_seconds=10,
        time_source=lambda: 100,
    )
    assert cache.get_token() == "cached"

    results: list[str] = []
    errors: list[BaseException] = []

    def advisory_refresh() -> None:
        try:
            results.append(cache.get_token())
        except BaseException as exc:
            errors.append(exc)

    thread = threading.Thread(target=advisory_refresh, daemon=True)
    thread.start()
    assert refresh_started.wait(timeout=5)

    # The cached token is revoked while the advisory refresh is in flight. A
    # subsequent provider failure must not use that revoked token as the normal
    # advisory fallback.
    cache.invalidate()
    release_refresh.set()
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert results == []
    assert len(errors) == 1
    assert isinstance(errors[0], AnthropicError)

    # The invalidation's one-shot force flag survives the failed in-flight
    # refresh and is consumed by the next successful provider call.
    assert cache.get_token() == "forced-fresh"
    assert force_seen == [False, False, True]
