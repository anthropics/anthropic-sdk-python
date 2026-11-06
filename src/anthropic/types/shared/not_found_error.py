from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["NotFoundError"]


class NotFoundError(BaseModel):
    message: str
    """A human-readable explanation of the error.

    Its wording can change, so don't match on it.
    """

    type: Literal["not_found_error"]
    """The broad category of the error."""
