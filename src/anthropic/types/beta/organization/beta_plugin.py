from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_plugin_api_actor import BetaPluginAPIActor
from .beta_plugin_component import BetaPluginComponent
from .beta_plugin_owner_user import BetaPluginOwnerUser
from .beta_plugin_user_actor import BetaPluginUserActor
from .beta_plugin_content_scan import BetaPluginContentScan
from .beta_plugin_owner_organization import BetaPluginOwnerOrganization

__all__ = ["BetaPlugin", "CreatedBy", "Owner"]

CreatedBy: TypeAlias = Annotated[Union[BetaPluginUserActor, BetaPluginAPIActor, None], UnionDiscriminator("type")]

Owner: TypeAlias = Annotated[Union[BetaPluginOwnerOrganization, BetaPluginOwnerUser], UnionDiscriminator("type")]


class BetaPlugin(BaseModel):
    id: str
    """The Plugin's ID."""

    components: Optional[List[BetaPluginComponent]] = None
    """What the served version contains; null when not enumerated."""

    content_scan: Optional[BetaPluginContentScan] = None
    """The served version's content scan; null when it has not been scanned."""

    created_at: datetime
    """RFC 3339."""

    created_by: Optional[CreatedBy] = None
    """Who created the Plugin; null when no creator is recorded."""

    description: Optional[str] = None
    """The served version's description."""

    display_name: Optional[str] = None
    """The served version's display name."""

    latest_version_id: str
    """The newest version."""

    manifest_version: Optional[str] = None
    """
    The served version's manifest `version`, normalized for display, or `null` (the
    Plugin Version's `manifest_version` says how and when).
    """

    marketplace_id: str
    """The ID of the plugin marketplace the Plugin lives in."""

    name: str
    """Lowercase identifier, unique within its plugin marketplace.

    Fixed for an organization-owned Plugin's lifetime; a member-owned Plugin's
    changes when its owner renames it in claude.ai, while its `id` stays the same.
    """

    organization_installation_preference: Optional[
        Literal["auto_install", "available", "not_available", "required"]
    ] = None
    """
    Organization-owned Plugin: the organization-wide installation setting every
    member gets unless an RBAC Group they belong to holds its own — the Plugin's own
    setting, or its plugin marketplace's default. Null for a member-owned Plugin,
    which has shares instead. One of `required`, `auto_install`, `available`,
    `not_available`; a value this API does not yet name is returned as stored.
    """

    organization_installation_preference_inherited: Optional[bool] = None
    """
    Organization-owned Plugin: true while it has no organization-wide setting of its
    own and `organization_installation_preference` is its plugin marketplace's
    default. Null for a member-owned Plugin.
    """

    owner: Owner
    """
    Who owns the Plugin: the organization, or the member whose personal plugin
    marketplace it lives in.
    """

    reach: Optional[Literal["contained", "privileged", "remote"]] = None
    """How far the served version reaches, or `null` if it is not classified.

    `remote` means it declares an MCP server or a CLI. `privileged` means it
    declares no MCP server or CLI, but declares a hook, monitor, language server, or
    settings, or has a skill, command, or other Markdown file whose frontmatter
    pre-approves tools (`allowed-tools` with any value other than an empty one or
    one that names only `AskUserQuestion`, `TodoWrite`, and `ToolSearch`). Otherwise
    it is `contained`.

    If the frontmatter of a skill, command, or other Markdown file that could change
    the value could not be read, or was past a size limit, the version is `null` or
    `privileged` (or `remote`, if it declares an MCP server or a CLI), not
    `contained`. The value is normally worked out when a version is stored, under
    the rules of that time, so an older version can be `null`, or `contained` where
    the same files stored today would be `privileged` or `null`.
    """

    served_version_id: str
    """The version claude.ai serves to members."""

    served_version_pinned: bool
    """
    True once the served version has been pinned, through Update Plugin or in
    claude.ai. While false, a new version normally becomes the served version when
    it is stored. While the newest version is not the served version, as when a
    version saved in claude.ai is waiting for its content scan, `served_version_id`
    differs from `latest_version_id`.
    """

    type: Literal["plugin"]
    """Always `plugin`."""

    updated_at: datetime
    """RFC 3339.

    Moves on a served-version change (including pinning an unpinned Plugin to the
    version it already serves) and, normally, on a new version. A version saved in
    claude.ai that waits for its content scan moves it when it becomes the served
    version, and not necessarily when it is stored. A change to the Plugin's
    installation settings or shares does not move it.
    """
