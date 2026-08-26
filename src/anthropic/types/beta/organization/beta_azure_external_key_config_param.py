# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaAzureExternalKeyConfigParam"]


class BetaAzureExternalKeyConfigParam(TypedDict, total=False):
    """Azure Key Vault provider configuration."""

    key_name: Required[str]
    """Name of the key within the vault."""

    tenant_id: Required[str]
    """Azure AD tenant ID."""

    type: Required[Literal["azure"]]

    vault_uri: Required[str]
    """
    Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or
    `https://{hsm-name}.managedhsm.azure.net`.
    """

    client_id: Optional[str]
    """Azure AD application (client) ID.

    Omit to use Anthropic's multitenant app. Provide only if using a single-tenant
    app registration in the customer's directory.
    """
