from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["JWKSInlineParam"]


class JWKSInlineParam(TypedDict, total=False):
    """JWKS supplied directly; no network fetch."""

    keys: Required[Iterable[Dict[str, object]]]
    """Inline JWK objects."""

    type: Required[Literal["inline"]]
