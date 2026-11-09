from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["InstallationSettingSetParams"]


class InstallationSettingSetParams(TypedDict, total=False):
    plugin_id: Required[str]
    """ID of the Plugin (prefixed `plugin_`)."""

    installation_preference: Required[Literal["auto_install", "available", "not_available", "required"]]
    """
    The installation setting the target is to hold for this Plugin: one of
    `required`, `auto_install`, `available`, `not_available`.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
