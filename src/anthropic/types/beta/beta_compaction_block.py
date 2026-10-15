from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_response_tool_removal_block import BetaResponseToolRemovalBlock
from .beta_response_tool_addition_block import BetaResponseToolAdditionBlock

__all__ = ["BetaCompactionBlock", "ToolChange"]

ToolChange: TypeAlias = Annotated[
    Union[BetaResponseToolAdditionBlock, BetaResponseToolRemovalBlock], UnionDiscriminator("type")
]


class BetaCompactionBlock(BaseModel):
    """A compaction block returned when autocompact is triggered.

    When content is None, it indicates the compaction failed to produce a valid
    summary (e.g., malformed output from the model). Clients may round-trip
    compaction blocks with null content; the server treats them as no-ops.
    """

    content: Optional[str] = None
    """Summary of compacted content, or null if compaction failed"""

    encrypted_content: Optional[str] = None
    """Opaque metadata from prior compaction, to be round-tripped verbatim"""

    type: Literal["compaction"]

    signature: Optional[str] = None
    """Signature over the summary, to be sent back with the block verbatim"""

    tool_changes: Optional[List[ToolChange]] = None
    """
    The tool changes of the compacted range: the `tool_addition` and `tool_removal`
    blocks that take the request's `tools` to the tool set in effect at the end of
    the range, or `[]` when the range changed no tool. Absent when the server did
    not compute them. Send the block back unchanged.
    """
