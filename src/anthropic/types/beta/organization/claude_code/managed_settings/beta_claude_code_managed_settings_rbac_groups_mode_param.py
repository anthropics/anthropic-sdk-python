from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeCodeManagedSettingsRBACGroupsModeParam"]


class BetaClaudeCodeManagedSettingsRBACGroupsModeParam(TypedDict, total=False):
    type: Required[Literal["rbac_groups"]]
