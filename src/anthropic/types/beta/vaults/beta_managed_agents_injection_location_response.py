# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsInjectionLocationResponse"]


class BetaManagedAgentsInjectionLocationResponse(BaseModel):
    """Where in the outbound request the secret value is substituted."""

    body: bool
    """Whether the placeholder is substituted in the request body."""

    header: bool
    """Whether the placeholder is substituted in request header values."""
