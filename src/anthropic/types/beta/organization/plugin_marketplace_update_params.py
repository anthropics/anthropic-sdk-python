from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginMarketplaceUpdateParams"]


class PluginMarketplaceUpdateParams(TypedDict, total=False):
    default_installation_preference: Required[Literal["auto_install", "available", "not_available", "required"]]
    """
    The organization-wide installation setting every Plugin in the marketplace
    without one of its own gets: one of `required`, `auto_install`, `available`,
    `not_available`. Once set it can be changed but not removed.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
