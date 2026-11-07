from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_thread_create_params import BetaThreadCreateParams
from .beta_thread_continue_params import BetaThreadContinueParams

__all__ = ["BetaMessageThreadParam"]

BetaMessageThreadParam: TypeAlias = Union[BetaThreadCreateParams, BetaThreadContinueParams]
