from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaInputTokensTriggerParam"]


class BetaInputTokensTriggerParam(TypedDict, total=False):
    type: Required[Literal["input_tokens"]]

    value: Required[int]
