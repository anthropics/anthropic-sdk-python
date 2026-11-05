from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .external_key_in_workspace_policy_error_details import ExternalKeyInWorkspacePolicyErrorDetails

__all__ = ["ExternalKeyInWorkspacePolicyError"]


class ExternalKeyInWorkspacePolicyError(BadRequestError):
    """
    The External Key can't be deleted or reconfigured while the organization's Workspace Policy lists it as an allowed key.
    """

    error_code: Literal["external_key_in_workspace_policy"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ExternalKeyInWorkspacePolicyErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
