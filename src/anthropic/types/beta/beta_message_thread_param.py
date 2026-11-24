from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_thread_create_params import BetaThreadCreateParams
from .beta_thread_continue_params import BetaThreadContinueParams

__all__ = ["BetaMessageThreadParam"]

BetaMessageThreadParam: TypeAlias = Union[BetaThreadCreateParams, BetaThreadContinueParams]
"""Server-held conversation state (a Thread).

`{"type": "create"}` asks the server to hold this conversation's state under the response's `id`; `{"type": "continue", "previous_message_id": ...}` resumes from a previous response so only the new turn's messages are sent. The response shape is unchanged.
"""
