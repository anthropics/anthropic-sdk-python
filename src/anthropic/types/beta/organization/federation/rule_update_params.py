# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo
from ....anthropic_beta_param import AnthropicBetaParam
from .beta_federation_rule_match_param import BetaFederationRuleMatchParam
from .beta_service_account_target_param import BetaServiceAccountTargetParam

__all__ = ["RuleUpdateParams"]


class RuleUpdateParams(TypedDict, total=False):
    applies_to_all_workspaces: Optional[bool]
    """
    When true, enables this rule for every workspace in the org (including
    workspaces created later). Setting `false` is rejected with 400 if no workspace
    would remain enabled; a rule with only a legacy `workspace_id` binding continues
    to mint.
    """

    attributes: Optional[Dict[str, str]]
    """Replaces the CEL expressions `{name: expr}` extracting named values from claims.

    Send null to clear them. Not yet supported; any non-empty value is rejected
    with 400.
    """

    description: Optional[str]
    """Replaces the description.

    Omit to leave unchanged; send `null` to clear (the field is stored as an empty
    string).
    """

    match: Optional[BetaFederationRuleMatchParam]
    """Does the incoming JWT qualify?

    All populated fields must pass; omitted fields are skipped. At least one of
    `subject_prefix` (other than a wildcard-only value like `*`), `claims`, or
    `condition` is required; `audience` alone is not sufficient.
    """

    name: Optional[str]
    """Replaces the slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    oauth_scope: Optional[str]
    """Replaces the space-separated OAuth scopes granted on minted tokens.

    OAuth callers may only set `workspace:developer` or `workspace:inference`; other
    scopes (such as `org:admin`) require a Console session.
    """

    target: Optional[BetaServiceAccountTargetParam]
    """Bind to a fixed service account by ID."""

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

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
