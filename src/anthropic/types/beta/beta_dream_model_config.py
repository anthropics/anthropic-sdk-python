# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamModelConfig"]


class BetaDreamModelConfig(BaseModel):
    """Model identifier and configuration applied to every pipeline stage.

    Same wire shape as the Agents API ModelConfig.
    """

    id: str
    """Model identifier, e.g. "claude-opus-4-7". 1-256 characters."""

    speed: Optional[Literal["standard", "fast"]] = None
    """Inference speed mode.

    `fast` provides significantly faster output token generation at premium pricing.
    Not all models support `fast`; invalid combinations are rejected at create time.
    """
