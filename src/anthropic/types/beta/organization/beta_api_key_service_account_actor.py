# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAPIKeyServiceAccountActor"]


class BetaAPIKeyServiceAccountActor(BaseModel):
    service_account_id: str
    """ID of the Service Account the API key acts as."""

    type: Literal["service_account_actor"]
    """Principal type. Always `"service_account_actor"` for a Service Account."""
