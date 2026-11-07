from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CacheMissMessagesChanged"]


class CacheMissMessagesChanged(BaseModel):
    """
    A `cache_miss_reason` for a request whose `messages` differ from the previous request's in an earlier entry, instead of only having entries appended. The `model`, `system`, and `tools` match.

    See the [cache diagnostics guide](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics#cache-miss-reason-types) to learn what to change for each reason.
    """

    cache_missed_input_tokens: int
    """
    Approximate number of input tokens that would have been read from cache had the
    prefix matched the previous request.
    """

    type: Literal["messages_changed"]
