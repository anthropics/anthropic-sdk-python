# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonError"]


class BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonError(BaseModel):
    """The deployment's workspace was archived."""

    type: Literal["workspace_archived_error"]
