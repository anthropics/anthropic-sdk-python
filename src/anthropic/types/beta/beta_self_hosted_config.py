# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaSelfHostedConfig"]


class BetaSelfHostedConfig(BaseModel):
    """Configuration for self-hosted environments."""

    type: Literal["self_hosted"]
    """Environment type"""
