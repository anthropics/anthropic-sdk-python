# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel
from .text_block import TextBlock
from .content_block import ContentBlock as ContentBlock

__all__ = ["ContentBlockStartEvent"]


class ContentBlockStartEvent(BaseModel):
    content_block: TextBlock

    index: int

    type: Literal["content_block_start"]
