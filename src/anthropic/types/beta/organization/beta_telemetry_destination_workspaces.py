from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_telemetry_destination_workspaces_all import BetaTelemetryDestinationWorkspacesAll
from .beta_telemetry_destination_workspaces_exclude import BetaTelemetryDestinationWorkspacesExclude
from .beta_telemetry_destination_workspaces_include import BetaTelemetryDestinationWorkspacesInclude

__all__ = ["BetaTelemetryDestinationWorkspaces"]

BetaTelemetryDestinationWorkspaces: TypeAlias = Annotated[
    Union[
        BetaTelemetryDestinationWorkspacesAll,
        BetaTelemetryDestinationWorkspacesInclude,
        BetaTelemetryDestinationWorkspacesExclude,
    ],
    UnionDiscriminator("type"),
]
"""Which of the organization's workspaces a telemetry destination covers.

Several destinations can cover the same workspace. Each of them receives the workspace's spans while it is enabled.

The workspace list of an `include` or `exclude` destination isn't part of the destination object. List the destination's workspaces to read it. Add or remove one workspace at a time, or replace the whole list with an update. A list holds at most 1,000 workspaces.
"""
