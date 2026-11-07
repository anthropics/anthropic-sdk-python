from ...._models import BaseModel

__all__ = ["BetaPluginMarketplaceValidationPluginError"]


class BetaPluginMarketplaceValidationPluginError(BaseModel):
    error: str
    """Why the plugin would be skipped by a synchronization."""

    error_code: str
    """A stable identifier for the reason — the value to branch on."""

    name: str
    """The plugin's name, as its entry in marketplace.json declares it."""
