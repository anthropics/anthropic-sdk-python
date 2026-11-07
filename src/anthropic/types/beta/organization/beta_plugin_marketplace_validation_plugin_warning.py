from ...._models import BaseModel

__all__ = ["BetaPluginMarketplaceValidationPluginWarning"]


class BetaPluginMarketplaceValidationPluginWarning(BaseModel):
    error_code: str
    """A stable identifier for the kind of warning."""

    message: str
    """What would be left out, and why."""
