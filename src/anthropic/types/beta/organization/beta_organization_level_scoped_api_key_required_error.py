from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_organization_level_scoped_api_key_required_error_details import (
    BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails,
)

__all__ = ["BetaOrganizationLevelScopedAPIKeyRequiredError"]


class BetaOrganizationLevelScopedAPIKeyRequiredError(PermissionDeniedError):
    """The credential is not a scoped API key that is bound at the organization level."""

    error_code: Literal["organization_level_scoped_api_key_required"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
