from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["CertificateCreateParams"]


class CertificateCreateParams(TypedDict, total=False):
    ca_certificate_pem: Required[str]
    """PEM-encoded X.509 CA certificate.

    Must contain exactly one certificate and no private-key material. Maximum 8KB.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
