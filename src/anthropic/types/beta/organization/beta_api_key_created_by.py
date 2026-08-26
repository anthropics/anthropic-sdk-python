# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAPIKeyCreatedBy"]


class BetaAPIKeyCreatedBy(BaseModel):
    id: str
    """ID of the actor that created the object."""

    type: Literal["service_account", "user"]
    """Type of the actor that created the object."""
