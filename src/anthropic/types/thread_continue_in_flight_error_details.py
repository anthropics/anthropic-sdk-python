from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ThreadContinueInFlightErrorDetails"]


class ThreadContinueInFlightErrorDetails(BaseModel):
    """Another request is still continuing from the same `previous_message_id`.

    Wait for it to complete and continue from its response `id`, or replay the full conversation with `thread: {"type": "create"}`.
    """

    error_code: Literal["thread_continue_in_flight"]
