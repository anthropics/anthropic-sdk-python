from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaDeletedPlugin"]


class BetaDeletedPlugin(BaseModel):
    id: str
    """The deleted Plugin's ID."""

    type: Literal["plugin_deleted"]
    """Always `plugin_deleted`."""
