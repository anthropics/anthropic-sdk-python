from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaTelemetryDestinationStateEnabledParams"]


class BetaTelemetryDestinationStateEnabledParams(TypedDict, total=False):
    """Start deliveries to the telemetry destination again.

    This doesn't reset `delivery_health`.
    """

    type: Required[Literal["enabled"]]
