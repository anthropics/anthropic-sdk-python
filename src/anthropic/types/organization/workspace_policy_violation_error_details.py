from typing_extensions import Literal

from ..._models import BaseModel
from .workspace_policy_field import WorkspacePolicyField

__all__ = ["WorkspacePolicyViolationErrorDetails"]


class WorkspacePolicyViolationErrorDetails(BaseModel):
    """The request breaks the organization's Workspace Policy.

    The message says which rule it broke; an organization admin can see and change the policy in the Console.
    """

    error_code: Literal["workspace_policy_violation"]

    field: WorkspacePolicyField
    """The request field the broken rule applies to."""
