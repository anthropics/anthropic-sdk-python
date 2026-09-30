from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaSpendLimitOrganizationScopeParam"]


class BetaSpendLimitOrganizationScopeParam(TypedDict, total=False):
    type: Required[Literal["organization"]]
