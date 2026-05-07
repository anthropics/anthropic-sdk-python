# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

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
    """The failing step of an MCP validation probe."""

    refresh: Optional[BetaManagedAgentsRefreshObject] = None
    """Outcome of a refresh-token exchange attempted during credential validation."""

    status: BetaManagedAgentsCredentialValidationStatus
    """Overall verdict of a credential validation probe."""

    type: Literal["vault_credential_validation"]

    validated_at: datetime
    """A timestamp in RFC 3339 format"""

    vault_id: str
    """Identifier of the vault containing the credential."""
