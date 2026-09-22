from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaCacheControlEphemeral"]


class BetaCacheControlEphemeral(BaseModel):
    type: Literal["ephemeral"]

    ttl: Optional[Literal["5m", "1h"]] = None
    """The time-to-live for the cache control breakpoint.

    This may be one the following values:

    - `5m`: 5 minutes
    - `1h`: 1 hour

    Defaults to `5m`. See
    [prompt caching pricing](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
    for details.
    """
