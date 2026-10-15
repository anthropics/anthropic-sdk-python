from ..._models import BaseModel

__all__ = ["BetaDreamError"]


class BetaDreamError(BaseModel):
    """Failure detail for a Dream whose `status` is `failed`."""

    message: str
    """A human-readable explanation of why the dream failed."""

    type: str
    """A code for why the dream failed, such as `timeout` or `internal_error`.

    The
    [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#errors)
    lists common error codes and when they occur.
    """
