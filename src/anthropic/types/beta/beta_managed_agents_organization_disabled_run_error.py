# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsOrganizationDisabledRunError"]


class BetaManagedAgentsOrganizationDisabledRunError(BaseModel):
    """The deployment's organization is disabled."""

    message: str
    """Human-readable error description."""

    type: Literal["organization_disabled_error"]
