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
    An asynchronous job that reads a memory store and past sessions, then writes a reorganized version of that memory store.

    By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead. The Dreams API is in research preview, so this resource can still change.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#how-it-works) for what a dream reads and produces.
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
    """The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the
    model as an object, even if the request gave only a model ID.
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
    """Where a dream is in its lifecycle.

    `completed`, `failed`, and `canceled` are final: once a dream has one of these
    statuses, its status doesn't change again.

    See the
    [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#lifecycle)
    for what each status means.
    """

    type: Literal["dream"]

    usage: BetaDreamUsage
    """The tokens that a dream has used so far.

    The counts are zero while the dream is `pending` and update while it is
    `running`. They can keep changing after a cancel.

    See the
    [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#billing)
    for how dreams are billed. See the
    [prompt caching guide](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#tracking-cache-performance)
    for how the input token counts add up.
    """
