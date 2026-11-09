from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from .beta_request_tool_removal_block_param import BetaRequestToolRemovalBlockParam
from .beta_request_tool_addition_block_param import BetaRequestToolAdditionBlockParam

__all__ = ["BetaCompactionBlockParam", "ToolChange"]

ToolChange: TypeAlias = Union[BetaRequestToolAdditionBlockParam, BetaRequestToolRemovalBlockParam]


class BetaCompactionBlockParam(TypedDict, total=False):
    """A compaction block containing summary of previous context.

    Users should round-trip these blocks from responses to subsequent requests
    to maintain context across compaction boundaries.

    When content is None, the block represents a failed compaction. The server
    treats these as no-ops. Empty string content is not allowed.
    """

    type: Required[Literal["compaction"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    content: Optional[str]
    """Summary of previously compacted content, or null if compaction failed"""

    encrypted_content: Optional[str]
    """Opaque metadata from prior compaction, to be round-tripped verbatim"""

    signature: Optional[str]
    """The block's signature as returned, to be sent back verbatim"""

    tool_changes: Optional[Iterable[ToolChange]]
    """
    The tool changes of the compacted range, as the server returned them on this
    block: the `tool_addition` and `tool_removal` entries that take the request's
    `tools` to the tool set in effect at the end of the range. Send them back
    unchanged with the block.
    """
