from typing_extensions import Literal

from ...._exceptions import PreconditionFailedError
from .beta_heartbeat_precondition_failed_error_details import BetaHeartbeatPreconditionFailedErrorDetails

__all__ = ["BetaHeartbeatPreconditionFailedError"]


class BetaHeartbeatPreconditionFailedError(PreconditionFailedError):
    """
    `expected_last_heartbeat` does not match the stored heartbeat, so another worker may hold the lease.
    """

    error_code: Literal["heartbeat_precondition_failed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaHeartbeatPreconditionFailedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
