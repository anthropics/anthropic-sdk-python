from typing_extensions import Literal

from .._exceptions import BadRequestError
from .thread_unsupported_request_error_details import ThreadUnsupportedRequestErrorDetails

__all__ = ["ThreadUnsupportedRequestError"]


class ThreadUnsupportedRequestError(BadRequestError):
    """
    The request combines `thread` with a request field or an organization setting that Threads do not support; `unsupported`, when present, names it. Send the full conversation without `thread`, or change that field.
    """

    error_code: Literal["thread_unsupported_request"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ThreadUnsupportedRequestErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
