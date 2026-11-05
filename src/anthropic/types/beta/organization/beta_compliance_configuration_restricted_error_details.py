from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaComplianceConfigurationRestrictedErrorDetails"]


class BetaComplianceConfigurationRestrictedErrorDetails(BaseModel):
    """
    The organization's compliance configuration does not let Claude Tag store anything new.
    """

    error_code: Literal["compliance_configuration_restricted"]
