# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["CertificateListParams"]


class CertificateListParams(TypedDict, total=False):
    include_archived: bool
    """Whether to include archived certificates in the results. Defaults to false."""

    limit: int
    """Maximum number of certificates to return per page.

    Defaults to 20, maximum 1000.
    """

    page: str
    """Opaque pagination cursor from a previous `list_tunnel_certificates` response."""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
