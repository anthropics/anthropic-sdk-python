from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsServiceAccountExecutionIdentity"]


class BetaManagedAgentsServiceAccountExecutionIdentity(BaseModel):
    """The Anthropic-managed service account as returned in API responses."""

    type: Literal["service_account"]
