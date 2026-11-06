from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationTestFailure"]


class BetaTelemetryDestinationTestFailure(BaseModel):
    """The test span was not delivered."""

    error: str
    """
    A message that describes why the test span was not delivered, including the HTTP
    status code when the destination returned one. Examples:
    `HTTP error (status 403)`, `timeout`, `TLS failure`. It has the same form as the
    destination's `delivery_health.last_error` and never contains the destination's
    response body, any header value, a network address, or TLS details.
    """

    type: Literal["failure"]
