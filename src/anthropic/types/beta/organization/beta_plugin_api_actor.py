from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginAPIActor"]


class BetaPluginAPIActor(BaseModel):
    api_key_id: str
    """The key's ID."""

    type: Literal["api_actor"]
    """
    An Admin API key, in the same form the Compliance API activity feed uses for it.
    """
