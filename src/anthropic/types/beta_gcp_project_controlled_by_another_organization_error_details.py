from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaGCPProjectControlledByAnotherOrganizationErrorDetails"]


class BetaGCPProjectControlledByAnotherOrganizationErrorDetails(BaseModel):
    """
    Another organization has data controls turned on for this Google Cloud project, or turned them off recently. The message says how long to wait.
    """

    error_code: Literal["gcp_project_controlled_by_another_organization"]
