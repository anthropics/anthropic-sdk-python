from typing_extensions import Literal

from .._exceptions import ConflictError
from .beta_gcp_project_controlled_by_another_organization_error_details import (
    BetaGCPProjectControlledByAnotherOrganizationErrorDetails,
)

__all__ = ["BetaGCPProjectControlledByAnotherOrganizationError"]


class BetaGCPProjectControlledByAnotherOrganizationError(ConflictError):
    """
    Another organization has data controls turned on for this Google Cloud project, or turned them off recently. The message says how long to wait.
    """

    error_code: Literal["gcp_project_controlled_by_another_organization"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaGCPProjectControlledByAnotherOrganizationErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
