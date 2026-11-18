from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ThreadNotFoundErrorDetails"]


class ThreadNotFoundErrorDetails(BaseModel):
    """No usable Thread state was found for `previous_message_id`.

    Replay the full conversation with `thread: {"type": "create"}` to start a new Thread.
    """

    error_code: Literal["thread_not_found"]
