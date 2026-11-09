from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .cache_control_ephemeral_param import CacheControlEphemeralParam
from .computer_toolset_configs_param import ComputerToolsetConfigsParam

__all__ = ["ComputerToolset20260801Param"]


class ComputerToolset20260801Param(TypedDict, total=False):
    """
    The computer toolset: a single ``tools[]`` entry (carrying no
    ``name``) that declares the computer tool family. The model is
    served the family's tool with any members disabled via ``configs``
    removed from its schema. Every member is enabled by default, zoom
    included. The single-tool options ``display_number`` and
    ``enable_zoom`` are not fields of a toolset entry — it carries only
    ``type``, ``configs``, and ``cache_control``; zoom is controlled
    via ``configs.zoom.enabled``.
    """

    type: Required[Literal["computer_toolset_20260801"]]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    configs: Optional[ComputerToolsetConfigsParam]
    """Sparse per-member overrides, keyed by member name.

    Absent, null, and {} are equivalent; a member's defaults apply wherever its key
    is absent.
    """
