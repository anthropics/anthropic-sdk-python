from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_plugin_owner_user import BetaPluginOwnerUser
from .beta_plugin_owner_organization import BetaPluginOwnerOrganization

__all__ = ["BetaPluginMarketplace", "Owner"]

Owner: TypeAlias = Annotated[Union[BetaPluginOwnerOrganization, BetaPluginOwnerUser], UnionDiscriminator("type")]


class BetaPluginMarketplace(BaseModel):
    id: str
    """The plugin marketplace's ID, prefixed `marketplace_`."""

    created_at: datetime
    """RFC 3339."""

    default_installation_preference: Optional[Literal["auto_install", "available", "not_available", "required"]] = None
    """
    Organization plugin marketplace: the organization-wide setting every Plugin in
    it with no setting of its own gets. Null for a member's personal plugin
    marketplace. One of `required`, `auto_install`, `available`, `not_available`; a
    value this API does not yet name is returned as stored.
    """

    last_sync_ended_at: Optional[datetime] = None
    """RFC 3339.

    When the most recent synchronization attempt to finish did so, whatever its
    outcome; for a repository plugin marketplace no synchronization has run on yet,
    when it was created. Null for a plugin marketplace that is not synchronized from
    a repository.
    """

    last_sync_read_sha: Optional[str] = None
    """
    The commit the last synchronization attempt that reached the repository read,
    whether or not its content was then accepted (see `sync_status`); an attempt
    that ends `failed_auth` or `failed_transient` leaves it unchanged. Null until an
    attempt has first read the repository, and for a plugin marketplace that is not
    synchronized from a repository.
    """

    name: str
    """Fixed for the plugin marketplace's lifetime."""

    owner: Owner
    """The organization, or the member whose personal plugin marketplace it is."""

    source: Literal["directory", "github", "gitlab", "manual", "public_git"]
    """
    Where the plugin marketplace's Plugins come from: `manual` when they are
    uploaded; `github`, `gitlab` or `public_git` when they are synchronized from the
    Git repository the owner connected, into which nothing can be uploaded;
    `directory` is Anthropic's own catalog, which this API does not list. A value
    this API does not yet name is returned as stored.
    """

    sync_status: Optional[
        Literal["failed_auth", "failed_content", "failed_limits", "failed_transient", "in_progress", "success"]
    ] = None
    """
    Outcome of the plugin marketplace's most recent synchronization: one of
    `success`, `in_progress`, `failed_content`, `failed_transient`, `failed_auth`,
    `failed_limits`; a value this API does not yet name is returned as stored. Null
    until a synchronization is first attempted — so always for a `manual` plugin
    marketplace.
    """

    type: Literal["plugin_marketplace"]
    """Always `plugin_marketplace`."""
