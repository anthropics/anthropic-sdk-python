# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsVaultNotFoundDeploymentPausedReasonError"]


class BetaManagedAgentsVaultNotFoundDeploymentPausedReasonError(BaseModel):
    """A vault referenced by the deployment no longer exists."""

    type: Literal["vault_not_found_error"]
