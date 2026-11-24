from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, TypeAlias

from .beta_fallback_param import BetaFallbackParam

__all__ = ["BetaFallbacksParam"]

BetaFallbacksParam: TypeAlias = Union[Iterable[BetaFallbackParam], Literal["default"]]
"""
Opt-in server-side retry on one or more substitute models when the requested model declines for policy reasons. Tried in order: if the first entry also declines, the second is tried, and so on. Some models don't support fallbacks; on those models, a list of fallback models returns a 400 error. See [Server-side fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback). The string "default" requests the requested model's server-defined default fallback configuration. On a model that doesn't support fallbacks, the request runs on the requested model alone, so a declined request stays declined.
"""
