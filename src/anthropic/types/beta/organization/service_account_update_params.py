# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["ServiceAccountUpdateParams"]


class ServiceAccountUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """Replaces the description.

    Omit to leave unchanged; send `null` to clear (the field is stored as an empty
    string).
    """

    organization_role: Optional[Literal["admin", "developer"]]
    """Replaces the org-level role. Omit or send `null` to leave unchanged."""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
