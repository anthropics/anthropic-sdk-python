# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_dream_error import BetaDreamError
from .beta_dream_input import BetaDreamInput
from .beta_dream_usage import BetaDreamUsage
from .beta_dream_output import BetaDreamOutput
from .beta_dream_status import BetaDreamStatus
from .beta_dream_model_config import BetaDreamModelConfig

__all__ = ["BetaDream"]


class BetaDream(BaseModel):
    """
    An asynchronous memory-consolidation job that reads a memory store plus a set of session transcripts and writes consolidated memories into a new output memory store. The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to generally-available endpoints.
    """

    id: str

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    ended_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    error: Optional[BetaDreamError] = None
    """Failure detail for a Dream whose `status` is `failed`."""

    inputs: List[BetaDreamInput]

    instructions: Optional[str] = None

    model: BetaDreamModelConfig
    """Model identifier and configuration applied to every pipeline stage.

    Same wire shape as the Agents API ModelConfig.
    """

    outputs: List[BetaDreamOutput]

    session_id: Optional[str] = None

    status: BetaDreamStatus
    """Lifecycle status of a Dream."""

    type: Literal["dream"]

    usage: BetaDreamUsage
    """Cumulative token usage for the dream across every pipeline stage."""
