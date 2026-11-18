from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ThreadAlreadyContinuedErrorDetails"]


class ThreadAlreadyContinuedErrorDetails(BaseModel):
    """
    The response that `previous_message_id` names has already been continued, and each response can be continued only once. Continue from the Thread's most recent response `id`.
    """

    error_code: Literal["thread_already_continued"]
