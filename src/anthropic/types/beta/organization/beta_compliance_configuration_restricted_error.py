from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_compliance_configuration_restricted_error_details import BetaComplianceConfigurationRestrictedErrorDetails

__all__ = ["BetaComplianceConfigurationRestrictedError"]


class BetaComplianceConfigurationRestrictedError(PermissionDeniedError):
    """
    The organization's compliance configuration does not let Claude Tag store anything new.
    """

    error_code: Literal["compliance_configuration_restricted"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaComplianceConfigurationRestrictedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
