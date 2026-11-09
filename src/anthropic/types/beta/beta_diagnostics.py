from typing import Optional

from ..._models import BaseModel
from .beta_cache_miss_reason import BetaCacheMissReason

__all__ = ["BetaDiagnostics"]


class BetaDiagnostics(BaseModel):
    """
    Request-level diagnostics: why the prompt cache could not fully reuse
    the prefix of the request named by `diagnostics.previous_message_id`.
    """

    cache_miss_reason: Optional[BetaCacheMissReason] = None
    """
    Explains why the prompt cache could not fully reuse the prefix from the request
    identified by `diagnostics.previous_message_id`. `null` means diagnosis is still
    pending — the response was serialized before the background comparison
    completed.
    """
