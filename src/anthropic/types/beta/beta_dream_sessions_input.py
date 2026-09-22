from typing import List
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamSessionsInput"]


class BetaDreamSessionsInput(BaseModel):
    """The sessions that a dream reads, given as an entry in `inputs`."""

    session_ids: List[str]
    """The IDs of the sessions whose transcripts the dream reads (`sesn_...`).

    Give 1 to 100 IDs, with no duplicates. Each session must be in the same
    workspace as the dream. Responses list the IDs in sorted order.

    The
    [limits table in the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#limits)
    lists all the limits on a dream.
    """

    type: Literal["sessions"]
