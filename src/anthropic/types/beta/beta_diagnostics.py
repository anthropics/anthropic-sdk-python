# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_cache_miss_unavailable import BetaCacheMissUnavailable
from .beta_cache_miss_model_changed import BetaCacheMissModelChanged
from .beta_cache_miss_tools_changed import BetaCacheMissToolsChanged
from .beta_cache_miss_system_changed import BetaCacheMissSystemChanged
from .beta_cache_miss_messages_changed import BetaCacheMissMessagesChanged
from .beta_cache_miss_previous_message_not_found import BetaCacheMissPreviousMessageNotFound

__all__ = ["BetaDiagnostics", "CacheMissReason"]

CacheMissReason: TypeAlias = Annotated[
    Union[
        BetaCacheMissModelChanged,
        BetaCacheMissSystemChanged,
        BetaCacheMissToolsChanged,
        BetaCacheMissMessagesChanged,
        BetaCacheMissPreviousMessageNotFound,
        BetaCacheMissUnavailable,
        None,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaDiagnostics(BaseModel):
    """Response envelope for request-level diagnostics.

    Present (possibly
    null) whenever the caller supplied `diagnostics` on the request.
    """

    cache_miss_reason: Optional[CacheMissReason] = None
    """
    Explains why the prompt cache could not fully reuse the prefix from the request
    identified by `diagnostics.previous_message_id`. `null` means diagnosis is still
    pending — the response was serialized before the background comparison
    completed.
    """
