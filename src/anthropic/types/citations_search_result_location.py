# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CitationsSearchResultLocation"]


class CitationsSearchResultLocation(BaseModel):
    cited_text: str
    """The full text of the cited block range, concatenated.

    Always equals the contents of `content[start_block_index:end_block_index]`
    joined together. The text block is the minimal citable unit; this field is never
    a substring of a single block. Not counted toward output tokens, and not counted
    toward input tokens when sent back in subsequent turns.
    """

    end_block_index: int
    """
    Exclusive 0-based end index of the cited block range in the source's `content`
    array.

    Always greater than `start_block_index`; a single-block citation has
    `end_block_index = start_block_index + 1`.
    """

    search_result_index: int
    """
    0-based index of the cited search result among all `search_result` content
    blocks in the request, in the order they appear across messages and tool
    results.

    Counted separately from `document_index`; server-side web search results are not
    included in this count.
    """

    source: str

    start_block_index: int
    """0-based index of the first cited block in the source's `content` array."""

    title: Optional[str] = None

    type: Literal["search_result_location"]
