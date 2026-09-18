from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaDreamModelConfigParam"]


class BetaDreamModelConfigParam(TypedDict, total=False):
    """The object form of `model` in a request to create a dream."""

    id: Required[str]
    """The ID of the model to run the dream with.

    The ID can be 1 to 256 characters long.

    The
    [limits table in the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#limits)
    lists the supported models.
    """

    speed: Optional[Literal["standard", "fast"]]
    """Inference speed mode.

    `fast` provides significantly faster output token generation at premium pricing.
    Not all models support `fast`; invalid combinations are rejected at create time.
    """
