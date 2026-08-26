# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["ServiceAccountCreateParams"]


class ServiceAccountCreateParams(TypedDict, total=False):
    name: Required[str]
    """Slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    description: Optional[str]
    """Optional free-text description."""

    organization_role: Literal["admin", "developer"]
    """Org-level role. Defaults to `developer`."""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
