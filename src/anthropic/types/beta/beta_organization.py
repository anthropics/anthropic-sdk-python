# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaOrganization"]


class BetaOrganization(BaseModel):
    id: str
    """ID of the Organization."""

    name: str
    """Name of the Organization."""

    type: Literal["organization"]
    """Object type.

    For Organizations, this is always `"organization"`.
    """
