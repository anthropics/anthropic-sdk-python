# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_text_delta import BetaTextDelta
from .beta_input_json_delta import BetaInputJSONDelta

__all__ = ["BetaRawContentBlockDeltaEvent", "Delta"]

Delta: TypeAlias = Annotated[Union[BetaTextDelta, BetaInputJSONDelta], PropertyInfo(discriminator="type")]


class BetaRawContentBlockDeltaEvent(BaseModel):
    delta: Delta

    index: int

    type: Literal["content_block_delta"]
