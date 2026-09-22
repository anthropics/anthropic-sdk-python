from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_event_params import BetaManagedAgentsEventParams

__all__ = ["EventSendParams"]


class EventSendParams(TypedDict, total=False):
    events: Required[Iterable[BetaManagedAgentsEventParams]]
    """Events to send to the `session`."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
