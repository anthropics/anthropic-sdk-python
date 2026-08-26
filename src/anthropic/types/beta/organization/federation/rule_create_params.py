# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from ....anthropic_beta_param import AnthropicBetaParam
from .beta_federation_rule_match_param import BetaFederationRuleMatchParam
from .beta_service_account_target_param import BetaServiceAccountTargetParam

__all__ = ["RuleCreateParams"]


class RuleCreateParams(TypedDict, total=False):
    issuer_id: Required[str]
    """Tagged ID of the federation issuer."""

    match: Required[BetaFederationRuleMatchParam]
    """Conditions the verified JWT must satisfy for this rule to apply.

    At least one of `subject_prefix` (other than a wildcard-only value like `*`),
    `claims`, or `condition` is required; `audience` alone is not sufficient.
    """

    name: Required[str]
    """Slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    oauth_scope: Required[str]
    """Space-separated OAuth scopes.

    OAuth callers may only set `workspace:developer` or `workspace:inference`; other
    scopes (such as `org:admin`) require a Console session.
    """

    target: Required[BetaServiceAccountTargetParam]
    """Identity that tokens minted via this rule act as.

    Currently always a `service_account` target.
    """

    applies_to_all_workspaces: bool
    """
    When true, enable this rule for every workspace in the org (including workspaces
    created later).
    """

    attributes: Optional[Dict[str, str]]
    """CEL expressions `{name: expr}` extracting named values from claims.

    Not yet supported; any non-empty value is rejected with 400.
    """

    description: Optional[str]
    """Optional free-text description."""

    token_lifetime_seconds: int
    """Lifetime in seconds for access tokens minted via this rule (60-86400).

    Defaults to 3600 (1h). Minted tokens are capped at
    `max(60, min(this value, 2 × remaining assertion validity))` seconds.
    """

    workspace_id: Optional[str]
    """Tagged ID of the workspace to enable this rule for.

    Required unless `applies_to_all_workspaces` is true. Additional workspaces can
    be added via the `/federation_rules/{federation_rule_id}/workspaces`
    sub-resource.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
