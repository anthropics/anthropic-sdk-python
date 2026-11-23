from typing_extensions import Literal

from ...._models import BaseModel
from .beta_workspace_changed_concurrently_field import BetaWorkspaceChangedConcurrentlyField

__all__ = ["BetaWorkspaceChangedConcurrentlyErrorDetails"]


class BetaWorkspaceChangedConcurrentlyErrorDetails(BaseModel):
    """
    Another request changed the Workspace, so this request left the setting named in `field` as it is. The error's `message` says which of this request's other changes are in place. Read the Workspace and send the request again if you still want the change.
    """

    error_code: Literal["workspace_changed_concurrently"]

    field: BetaWorkspaceChangedConcurrentlyField
    """The request field whose change was refused.

    Other values may be returned. The value is a name with no data of its own.
    """
