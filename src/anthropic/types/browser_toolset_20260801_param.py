# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

from .browser_toolset_configs_param import BrowserToolsetConfigsParam
from .cache_control_ephemeral_param import CacheControlEphemeralParam

__all__ = ["BrowserToolset20260801Param"]


class BrowserToolset20260801Param(TypedDict, total=False):
    """
    The browser toolset: a single ``tools[]`` entry (carrying no
    ``name``) that declares the browser tool family. The model is served
    the family's tool with any members disabled via ``configs`` removed
    from its schema.
    """

    type: Required[Literal["browser_toolset_20260801"]]

    allowed_callers: List[
        Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]
    ]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    configs: Optional[BrowserToolsetConfigsParam]
    """
    Per-member configuration for `browser_toolset_20260801`: one optional field per
    member tool, keyed by the member name — the same name the member's `tool_use`
    blocks carry. Every member is an accepted key, and a member's defaults apply
    wherever its key is absent. Unknown keys are rejected: the field set is this
    toolset version's complete member set.
    """
