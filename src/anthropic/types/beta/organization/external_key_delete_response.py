# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ExternalKeyDeleteResponse"]


class ExternalKeyDeleteResponse(BaseModel):
    id: str
    """ID of the deleted External Key."""

    type: Literal["external_key_deleted"]
