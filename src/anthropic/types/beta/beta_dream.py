from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_dream_error import BetaDreamError
from .beta_dream_input import BetaDreamInput
from .beta_dream_usage import BetaDreamUsage
from .beta_dream_output import BetaDreamOutput
from .beta_dream_status import BetaDreamStatus
from .beta_output_behavior import BetaOutputBehavior
from .beta_dream_model_config import BetaDreamModelConfig

__all__ = ["BetaDream"]


class BetaDream(BaseModel):
    """
    An asynchronous memory-consolidation job that reads a memory store plus a set of session transcripts and writes consolidated memories into an output memory store — a new store by default, or an existing store chosen via output_behavior. The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to generally-available endpoints.
    """

    id: str
    """The unique ID of the dream (`drm_...`)."""

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    ended_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    error: Optional[BetaDreamError] = None
    """Failure detail for a Dream whose `status` is `failed`."""

    inputs: List[BetaDreamInput]
    """The sources that the dream reads, from the request that created it."""

    instructions: Optional[str] = None
    """The guidance given when the dream was created, or `null` if none was given."""

    model: BetaDreamModelConfig
    """Model identifier and configuration applied to every pipeline stage.

    Same wire shape as the Agents API ModelConfig.
    """

    output_behavior: BetaOutputBehavior
    """Which memory store a dream writes its result to.

    Defaults to `create_new` when left out of a create request.
    """

    outputs: List[BetaDreamOutput]
    """
    The memory store that holds the dream's result, as a one-item array, or an empty
    array until the dream records that memory store.

    The array is empty while the dream is `pending` and for a short time after it
    starts `running`. It can stay empty if the dream fails or is canceled before
    then. The memory store holds the complete result only once `status` is
    `completed`.

    See the
    [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#use-the-output)
    for how to review and use the result.
    """

    session_id: Optional[str] = None
    """
    The ID of the session that runs the dream (`sesn_...`), or `null` if that
    session hasn't started.

    Stream that session's events to follow what the dream reads and writes.

    See the
    [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#watch-the-pipeline-run)
    for how to watch a running dream.
    """

    status: BetaDreamStatus
    """Lifecycle status of a Dream."""

    type: Literal["dream"]

    usage: BetaDreamUsage
    """Cumulative token usage for the dream across every pipeline stage."""
