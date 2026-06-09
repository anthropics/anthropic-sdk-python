# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..model_param import ModelParam

__all__ = ["BetaFallbackInfoParam"]


class BetaFallbackInfoParam(TypedDict, total=False):
    """Identifies one hop of a fallback transition."""

    model: Required[ModelParam]
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """
