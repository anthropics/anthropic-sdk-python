# File generated from our OpenAPI spec by Stainless.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["MessageDeltaEvent", "Delta"]


class Delta(BaseModel):
    stop_reason: Optional[Literal["end_turn", "max_tokens", "stop_sequence"]] = None

    stop_sequence: Optional[str] = None


class MessageDeltaEvent(BaseModel):
    delta: Delta

    type: Literal["message_delta"]
