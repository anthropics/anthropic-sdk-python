# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_text_block_param import BetaManagedAgentsTextBlockParam
from .beta_managed_agents_image_block_param import BetaManagedAgentsImageBlockParam
from .beta_managed_agents_document_block_param import BetaManagedAgentsDocumentBlockParam
from .beta_managed_agents_search_result_block_param import BetaManagedAgentsSearchResultBlockParam

__all__ = ["BetaManagedAgentsUserToolResultEventParams", "Content"]

Content: TypeAlias = Union[
    BetaManagedAgentsTextBlockParam,
    BetaManagedAgentsImageBlockParam,
    BetaManagedAgentsDocumentBlockParam,
    BetaManagedAgentsSearchResultBlockParam,
]


class BetaManagedAgentsUserToolResultEventParams(TypedDict, total=False):
    """Parameters for providing the result of an agent-toolset tool execution.

    Only valid on `self_hosted` environments, where sandbox-routed tools are executed by the client rather than the server.
    """

    tool_use_id: Required[str]
    """
    The id of the `agent.tool_use` event this result corresponds to, which can be
    found in the last `session.status_idle`
    [event's](https://platform.claude.com/docs/en/api/beta/sessions/events/list#beta_managed_agents_session_requires_action.event_ids)
    `stop_reason.event_ids` field.
    """

    type: Required[Literal["user.tool_result"]]

    content: Iterable[Content]
    """The result content returned by the tool."""

    is_error: Optional[bool]
    """Whether the tool execution resulted in an error."""
