from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CacheMissToolsChanged"]


class CacheMissToolsChanged(BaseModel):
    """
    A `cache_miss_reason` for a request whose `tools` differ from the previous request's, for example because tools were added, removed, or reordered.

    See the [cache diagnostics guide](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics#cache-miss-reason-types) to learn what to change for each reason.
    """

    cache_missed_input_tokens: int
    """
    Approximate number of input tokens that would have been read from cache had the
    prefix matched the previous request.
    """

    type: Literal["tools_changed"]
