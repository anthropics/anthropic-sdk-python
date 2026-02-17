# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .tool_param import ToolParam
from .citations_config_param import CitationsConfigParam
from .tool_bash_20250124_param import ToolBash20250124Param
from .memory_tool_20250818_param import MemoryTool20250818Param
from .cache_control_ephemeral_param import CacheControlEphemeralParam
from .web_fetch_tool_20250910_param import WebFetchTool20250910Param
from .web_search_tool_20250305_param import WebSearchTool20250305Param
from .tool_text_editor_20250124_param import ToolTextEditor20250124Param
from .tool_text_editor_20250429_param import ToolTextEditor20250429Param
from .tool_text_editor_20250728_param import ToolTextEditor20250728Param
from .code_execution_tool_20250522_param import CodeExecutionTool20250522Param
from .code_execution_tool_20250825_param import CodeExecutionTool20250825Param
from .tool_search_tool_bm25_20251119_param import ToolSearchToolBm25_20251119Param
from .tool_search_tool_regex_20251119_param import ToolSearchToolRegex20251119Param

__all__ = [
    "ToolUnionParam",
    "CodeExecutionTool20260120",
    "WebSearchTool20260209",
    "WebSearchTool20260209UserLocation",
    "WebFetchTool20260209",
]


class CodeExecutionTool20260120(TypedDict, total=False):
    """
    Code execution tool with REPL state persistence (daemon mode + gVisor checkpoint).
    """

    name: Required[Literal["code_execution"]]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Required[Literal["code_execution_20260120"]]

    allowed_callers: List[Literal["direct", "code_execution_20250825"]]

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    defer_loading: bool
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    strict: bool
    """When true, guarantees schema validation on tool names and inputs"""


class WebSearchTool20260209UserLocation(TypedDict, total=False):
    """Parameters for the user's location.

    Used to provide more relevant search results.
    """

    type: Required[Literal["approximate"]]

    city: Optional[str]
    """The city of the user."""

    country: Optional[str]
    """
    The two letter
    [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the
    user.
    """

    region: Optional[str]
    """The region of the user."""

    timezone: Optional[str]
    """The [IANA timezone](https://nodatime.org/TimeZones) of the user."""


class WebSearchTool20260209(TypedDict, total=False):
    name: Required[Literal["web_search"]]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Required[Literal["web_search_20260209"]]

    allowed_callers: List[Literal["direct", "code_execution_20250825"]]

    allowed_domains: Optional[SequenceNotStr[str]]
    """If provided, only these domains will be included in results.

    Cannot be used alongside `blocked_domains`.
    """

    blocked_domains: Optional[SequenceNotStr[str]]
    """If provided, these domains will never appear in results.

    Cannot be used alongside `allowed_domains`.
    """

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    defer_loading: bool
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    max_uses: Optional[int]
    """Maximum number of times the tool can be used in the API request."""

    strict: bool
    """When true, guarantees schema validation on tool names and inputs"""

    user_location: Optional[WebSearchTool20260209UserLocation]
    """Parameters for the user's location.

    Used to provide more relevant search results.
    """


class WebFetchTool20260209(TypedDict, total=False):
    name: Required[Literal["web_fetch"]]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Required[Literal["web_fetch_20260209"]]

    allowed_callers: List[Literal["direct", "code_execution_20250825"]]

    allowed_domains: Optional[SequenceNotStr[str]]
    """List of domains to allow fetching from"""

    blocked_domains: Optional[SequenceNotStr[str]]
    """List of domains to block fetching from"""

    cache_control: Optional[CacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    citations: Optional[CitationsConfigParam]
    """Citations configuration for fetched documents.

    Citations are disabled by default.
    """

    defer_loading: bool
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    max_content_tokens: Optional[int]
    """Maximum number of tokens used by including web page text content in the context.

    The limit is approximate and does not apply to binary content such as PDFs.
    """

    max_uses: Optional[int]
    """Maximum number of times the tool can be used in the API request."""

    strict: bool
    """When true, guarantees schema validation on tool names and inputs"""


ToolUnionParam: TypeAlias = Union[
    ToolParam,
    ToolBash20250124Param,
    CodeExecutionTool20250522Param,
    CodeExecutionTool20250825Param,
    CodeExecutionTool20260120,
    MemoryTool20250818Param,
    ToolTextEditor20250124Param,
    ToolTextEditor20250429Param,
    ToolTextEditor20250728Param,
    WebSearchTool20250305Param,
    WebFetchTool20250910Param,
    WebSearchTool20260209,
    WebFetchTool20260209,
    ToolSearchToolBm25_20251119Param,
    ToolSearchToolRegex20251119Param,
]
