from typing import Dict, List
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaJWKSInline"]


class BetaJWKSInline(BaseModel):
    """JWKS supplied directly; no network fetch."""

    keys: List[Dict[str, object]]
    """Inline JWK objects."""

    type: Literal["inline"]
