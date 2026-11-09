from typing import List

from ...._models import BaseModel
from .beta_plugin_marketplace_validation_plugin_warning import BetaPluginMarketplaceValidationPluginWarning

__all__ = ["BetaPluginMarketplaceValidationPluginWarnings"]


class BetaPluginMarketplaceValidationPluginWarnings(BaseModel):
    name: str
    """The plugin's name, as its entry in marketplace.json declares it."""

    warnings: List[BetaPluginMarketplaceValidationPluginWarning]
    """The parts of the plugin a synchronization would leave out."""
