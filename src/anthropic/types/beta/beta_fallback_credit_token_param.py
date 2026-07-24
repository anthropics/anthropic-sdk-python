# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaFallbackCreditTokenParam"]


class BetaFallbackCreditTokenParam(TypedDict, total=False):
    """Object form of ``fallback_credit_token``: the token plus a redemption
    mode.

    Requires ``anthropic-beta: fallback-credit-2026-07-01``; without that
    header the field accepts the bare string only. The bare string and the
    mode-less object are equivalent (both select ``strict``), so wrapping
    an existing token changes nothing by itself.
    """

    token: Required[str]
    """
    The opaque `fallback_credit_token` from a prior refusal's `stop_details` — the
    same string the bare-string form carries.
    """

    mode: Literal["strict", "best_effort"]
    """How a failing token affects the retry.

    `strict` (the default, and the bare-string behavior): a failing redemption is a
    400 and the retry is not served. `best_effort`: the retry is served either way —
    a token-layer failure no longer rejects the request; the retry proceeds at
    normal price and the outcome is reported on the response's
    `usage.fallback_credit`. Two failures stay hard in both modes: a malformed
    token, and combining `fallback_credit_token` with `fallbacks`.
    """
