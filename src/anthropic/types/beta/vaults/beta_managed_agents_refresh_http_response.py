# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsRefreshHTTPResponse"]


class BetaManagedAgentsRefreshHTTPResponse(BaseModel):
    """An HTTP response captured during a credential validation probe."""

    body: str
    """Response body. May be truncated and has sensitive values scrubbed."""

    body_truncated: bool
    """Whether `body` was truncated."""

    content_type: str
    """Value of the `Content-Type` response header."""

    status_code: int
    """HTTP status code."""
