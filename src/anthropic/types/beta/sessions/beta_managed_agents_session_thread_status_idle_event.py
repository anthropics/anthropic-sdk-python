# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_managed_agents_session_end_turn import BetaManagedAgentsSessionEndTurn
from .beta_managed_agents_session_requires_action import BetaManagedAgentsSessionRequiresAction
from .beta_managed_agents_session_retries_exhausted import BetaManagedAgentsSessionRetriesExhausted

__all__ = ["BetaManagedAgentsSessionThreadStatusIdleEvent", "StopReason"]

StopReason: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsSessionEndTurn,
        BetaManagedAgentsSessionRequiresAction,
        BetaManagedAgentsSessionRetriesExhausted,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsSessionThreadStatusIdleEvent(BaseModel):
    """A session thread has yielded and is awaiting input.

    Emitted on the thread's own stream and cross-posted to the primary stream for child threads.
    """

    id: str
    """Unique identifier for this event."""

    agent_name: str
    """Name of the agent the thread runs."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    session_thread_id: str
    """Public sthr\\__ ID of the thread that went idle."""

    stop_reason: StopReason
    """The agent completed its turn naturally and is ready for the next user message."""

    type: Literal["session.thread_status_idle"]
