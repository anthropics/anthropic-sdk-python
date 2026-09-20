from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_web_fetch_url_sources import BetaWebFetchURLSources
from .beta_citations_config_param import BetaCitationsConfigParam
from .beta_cache_control_ephemeral import BetaCacheControlEphemeral

__all__ = ["BetaWebFetchTool20260209"]


class BetaWebFetchTool20260209(BaseModel):
    name: Literal["web_fetch"]
    """Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.
    """

    type: Literal["web_fetch_20260209"]

    allowed_callers: Optional[
        List[Literal["direct", "code_execution_20250825", "code_execution_20260120", "code_execution_20260521"]]
    ] = None

    allowed_domains: Optional[List[str]] = None
    """List of domains to allow fetching from"""

    blocked_domains: Optional[List[str]] = None
    """List of domains to block fetching from"""

    cache_control: Optional[BetaCacheControlEphemeral] = None
    """Create a cache control breakpoint at this content block."""

    citations: Optional[BetaCitationsConfigParam] = None
    """Citations configuration for fetched documents.

    Citations are disabled by default.
    """

    defer_loading: Optional[bool] = None
    """If true, tool will not be included in initial system prompt.

    Only loaded when returned via tool_reference from tool search.
    """

    max_content_tokens: Optional[int] = None
    """Maximum number of tokens used by including web page text content in the context.

    The limit is approximate and does not apply to binary content such as PDFs.
    """

    max_uses: Optional[int] = None
    """Maximum number of times the tool can be used in the API request."""

    strict: Optional[bool] = None
    """When true, guarantees schema validation on tool names and inputs"""

    url_sources: Optional[BetaWebFetchURLSources] = None
    """Which sources contribute to the set of URLs web fetch may fetch.

    Each key is a tagged variant: `user_input` is `all` or `none`; the two tool
    filters are `all`, `none`, `only` (only the named tools' results) or `except`
    (every result but the named tools'). A named tool must be declared in this
    request's `tools[]`.
    """
