# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaWebhookVaultCredentialArchivedEventData"]


class BetaWebhookVaultCredentialArchivedEventData(BaseModel):
    id: str
    """ID of the resource that triggered the event."""

    organization_id: str

    type: Literal["vault_credential.archived"]

    vault_id: str
    """ID of the vault that owns this credential."""

    workspace_id: str
