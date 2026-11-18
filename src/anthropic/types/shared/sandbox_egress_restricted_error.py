from typing_extensions import Literal

from ..._exceptions import PermissionDeniedError
from .sandbox_egress_restricted_error_details import SandboxEgressRestrictedErrorDetails

__all__ = ["SandboxEgressRestrictedError"]


class SandboxEgressRestrictedError(PermissionDeniedError):
    """
    The request came from a Claude sandbox with restricted network access, which is not allowed to make this change. Send it from outside the sandbox, or from a sandbox with unrestricted network access.
    """

    error_code: Literal["sandbox_egress_restricted"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: SandboxEgressRestrictedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
