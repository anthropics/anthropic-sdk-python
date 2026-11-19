from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ......_types import SequenceNotStr
from .....anthropic_beta_param import AnthropicBetaParam
from .beta_claude_code_managed_settings_mode_param import BetaClaudeCodeManagedSettingsModeParam

__all__ = ["ConfigurationUpdateParams"]


class ConfigurationUpdateParams(TypedDict, total=False):
    mode: BetaClaudeCodeManagedSettingsModeParam
    """The new mode, as an object such as `{"type": "rbac_groups"}`."""

    rbac_group_order: SequenceNotStr[str]
    """
    Every RBAC Group that has settings, each listed once, in the new order, highest
    precedence first. Requires `rbac_group_order_version`.
    """

    rbac_group_order_version: str
    """The `rbac_group_order_version` from the read this change is based on.

    Requires `rbac_group_order`.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `ce-claude-code-managed-settings-2026-10-06` in this header.
    """
