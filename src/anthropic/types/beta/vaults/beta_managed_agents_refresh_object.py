from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_refresh_http_response import BetaManagedAgentsRefreshHTTPResponse

__all__ = ["BetaManagedAgentsRefreshObject"]


class BetaManagedAgentsRefreshObject(BaseModel):
    """Outcome of a refresh-token exchange attempted during credential validation."""

    http_response: Optional[BetaManagedAgentsRefreshHTTPResponse] = None
    """An HTTP response captured during a credential validation probe."""

    status: Literal["succeeded", "failed", "connect_error", "no_refresh_token"]
    """Outcome of a refresh-token exchange attempted during credential validation.

    - `succeeded` - The token endpoint returned a new access token.
    - `failed` - The token endpoint returned an error response. See `http_response`
      for detail.
    - `connect_error` - The token endpoint could not be reached (DNS, TLS, or
      connection error).
    - `no_refresh_token` - No refresh token is stored for the credential, so no
      exchange was attempted.
    """
