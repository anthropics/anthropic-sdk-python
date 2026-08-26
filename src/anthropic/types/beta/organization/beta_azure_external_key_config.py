# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAzureExternalKeyConfig"]


class BetaAzureExternalKeyConfig(BaseModel):
    key_name: str
    """Name of the key within the vault."""

    tenant_id: str
    """Azure AD tenant ID."""

    type: Literal["azure"]

    vault_uri: str
    """
    Key Vault data-plane URI — `https://{vault-name}.vault.azure.net` or
    `https://{hsm-name}.managedhsm.azure.net`.
    """

    client_id: Optional[str] = None
    """Azure AD application (client) ID.

    Omit to use Anthropic's multitenant app. Provide only if using a single-tenant
    app registration in the customer's directory.
    """
