from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["BetaDreamSessionsInputParam"]


class BetaDreamSessionsInputParam(TypedDict, total=False):
    """The sessions that a dream reads, given as an entry in `inputs`."""

    session_ids: Required[SequenceNotStr[str]]
    """The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

    Give 1 to 100 IDs, with no duplicates. Each session must be in the same
    workspace as the dream. Responses list the IDs in sorted order.

    The
    [limits table in the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#limits)
    lists all the limits on a dream.
    """

    type: Required[Literal["sessions"]]
