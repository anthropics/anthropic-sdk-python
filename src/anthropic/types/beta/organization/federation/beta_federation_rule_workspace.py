# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaFederationRuleWorkspace"]


class BetaFederationRuleWorkspace(BaseModel):
    created_at: datetime
    """When this workspace was enabled for the rule."""

    created_by_actor_id: Optional[str] = None
    """
    Tagged ID (`user_...` or `svac_...`) of the actor that enabled this workspace
    for the rule, if known.
    """

    federation_rule_id: str
    """Tagged ID of the federation rule."""

    type: Literal["federation_rule_workspace"]

    workspace_id: str
    """Tagged ID of the workspace this rule is enabled for."""

    workspace_name: Optional[str] = None
    """Workspace display name. Populated when listing; null in the enable response."""
