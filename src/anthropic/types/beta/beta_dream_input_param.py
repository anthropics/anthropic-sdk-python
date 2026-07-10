# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_dream_sessions_input_param import BetaDreamSessionsInputParam
from .beta_dream_memory_store_input_param import BetaDreamMemoryStoreInputParam

__all__ = ["BetaDreamInputParam"]

BetaDreamInputParam: TypeAlias = Union[BetaDreamMemoryStoreInputParam, BetaDreamSessionsInputParam]
