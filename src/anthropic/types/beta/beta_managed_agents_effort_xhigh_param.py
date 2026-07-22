# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsEffortXhighParam"]


class BetaManagedAgentsEffortXhighParam(TypedDict, total=False):
    """Extra-high effort. Not all models accept this level."""

    type: Required[Literal["xhigh"]]
