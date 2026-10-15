from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_browser_toolset_configs_param import BetaBrowserToolsetConfigsParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaBrowserToolset20260801Param"]


class BetaBrowserToolset20260801Param(TypedDict, total=False):
    """
    The browser toolset: a single ``tools[]`` entry (carrying no
    ``name``) that declares the browser tool family. The model is served
    the family's tool with any members disabled via ``configs`` removed
    from its schema.
    """

    type: Required[Literal["browser_toolset_20260801"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    configs: Optional[BetaBrowserToolsetConfigsParam]
    """Sparse per-member overrides, keyed by member name.

    Absent, null, and {} are equivalent; a member's defaults apply wherever its key
    is absent.
    """
