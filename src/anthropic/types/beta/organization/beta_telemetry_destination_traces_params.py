from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_telemetry_destination_content_mode import BetaTelemetryDestinationContentMode

__all__ = ["BetaTelemetryDestinationTracesParams"]


class BetaTelemetryDestinationTracesParams(TypedDict, total=False):
    """
    The settings for the traces that a telemetry destination receives, as a create or update request sets them. An omitted field takes its default on create and keeps its stored value on update.
    """

    content_mode: Optional[BetaTelemetryDestinationContentMode]
    """What the exported spans contain. Defaults to `metadata_only` on create.

    On update, `null` sets `metadata_only`.
    """

    enabled: bool
    """Whether the destination receives traces.

    Defaults to true on create. It cannot be null.
    """

    endpoint_url: Optional[str]
    """
    The full URL of your collector's traces endpoint, for a collector that takes
    traces on a path other than `/v1/traces`. The API posts traces to it exactly as
    given and appends nothing.

    The same rules as for `endpoint_url` apply, except that any path is allowed. It
    must have the same scheme, host, and port as `endpoint_url`. At most 2,048
    characters.

    On create, `null` is the same as leaving it out. On update, `null` removes it.
    The API then posts traces to `endpoint_url` with `/v1/traces` appended. A change
    of this URL alone keeps the registered headers.
    """

    max_content_bytes: Optional[int]
    """
    The most bytes of content that one exported span can contain, from 1 up to the
    API's maximum. `null` sets no bound, so only the API's maximum applies.

    On create, leaving it out is the same as `null`. The error for a value above the
    maximum states the maximum.
    """
