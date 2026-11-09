from typing_extensions import Literal

from .._exceptions import BadRequestError
from .thread_already_continued_error_details import ThreadAlreadyContinuedErrorDetails

__all__ = ["ThreadAlreadyContinuedError"]


class ThreadAlreadyContinuedError(BadRequestError):
    """
    The response that `previous_message_id` names has already been continued, and each response can be continued only once. Continue from the Thread's most recent response `id`.
    """

    error_code: Literal["thread_already_continued"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ThreadAlreadyContinuedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
