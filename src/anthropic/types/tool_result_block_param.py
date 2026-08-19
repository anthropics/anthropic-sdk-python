# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .text_block_param import TextBlockParam
from .image_block_param import ImageBlockParam
from .document_block_param import DocumentBlockParam
from .browser_state_block_param import BrowserStateBlockParam
from .search_result_block_param import SearchResultBlockParam
from .tool_reference_block_param import ToolReferenceBlockParam
from .cache_control_ephemeral_param import CacheControlEphemeralParam

__all__ = ["ToolResultBlockParam", "Content"]

Content: TypeAlias = Union[
    TextBlockParam,
    ImageBlockParam,
    SearchResultBlockParam,
    DocumentBlockParam,
    ToolReferenceBlockParam,
    BrowserStateBlockParam,
]


class ToolResultBlockParam(TypedDict, total=False):
    tool_use_id: Required[str]

    type: Required[Literal["tool_result"]]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    content: Union[str, Iterable[Content]]

    is_error: bool

    toolset_name: Optional[str]
    """For a toolset member tool_result, the toolset family of the paired tool_use."""
