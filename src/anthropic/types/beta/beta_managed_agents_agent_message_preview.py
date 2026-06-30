# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentMessagePreview"]


class BetaManagedAgentsAgentMessagePreview(BaseModel):
    id: str
    """The id the buffered agent.message will carry if it is emitted.

    Matches the event_id on this preview's event_delta events.
    """

    type: Literal["agent.message"]
