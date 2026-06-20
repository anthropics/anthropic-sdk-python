# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsFileNotFoundDeploymentPausedReasonError"]


class BetaManagedAgentsFileNotFoundDeploymentPausedReasonError(BaseModel):
    """A file resource referenced by the deployment no longer exists."""

    type: Literal["file_not_found_error"]
