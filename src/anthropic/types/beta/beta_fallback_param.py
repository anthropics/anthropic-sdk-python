# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..model_param import ModelParam
from .beta_output_config_param import BetaOutputConfigParam
from .beta_thinking_config_enabled_param import BetaThinkingConfigEnabledParam
from .beta_thinking_config_adaptive_param import BetaThinkingConfigAdaptiveParam
from .beta_thinking_config_disabled_param import BetaThinkingConfigDisabledParam

__all__ = ["BetaFallbackParam", "Thinking"]

Thinking: TypeAlias = Union[
    BetaThinkingConfigEnabledParam, BetaThinkingConfigDisabledParam, BetaThinkingConfigAdaptiveParam
]


class BetaFallbackParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """One entry in the `fallbacks` chain on a `/v1/messages` request.

    `model` is required. The four override fields (`max_tokens`, `thinking`,
    `output_config`, and `speed`) replace the corresponding top-level field
    for this attempt only and are validated as if the request were made to
    `model`. Any other key is rejected at parse time.
    """

    model: Required[ModelParam]
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    max_tokens: Optional[int]

    output_config: Optional[BetaOutputConfigParam]

    speed: Optional[Literal["standard", "fast"]]

    thinking: Optional[Thinking]
