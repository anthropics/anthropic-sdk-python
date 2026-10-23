from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsAPIActor"]


class BetaAnalyticsAPIActor(BaseModel):
    api_key_id: str
    """Tagged API key ID."""

    type: Literal["api_actor"]
