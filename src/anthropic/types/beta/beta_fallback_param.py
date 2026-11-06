from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..model_param import ModelParam
from .beta_output_config_param import BetaOutputConfigParam
from .beta_thinking_config_enabled_param import BetaThinkingConfigEnabledParam
from .beta_thinking_config_adaptive_param import BetaThinkingConfigAdaptiveParam
from .beta_thinking_config_disabled_param import BetaThinkingConfigDisabledParam
from .beta_thinking_config_between_tools_param import BetaThinkingConfigBetweenToolsParam

__all__ = ["BetaFallbackParam", "Thinking"]

Thinking: TypeAlias = Union[
    BetaThinkingConfigEnabledParam,
    BetaThinkingConfigDisabledParam,
    BetaThinkingConfigBetweenToolsParam,
    BetaThinkingConfigAdaptiveParam,
]


class BetaFallbackParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """One entry in the `fallbacks` chain on a `/v1/messages` request.

    `model` is required. The override fields (`max_tokens`, `thinking`,
    `output_config`, and `speed`) set the corresponding parameter for this
    attempt only and are validated as if the request were made to `model`.
    Any other key is rejected at parse time.
    """

    model: Required[ModelParam]
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    max_tokens: Optional[int]
    """
    The `max_tokens` for the fallback attempt that uses this `fallbacks` entry's
    `model`, in place of the request's `max_tokens`. If you leave it out or set it
    to `null`, the attempt uses the request's `max_tokens`.

    See the
    [refusals and fallback guide](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#naming-your-own-fallback-models)
    to learn more about fallback entries.
    """

    output_config: Optional[BetaOutputConfigParam]
    """
    Output parameters for the fallback attempt that uses this `fallbacks` entry's
    `model`, combined with the request's `output_config` one field at a time.

    - `format`: If you leave it out, the attempt uses the request's `format`. If you
      set it to `null`, the attempt runs without a format.
    - `effort`: If you leave it out, the attempt uses the request's `effort` when
      `model` supports that level with the attempt's `thinking`. If the request
      doesn't set `effort`, if `model` doesn't support the level, or if you set
      `effort` to `null`, the attempt runs at the default effort of `model`.
    - `task_budget`: If you leave it out, the attempt uses the request's
      `task_budget` when `model` accepts a task budget of that size. If the request
      doesn't set `task_budget`, if `model` doesn't accept it, or if you set
      `task_budget` to `null`, the attempt runs without a task budget.

    Set `output_config` to `null` to run the attempt without a format or a task
    budget, at the default effort of `model`.

    These rules apply with the `server-side-fallback-2026-07-01` beta header.
    """

    speed: Optional[Literal["standard", "fast"]]
    """
    The inference speed mode for the fallback attempt that uses this `fallbacks`
    entry's `model`. If you leave it out, the attempt runs at `fast` speed only when
    the request sets `speed` to `fast` and your organization can use fast mode on
    `model`.

    Otherwise, or when you set this field to `null`, the attempt runs at `standard`
    speed.

    These rules apply with the `server-side-fallback-2026-07-01` beta header.
    """

    thinking: Optional[Thinking]
    """
    The thinking configuration for the fallback attempt that uses this `fallbacks`
    entry's `model`. If you leave it out, the attempt uses the request's `thinking`
    when `model` supports that thinking `type`.

    If you leave it out and the request's thinking `type` is `between_tools` but
    `model` doesn't support `between_tools`, the attempt uses `disabled` if `model`
    supports it. Otherwise, if `model` doesn't support the request's thinking
    `type`, if the request doesn't set `thinking`, or if you set this field to
    `null`, the attempt uses the thinking `type` that `model` uses when a request
    leaves out `thinking`. The request's `thinking.display` still applies where
    `model` allows it.

    These rules apply with the `server-side-fallback-2026-07-01` beta header.
    """
