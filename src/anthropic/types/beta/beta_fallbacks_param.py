from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, TypeAlias

from .beta_fallback_param import BetaFallbackParam

__all__ = ["BetaFallbacksParam"]

BetaFallbacksParam: TypeAlias = Union[Iterable[BetaFallbackParam], Literal["default"]]
