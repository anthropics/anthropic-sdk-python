# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaJWKSInlineParam"]


class BetaJWKSInlineParam(TypedDict, total=False):
    """JWKS supplied directly; no network fetch."""

    keys: Required[Iterable[Dict[str, object]]]
    """Inline JWK objects."""

    type: Required[Literal["inline"]]
