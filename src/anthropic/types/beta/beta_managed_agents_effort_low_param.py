# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsEffortLowParam"]


class BetaManagedAgentsEffortLowParam(TypedDict, total=False):
    """Low effort. Favors latency over reasoning depth."""

    type: Required[Literal["low"]]
