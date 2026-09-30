from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["WorkspaceRateLimitOrganizationSource"]


class WorkspaceRateLimitOrganizationSource(BaseModel):
    type: Literal["organization"]
    """
    Always `organization`: no workspace-level override is stored, so the
    organization's value applies.
    """
