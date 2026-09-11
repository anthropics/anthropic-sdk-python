from typing import List
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamSessionsInput"]


class BetaDreamSessionsInput(BaseModel):
    """Input session transcripts the dream reads."""

    session_ids: List[str]

    type: Literal["sessions"]
