# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaDreamModelConfigParam"]


class BetaDreamModelConfigParam(TypedDict, total=False):
    """Model identifier and configuration applied to every pipeline stage."""

    id: Required[str]
    """Model identifier, e.g. "claude-opus-4-7". 1-256 characters."""

    speed: Optional[Literal["standard", "fast"]]
    """Inference speed mode.

    `fast` provides significantly faster output token generation at premium pricing.
    Not all models support `fast`; invalid combinations are rejected at create time.
    """
