# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel
from .content_block import ContentBlock

__all__ = ["ContentBlockStartEvent"]


class ContentBlockStartEvent(BaseModel):
    content_block: ContentBlock

    index: int

    type: Literal["content_block_start"]
