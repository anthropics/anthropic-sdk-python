# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_session_agent_update_param import BetaManagedAgentsSessionAgentUpdateParam

__all__ = ["SessionUpdateParams"]


class SessionUpdateParams(TypedDict, total=False):
    agent: BetaManagedAgentsSessionAgentUpdateParam
    """Mid-session agent configuration update.

    Only `tools` and `mcp_servers` are updatable. Full replacement: the provided
    array becomes the new value. To preserve existing entries, GET the session,
    modify the array, and POST it back.
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

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
