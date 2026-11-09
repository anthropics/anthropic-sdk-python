from typing import List, Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_plugin_marketplace_validation_plugin_error import BetaPluginMarketplaceValidationPluginError
from .beta_plugin_marketplace_validation_plugin_warnings import BetaPluginMarketplaceValidationPluginWarnings

__all__ = ["BetaPluginMarketplaceValidationReport"]


class BetaPluginMarketplaceValidationReport(BaseModel):
    """
    The outcome of validating plugin marketplace content: a report, not a
    stored object, so nothing in it can be retrieved afterwards.
    """

    commit_sha: Optional[str] = None
    """
    The full SHA of the commit that was validated: for a repository, the commit that
    was read; for an uploaded archive, the commit recorded in the archive's comment
    (as a Git host's download writes it; not verified), else null.
    """

    manifest_error: Optional[str] = None
    """
    Set when nothing could be validated: the repository or archive could not be
    read, or marketplace.json is missing, malformed or over a limit. Null otherwise.
    """

    manifest_error_code: Optional[str] = None
    """A stable identifier for `manifest_error`; null when that is."""

    plugin_errors: List[BetaPluginMarketplaceValidationPluginError]
    """
    One entry per plugin a synchronization would skip entirely, keyed by the
    plugin's name in marketplace.json.
    """

    plugin_warnings: List[BetaPluginMarketplaceValidationPluginWarnings]
    """
    One entry per plugin that would synchronize with some of its contents left out,
    keyed by the plugin's name in marketplace.json.
    """

    ref: Optional[str] = None
    """
    For a repository, the branch that was read by name: the one requested, or else
    the branch a synchronization of this repository is set to read. Null when no
    branch is named or set and the repository's default branch was read, for a
    request by commit SHA, and for an uploaded archive.
    """

    total_plugin_count: int
    """How many plugins marketplace.json declares; 0 when it could not be read."""

    type: Literal["plugin_marketplace_validation_report"]
    """Always `plugin_marketplace_validation_report`."""

    valid: bool
    """
    True when marketplace.json is well-formed and no plugin would be skipped;
    warnings never make it false.
    """
