# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

from .beta_clear_tool_uses_20250919_edit_param import BetaClearToolUses20250919EditParam

__all__ = ["BetaContextManagementConfigParam"]


class BetaContextManagementConfigParam(TypedDict, total=False):
    edits: Iterable[BetaClearToolUses20250919EditParam]
    """List of context management edits to apply"""
