from typing import Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationDeliveryHealth"]


class BetaTelemetryDestinationDeliveryHealth(BaseModel):
    """
    The most recent delivery results that the API records for a telemetry destination.

    Changes to the destination's configuration or state don't reset these fields. Changes to these fields don't change `updated_at`. The values can lag behind the latest deliveries.

    See the [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health) to learn how the API delivers spans and when it disables a destination.
    """

    last_error: Optional[str] = None
    """
    A message that describes the most recent failed delivery to the destination, or
    `null` if no delivery has failed yet.

    Examples are `temporary DNS failure`, `TLS failure`, `timeout`,
    `connection failure`, `invalid address`, `HTTP error (status 503)`, and
    `redirect (status 301)`. The message is `invalid address` both for a hostname
    that doesn't exist and for an address that isn't publicly routable. It never
    contains the endpoint's response body, a header value, a network address, or TLS
    details.

    `last_error` and `last_error_at` always change together. A later successful
    delivery doesn't clear them. If `last_success_at` is later than `last_error_at`,
    a delivery has succeeded since this failure.

    See the
    [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-errors)
    to learn the likely cause of each error.
    """

    last_error_at: Optional[datetime] = None
    """Time of the failure that `last_error` describes.

    Changes together with `last_error`. Null until a delivery first fails.
    """

    last_success_at: Optional[datetime] = None
    """
    Time of the most recent successful delivery to the destination, or `null` if no
    delivery has succeeded yet.
    """
