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

    By default the dream writes its result to a new memory store and doesn't change the input memory store. With `output_behavior` set to `update_existing`, it writes its result into the input memory store instead.

    The Dreams API is in research preview: the request and response shapes are volatile and may change without the deprecation period that applies to generally-available endpoints.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#how-it-works) for what a dream reads and produces.
    """

    id: str
    """The unique ID of the dream (`drm_...`)."""

    archived_at: Optional[datetime] = None
    """When the dream was archived, in RFC 3339, or `null` if it hasn't been archived."""

    created_at: datetime
    """When the dream was created, in RFC 3339.

    Lists of dreams are sorted by this time, newest first.
    """

    ended_at: Optional[datetime] = None
    """
    When the dream reached `completed`, `failed`, or `canceled`, in RFC 3339, or
    `null` if it is still `pending` or `running`.
    """

    error: Optional[BetaDreamError] = None
    """Why the dream failed, or `null` if `status` isn't `failed`."""

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
    """Where the dream writes its result, as set in the request that created the dream.

    If that request left out `output_behavior`, the dream used the `create_new`
    behavior.
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
    """
    The dream's token counts, which stop changing once its `status` is `completed`
    or `failed`. After a cancel, they can keep changing.
    """
