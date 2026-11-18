from typing_extensions import Literal

from .._exceptions import BadRequestError
from .thread_fingerprint_mismatch_error_details import ThreadFingerprintMismatchErrorDetails

__all__ = ["ThreadFingerprintMismatchError"]


class ThreadFingerprintMismatchError(BadRequestError):
    """
    A field that must stay the same across a Thread's turns differs from the value stored with the Thread; the message names each such field. Send the stored values, or replay the full conversation with `thread: {"type": "create"}` to change them.
    """

    error_code: Literal["thread_fingerprint_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ThreadFingerprintMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
