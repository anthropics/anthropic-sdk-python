# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaCitationContentBlockLocation"]


class BetaCitationContentBlockLocation(BaseModel):
    cited_text: str
    """The full text of the cited block range, concatenated.

    Always equals the contents of `content[start_block_index:end_block_index]`
    joined together. The text block is the minimal citable unit; this field is never
    a substring of a single block. Not counted toward output tokens, and not counted
    toward input tokens when sent back in subsequent turns.
    """

    document_index: int

    document_title: Optional[str] = None

    end_block_index: int
    """
    Exclusive 0-based end index of the cited block range in the source's `content`
    array.

    Always greater than `start_block_index`; a single-block citation has
    `end_block_index = start_block_index + 1`.
    """

    file_id: Optional[str] = None

    start_block_index: int
    """0-based index of the first cited block in the source's `content` array."""

    type: Literal["content_block_location"]
