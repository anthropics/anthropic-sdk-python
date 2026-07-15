# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookSessionThreadIdledEventData"]


class BetaWebhookSessionThreadIdledEventData(BaseModel):
    id: str
    """ID of the session that triggered the event."""

    organization_id: str

    session_thread_id: str
    """ID of the session thread this event refers to."""

    type: Literal["session.thread_idled"]

    workspace_id: str
