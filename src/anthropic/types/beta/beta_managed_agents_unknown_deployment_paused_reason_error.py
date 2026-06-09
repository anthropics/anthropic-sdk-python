# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsUnknownDeploymentPausedReasonError"]


class BetaManagedAgentsUnknownDeploymentPausedReasonError(BaseModel):
    """An unrecognized error auto-paused the deployment.

    A fallback variant; matches a run whose `error.type` is `unknown_error`.
    """

    type: Literal["unknown_error"]
