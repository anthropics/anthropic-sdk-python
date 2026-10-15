from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAPIActor"]


class BetaManagedAgentsAPIActor(BaseModel):
    """
    A direct caller of the public API, identified by the API key that authenticated the request.
    """

    api_key_id: str
    """ID of the API key (an `apikey_...` value).

    This identifies the key, not the secret.
    """

    type: Literal["api_actor"]
