from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .federation_rule_match import FederationRuleMatch
from .service_account_target import ServiceAccountTarget

__all__ = ["FederationRule"]


class FederationRule(BaseModel):
    """Authorization rule binding an external OIDC identity to Anthropic.

    Evaluates the match conditions and mints an OAuth access token for the
    resolved target, scoped to a single workspace where the rule is enabled
    (chosen by the caller at exchange time when the rule is enabled for more
    than one). For rules enabled via `workspace_ids` or
    `applies_to_all_workspaces`, the target service account must be a member
    of that workspace (it is implicitly a member of the default workspace);
    rules carrying only the legacy `workspace_id` binding do not enforce
    this.
    """

    id: str
    """Tagged ID of the federation rule."""

    applies_to_all_workspaces: bool
    """
    When true, this rule is enabled for every workspace in the org (including ones
    created after the rule). `workspace_ids` is ignored at exchange time.
    """

    archived_at: Optional[datetime] = None
    """If set, this rule is archived and rejects token exchange."""

    archived_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that archived this rule."""

    created_at: datetime
    """When this rule was created."""

    created_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that created this rule."""

    description: Optional[str] = None
    """Optional free-text description."""

    issuer_id: str
    """Tagged ID of the issuer whose tokens this rule accepts."""

    issuer_name: Optional[str] = None
    """Issuer's display name at read time."""

    match: FederationRuleMatch
    """Conditions the verified JWT must satisfy for this rule to apply.

    All populated matcher fields must pass.
    """

    name: str
    """Admin-chosen slug identifier."""

    oauth_scope: str
    """Space-separated OAuth scopes granted on the minted token."""

    target: ServiceAccountTarget
    """What this rule targets.

    Check `type` before reading the other fields. Tokens minted via a rule whose
    target `type` is `service_account` act as that service account.
    """

    token_lifetime_seconds: int
    """Lifetime in seconds of access tokens minted via this rule.

    Minted tokens are capped at
    `max(60, min(this value, 2 × remaining assertion validity))` seconds.
    """

    type: Literal["federation_rule"]

    updated_at: datetime
    """When this rule was last updated."""

    updated_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that last updated this rule."""

    workspace_ids: List[str]
    """Tagged IDs of the workspaces this rule is enabled for.

    May be empty for older rules that only carry the legacy `workspace_id` binding.
    Ignored at exchange time when `applies_to_all_workspaces` is true (the list may
    still be non-empty).
    """
