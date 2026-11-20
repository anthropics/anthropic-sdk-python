from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_workspace_changed_concurrently_error_details import BetaWorkspaceChangedConcurrentlyErrorDetails

__all__ = ["BetaWorkspaceChangedConcurrentlyError"]


class BetaWorkspaceChangedConcurrentlyError(ConflictError):
    """
    Another request changed the Workspace, so this request left the setting named in `field` as it is. The error's `message` says which of this request's other changes are in place. Read the Workspace and send the request again if you still want the change.
    """

    error_code: Literal["workspace_changed_concurrently"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaWorkspaceChangedConcurrentlyErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
