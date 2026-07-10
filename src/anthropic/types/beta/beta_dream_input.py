# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_dream_sessions_input import BetaDreamSessionsInput
from .beta_dream_memory_store_input import BetaDreamMemoryStoreInput

__all__ = ["BetaDreamInput"]

BetaDreamInput: TypeAlias = Annotated[
    Union[BetaDreamMemoryStoreInput, BetaDreamSessionsInput], PropertyInfo(discriminator="type")
]
