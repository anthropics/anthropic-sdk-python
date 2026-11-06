from typing_extensions import Literal

from ...._models import BaseModel
from .beta_telemetry_destination_disabled_reason import BetaTelemetryDestinationDisabledReason

__all__ = ["BetaTelemetryDestinationStateDisabled"]


class BetaTelemetryDestinationStateDisabled(BaseModel):
    """The API doesn't deliver anything to the telemetry destination.

    Spans produced while it is disabled aren't delivered later.
    """

    reason: BetaTelemetryDestinationDisabledReason
    """Whether a caller or the API disabled the destination and, when the API did, why.

    Read-only.
    """

    type: Literal["disabled"]
