from typing_extensions import Literal

from .._exceptions import BadRequestError
from .thread_continue_in_flight_error_details import ThreadContinueInFlightErrorDetails

__all__ = ["ThreadContinueInFlightError"]


class ThreadContinueInFlightError(BadRequestError):
    """Another request is still continuing from the same `previous_message_id`.

    Wait for it to complete and continue from its response `id`, or replay the full conversation with `thread: {"type": "create"}`.
    """

    error_code: Literal["thread_continue_in_flight"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ThreadContinueInFlightErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
