# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonError"]


class BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonError(BaseModel):
    """
    The deployment configures resources, but its environment is self-hosted and cannot mount them.
    """

    type: Literal["self_hosted_resources_unsupported_error"]
