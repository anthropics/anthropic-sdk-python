# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaCacheMissSystemChanged"]


class BetaCacheMissSystemChanged(BaseModel):
    cache_missed_input_tokens: int
    """
    Approximate number of input tokens that would have been read from cache had the
    prefix matched the previous request.
    """

    type: Literal["system_changed"]
