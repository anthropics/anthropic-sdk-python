from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ThreadFingerprintMismatchErrorDetails"]


class ThreadFingerprintMismatchErrorDetails(BaseModel):
    """
    A field that must stay the same across a Thread's turns differs from the value stored with the Thread; the message names each such field. Send the stored values, or replay the full conversation with `thread: {"type": "create"}` to change them.
    """

    error_code: Literal["thread_fingerprint_mismatch"]
