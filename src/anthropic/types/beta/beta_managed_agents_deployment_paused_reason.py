# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_error_deployment_paused_reason import BetaManagedAgentsErrorDeploymentPausedReason
from .beta_managed_agents_manual_deployment_paused_reason import BetaManagedAgentsManualDeploymentPausedReason

__all__ = ["BetaManagedAgentsDeploymentPausedReason"]

BetaManagedAgentsDeploymentPausedReason: TypeAlias = Annotated[
    Union[BetaManagedAgentsManualDeploymentPausedReason, BetaManagedAgentsErrorDeploymentPausedReason],
    PropertyInfo(discriminator="type"),
]
