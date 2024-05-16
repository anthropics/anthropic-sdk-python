# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated

from ...._utils import PropertyInfo
from ...._models import BaseModel
from ...text_delta import TextDelta
from .input_json_delta import InputJsonDelta

__all__ = ["ToolsBetaContentBlockDeltaEvent", "Delta"]

Delta = Annotated[Union[TextDelta, InputJsonDelta], PropertyInfo(discriminator="type")]


class ToolsBetaContentBlockDeltaEvent(BaseModel):
    delta: Delta

    index: int

    type: Literal["content_block_delta"]
