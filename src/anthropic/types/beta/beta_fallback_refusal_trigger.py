# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaFallbackRefusalTrigger"]


class BetaFallbackRefusalTrigger(BaseModel):
    """The `from` model declined for policy reasons."""

    category: Optional[Literal["cyber", "bio", "frontier_llm", "reasoning_extraction"]] = None
    """The policy category that triggered a refusal."""

    type: Literal["refusal"]
