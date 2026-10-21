from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .federation_rule_match_param import FederationRuleMatchParam
from .service_account_target_param import ServiceAccountTargetParam

__all__ = ["RuleUpdateParams"]


class RuleUpdateParams(TypedDict, total=False):
    applies_to_all_workspaces: Optional[bool]
    """
    When true, enables this rule for every workspace in the org (including
    workspaces created later). Setting `false` is rejected with 400 if no workspace
    would remain enabled; a rule with only a legacy `workspace_id` binding continues
    to mint.
    """

    description: Optional[str]
    """Replaces the description.

    Omit to leave unchanged; send `null` to clear (the field is stored as an empty
    string).
    """

    match: Optional[FederationRuleMatchParam]
    """Replaces the entire match object. All populated matcher fields must pass."""

    name: Optional[str]
    """Replaces the slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    oauth_scope: Optional[str]
    """Replaces the space-separated OAuth scopes granted on minted tokens.

    OAuth callers may only set `workspace:developer` or `workspace:inference`; other
    scopes (such as `org:admin`) require a Console session.
    """

    target: Optional[ServiceAccountTargetParam]
    """Replaces the entire target object. Currently always a `service_account` target."""

    token_lifetime_seconds: Optional[int]
    """
    Replaces the lifetime in seconds for access tokens minted via this rule
    (60-86400). Minted tokens are capped at
    `max(60, min(this value, 2 × remaining assertion validity))` seconds.
    """

    workspace_id: Optional[str]
    """Replaces the existing single workspace enablement (the previous one is removed).

    Rejected with 400 if the rule is enabled for more than one workspace; use the
    `/federation_rules/{federation_rule_id}/workspaces` sub-resource instead.
    """
