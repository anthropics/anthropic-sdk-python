# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonError"]


class BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonError(BaseModel):
    """A memory store referenced by the deployment is archived."""

    type: Literal["memory_store_archived_error"]
