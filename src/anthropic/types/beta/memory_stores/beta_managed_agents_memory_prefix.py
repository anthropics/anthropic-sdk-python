from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryPrefix"]


class BetaManagedAgentsMemoryPrefix(BaseModel):
    """
    A directory marker that [List Memories](https://platform.claude.com/docs/en/api/beta/memory_stores/memories/list) returns instead of the memories below the requested `depth`.

    It stands for one or more memories whose paths start with `path`. It isn't a stored object and doesn't have an ID. Each marker counts toward the page `limit`.
    """

    path: str
    """The rolled-up path prefix, including a trailing `/` (e.g.

    `/projects/foo/`). Pass this value as `path_prefix` on a subsequent list call to
    drill into the directory.
    """

    type: Literal["memory_prefix"]
