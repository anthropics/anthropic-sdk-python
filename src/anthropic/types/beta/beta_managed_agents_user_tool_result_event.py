# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .sessions.beta_managed_agents_text_block import BetaManagedAgentsTextBlock
from .sessions.beta_managed_agents_image_block import BetaManagedAgentsImageBlock
from .sessions.beta_managed_agents_document_block import BetaManagedAgentsDocumentBlock
from .sessions.beta_managed_agents_search_result_block import BetaManagedAgentsSearchResultBlock

__all__ = ["BetaManagedAgentsUserToolResultEvent", "Content"]

Content: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsTextBlock,
        BetaManagedAgentsImageBlock,
        BetaManagedAgentsDocumentBlock,
        BetaManagedAgentsSearchResultBlock,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaManagedAgentsUserToolResultEvent(BaseModel):
    """Event sent by the client providing the result of an agent-toolset tool execution.

    Only valid on `self_hosted` environments, where sandbox-routed tools are executed by the client rather than the server.
    """

    id: str
    """Unique identifier for this event."""

    tool_use_id: str
    """
    The id of the `agent.tool_use` event this result corresponds to, which can be
    found in the last `session.status_idle`
    [event's](https://platform.claude.com/docs/en/api/beta/sessions/events/list#beta_managed_agents_session_requires_action.event_ids)
    `stop_reason.event_ids` field.
    """

    type: Literal["user.tool_result"]

    content: Optional[List[Content]] = None
    """The result content returned by the tool."""

    is_error: Optional[bool] = None
    """Whether the tool execution resulted in an error."""

    processed_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    session_thread_id: Optional[str] = None
    """Routes this result to a subagent thread.

    Copy from the `agent.tool_use` event's `session_thread_id`.
    """
