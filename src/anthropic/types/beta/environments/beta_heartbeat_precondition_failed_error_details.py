from typing_extensions import Literal

from ...._models import BaseModel
from .beta_work_lease_state import BetaWorkLeaseState

__all__ = ["BetaHeartbeatPreconditionFailedErrorDetails"]


class BetaHeartbeatPreconditionFailedErrorDetails(BaseModel):
    """
    `expected_last_heartbeat` does not match the stored heartbeat, so another worker may hold the lease.
    """

    current_state: BetaWorkLeaseState
    """The lease as the server holds it."""

    error_code: Literal["heartbeat_precondition_failed"]
