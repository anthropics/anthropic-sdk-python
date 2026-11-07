from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_spend_limit_period import BetaSpendLimitPeriod
from .beta_spend_limit_user_scope_param import BetaSpendLimitUserScopeParam
from .beta_spend_limit_workspace_scope_param import BetaSpendLimitWorkspaceScopeParam
from .beta_spend_limit_organization_scope_param import BetaSpendLimitOrganizationScopeParam

__all__ = ["SpendLimitSetParams", "Scope"]


class SpendLimitSetParams(TypedDict, total=False):
    amount: Required[Optional[str]]
    """
    Limit amount as a non-negative integer decimal string in the minor unit of the
    organization's billing currency (cents for USD): "50000" is $500.00. `null` sets
    an explicit no-limit override for this scope and `period` only — each period
    resolves independently, so caps for other periods still apply.
    """

    scope: Required[Scope]
    """What the limit applies to.

    Claude Enterprise organizations set `user` limits. Claude Console organizations
    set `organization` and `workspace` limits. Any other combination returns 400.
    Setting `organization` and `workspace` limits through the API is in an early
    access preview. To request access, contact your Anthropic account team.
    """

    period: BetaSpendLimitPeriod

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""


Scope: TypeAlias = Union[
    BetaSpendLimitUserScopeParam, BetaSpendLimitOrganizationScopeParam, BetaSpendLimitWorkspaceScopeParam
]
