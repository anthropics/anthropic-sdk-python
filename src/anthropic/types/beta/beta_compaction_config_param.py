from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaCompactionConfigParam"]


class BetaCompactionConfigParam(TypedDict, total=False):
    """
    Compact the whole conversation and return a signed `compaction` block,
    alone, that a later request sends back first in `messages`, in place of
    the messages it summarizes. There is no trigger and no pause flag: sending
    the parameter compacts, and nothing is sampled after the block.

    The summarization prompt is the server's own unless `instructions` are
    given, which then replace it for this request; a value that is empty or
    only whitespace counts as absent.
    """

    type: Required[Literal["summarize"]]

    instructions: Optional[str]
    """Replaces the server's default summarization prompt for this request.

    An empty or whitespace-only value counts as absent.
    """
