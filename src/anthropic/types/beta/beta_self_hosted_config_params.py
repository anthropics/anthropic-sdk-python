# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaSelfHostedConfigParams"]


class BetaSelfHostedConfigParams(TypedDict, total=False):
    """Request params for `self_hosted` environment configuration."""

    type: Required[Literal["self_hosted"]]
    """Environment type"""
