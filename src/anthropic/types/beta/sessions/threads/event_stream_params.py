# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from ....anthropic_beta_param import AnthropicBetaParam
from ...beta_managed_agents_delta_type import BetaManagedAgentsDeltaType

__all__ = ["EventStreamParams"]


class EventStreamParams(TypedDict, total=False):
    session_id: Required[str]

    event_deltas: List[BetaManagedAgentsDeltaType]
    """
    When set, this connection also receives streaming deltas (`event_start`,
    `event_delta`) while an event is being produced, before the event itself
    arrives. Deltas are best-effort; when the final event is produced it carries the
    complete content. A model request that ends early (an error or interrupt)
    produces no final event — its terminal `span.model_request_end` closes the
    preview. Accepts one or more event types to preview and may be repeated:
    `agent.message` streams `content_delta` fragments; `agent.thinking` is
    start-only — a signal that the agent has begun extended thinking, concluded by
    the `agent.thinking` event itself. Only previews of the requested event types
    are sent.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
