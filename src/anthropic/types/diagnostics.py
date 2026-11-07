from typing import Optional

from .._models import BaseModel
from .cache_miss_reason import CacheMissReason

__all__ = ["Diagnostics"]


class Diagnostics(BaseModel):
    """
    Request-level diagnostics: why the prompt cache could not fully reuse
    the prefix of the request named by `diagnostics.previous_message_id`.
    """

    cache_miss_reason: Optional[CacheMissReason] = None
    """
    Explains why the prompt cache could not fully reuse the prefix from the request
    identified by `diagnostics.previous_message_id`. `null` means diagnosis is still
    pending — the response was serialized before the background comparison
    completed.
    """
