from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_mcp_probe import BetaManagedAgentsMCPProbe
from .beta_managed_agents_refresh_object import BetaManagedAgentsRefreshObject
from .beta_managed_agents_credential_validation_status import BetaManagedAgentsCredentialValidationStatus

__all__ = ["BetaManagedAgentsCredentialValidation"]


class BetaManagedAgentsCredentialValidation(BaseModel):
    """Result of live-probing a credential against its configured MCP server."""

    credential_id: str
    """Unique identifier of the credential that was validated."""

    has_refresh_token: bool
    """Whether the credential has a refresh token configured."""

    mcp_probe: Optional[BetaManagedAgentsMCPProbe] = None
    """Details of the failing MCP probe step. Null when the probe succeeded."""

    refresh: Optional[BetaManagedAgentsRefreshObject] = None
    """Details of the refresh-token exchange attempted on a 401.

    Null when no refresh was attempted.
    """

    status: BetaManagedAgentsCredentialValidationStatus
    """Overall verdict of the validation probe."""

    type: Literal["vault_credential_validation"]

    validated_at: datetime
    """When the validation probe was performed."""

    vault_id: str
    """Identifier of the vault containing the credential."""
