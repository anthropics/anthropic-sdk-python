from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .workspace_policy_violation_error_details import WorkspacePolicyViolationErrorDetails

__all__ = ["WorkspacePolicyViolationError"]


class WorkspacePolicyViolationError(BadRequestError):
    """The request breaks the organization's Workspace Policy.

    The message says which rule it broke; an organization admin can see and change the policy in the Console.
    """

    error_code: Literal["workspace_policy_violation"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: WorkspacePolicyViolationErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
