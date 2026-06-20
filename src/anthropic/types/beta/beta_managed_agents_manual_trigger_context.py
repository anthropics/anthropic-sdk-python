# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsManualTriggerContext"]


class BetaManagedAgentsManualTriggerContext(BaseModel):
    """
    The run was started manually by creating a session directly against the deployment.
    """

    type: Literal["manual"]
