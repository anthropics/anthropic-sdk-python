from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["APIKeyCreatedBy"]


class APIKeyCreatedBy(BaseModel):
    id: str
    """ID of the actor that created the object."""

    type: Literal["service_account", "user"]
    """Type of the actor that created the object."""
