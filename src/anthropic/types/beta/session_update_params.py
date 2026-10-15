from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from ..._types import SequenceNotStr
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_budget_limit_param import BetaManagedAgentsBudgetLimitParam
from .beta_managed_agents_session_agent_update_param import BetaManagedAgentsSessionAgentUpdateParam

__all__ = ["SessionUpdateParams"]


class SessionUpdateParams(TypedDict, total=False):
    agent: BetaManagedAgentsSessionAgentUpdateParam
    """Agent configuration update.

    Only `tools` and `mcp_servers` are updatable mid-session. Only valid for
    sessions created from an agent or deployment reference. The session must not be
    running.
    """

    budget: Optional[BetaManagedAgentsBudgetLimitParam]
    """Enforced spend ceiling for the session.

    Set an object to replace the budget of a session that was created with one, or
    `null` to remove it; omit to preserve. A budget cannot be added to a session
    created without one (rejected with reason `budget_create_only`), and a removed
    budget cannot be re-added. Allowed in any non-terminated status. Lowering
    `max_list_cost` to at or below the session's consumed list cost is rejected with
    reason `budget_not_raised`, and every model the session can run must have a
    public list price or the request is rejected with reason `model_not_budgetable`.
    """

    metadata: Optional[Dict[str, Optional[str]]]
    """Metadata patch.

    Set a key to a string to upsert it, or to null to delete it. Omit the field to
    preserve.
    """

    title: Optional[str]
    """Human-readable session title."""

    vault_ids: SequenceNotStr[str]
    """Vault IDs (`vlt_*`) to attach to the session.

    Not yet supported; requests setting this field are rejected. Reserved for future
    use.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
