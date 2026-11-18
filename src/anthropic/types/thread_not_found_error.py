from typing_extensions import Literal

from .._exceptions import NotFoundError
from .thread_not_found_error_details import ThreadNotFoundErrorDetails

__all__ = ["ThreadNotFoundError"]


class ThreadNotFoundError(NotFoundError):
    """No usable Thread state was found for `previous_message_id`.

    Replay the full conversation with `thread: {"type": "create"}` to start a new Thread.
    """

    error_code: Literal["thread_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ThreadNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
