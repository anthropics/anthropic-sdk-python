# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWorkspaceArchivedRunError"]


class BetaManagedAgentsWorkspaceArchivedRunError(BaseModel):
    """The deployment's workspace was archived."""

    message: str
    """Human-readable error description."""

    type: Literal["workspace_archived_error"]
