# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAPIActor"]


class BetaManagedAgentsAPIActor(BaseModel):
    """
    Attribution for a write made directly via the public API (outside of any session).
    """

    api_key_id: str
    """ID of the API key that performed the write.

    This identifies the key, not the secret.
    """

    type: Literal["api_actor"]
