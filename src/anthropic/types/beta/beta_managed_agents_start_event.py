# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_start_event_preview import BetaManagedAgentsStartEventPreview

__all__ = ["BetaManagedAgentsStartEvent"]


class BetaManagedAgentsStartEvent(BaseModel):
    """Opens a preview of a buffered event.

    Carries the previewed event's type and id only. Followed by zero or more event_delta events with the same event id, normally concluded by the buffered event carrying that id. If the producing model request ends without that event (an error or interrupt mid-stream), its terminal span.model_request_end closes the preview. Only sent on stream connections that opt in via event_deltas; never appears in event history.
    """

    event: BetaManagedAgentsStartEventPreview
    """The previewed event's type and id.

    The event type determines which delta types the preview's event_delta events
    carry: agent.message events stream content_delta fragments; agent.thinking
    previews are start-only — no deltas follow, and the buffered agent.thinking with
    the same id concludes them.
    """

    type: Literal["event_start"]
