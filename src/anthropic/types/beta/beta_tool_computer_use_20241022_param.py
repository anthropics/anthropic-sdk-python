# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam

__all__ = ["BetaToolComputerUse20241022Param"]


class BetaToolComputerUse20241022Param(TypedDict, total=False):
    display_height_px: Required[int]

    display_width_px: Required[int]

    name: Required[Literal["computer"]]

    type: Required[Literal["computer_20241022"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]

    display_number: Optional[int]
