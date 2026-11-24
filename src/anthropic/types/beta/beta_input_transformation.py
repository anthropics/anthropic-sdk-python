from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_thinking_dropped_input_transformation import BetaThinkingDroppedInputTransformation
from .beta_thinking_mismatch_allowed_input_transformation import BetaThinkingMismatchAllowedInputTransformation

__all__ = ["BetaInputTransformation"]

BetaInputTransformation: TypeAlias = Annotated[
    Union[BetaThinkingDroppedInputTransformation, BetaThinkingMismatchAllowedInputTransformation],
    UnionDiscriminator("type"),
]
"""
One entry of `input_transformations`: either a change the API made to the
request's input before showing it to the model, or a block that failed a
binding check and was still shown to the model unchanged. The `type` field
says which.
"""
