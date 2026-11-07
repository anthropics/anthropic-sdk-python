from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TextDelta"]


class TextDelta(BaseModel):
    text: str

    type: Literal["text_delta"]
