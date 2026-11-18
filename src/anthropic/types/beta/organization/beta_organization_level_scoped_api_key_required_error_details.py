from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails"]


class BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails(BaseModel):
    """The credential is not a scoped API key that is bound at the organization level."""

    error_code: Literal["organization_level_scoped_api_key_required"]
