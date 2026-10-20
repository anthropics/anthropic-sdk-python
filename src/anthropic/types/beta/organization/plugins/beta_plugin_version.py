from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ....._models import BaseModel, UnionDiscriminator
from ..beta_plugin_api_actor import BetaPluginAPIActor
from ..beta_plugin_component import BetaPluginComponent
from ..beta_plugin_user_actor import BetaPluginUserActor
from ..beta_plugin_content_scan import BetaPluginContentScan

__all__ = ["BetaPluginVersion", "CreatedBy"]

CreatedBy: TypeAlias = Annotated[Union[BetaPluginUserActor, BetaPluginAPIActor, None], UnionDiscriminator("type")]


class BetaPluginVersion(BaseModel):
    id: str
    """The version's ID."""

    components: Optional[List[BetaPluginComponent]] = None
    """What the version contains; null when not enumerated."""

    content_scan: Optional[BetaPluginContentScan] = None
    """This version's content scan; null when it has not been scanned."""

    created_at: datetime
    """RFC 3339."""

    created_by: Optional[CreatedBy] = None
    """Who uploaded this version; null when not recorded."""

    description: Optional[str] = None
    """The manifest's description; null when it declares none."""

    display_name: Optional[str] = None
    """The manifest's display name; null when it declares none."""

    manifest_version: Optional[str] = None
    """
    The manifest's `version`, normalized for display: one leading `v` or `V` is
    dropped, and the result is returned only if it is 1 to 64 characters, starts
    with a digit, and uses only ASCII letters, digits, `.`, `+`, and `-`; otherwise
    `null`. For example, `"v1.4.0"` is returned as `"1.4.0"`, and `"latest"` as
    `null`. For a synchronized plugin, the `version` of its `marketplace.json` entry
    can take the place of the manifest's `version`. It is also `null` for a version
    stored before claude.ai began recording this field (August 2026).
    """

    plugin_id: str
    """The Plugin's ID."""

    reach: Optional[Literal["contained", "privileged", "remote"]] = None
    """
    How far the version reaches: `remote`, `privileged`, `contained`, or `null`, as
    defined on the Plugin's `reach`.
    """

    release_notes: Optional[str] = None
    """As supplied with the upload; null when none were supplied."""

    type: Literal["plugin_version"]
    """Always `plugin_version`."""
