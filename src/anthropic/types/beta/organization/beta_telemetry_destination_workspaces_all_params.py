from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaTelemetryDestinationWorkspacesAllParams"]


class BetaTelemetryDestinationWorkspacesAllParams(TypedDict, total=False):
    """Cover every workspace of the organization. Doesn't take `workspace_ids`.

    An update that sets `all` empties the destination's workspace list.
    """

    type: Required[Literal["all"]]
