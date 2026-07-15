# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryPrefix"]


class BetaManagedAgentsMemoryPrefix(BaseModel):
    """
    A rolled-up directory marker returned by [List memories](/en/api/beta/memory_stores/memories/list) when `depth` is set. Indicates that one or more memories exist deeper than the requested depth under this prefix. This is a list-time rollup, not a stored resource; it has no ID and no lifecycle. Each prefix counts toward the page `limit` and interleaves with `memory` items in path order.
    """

    path: str
    """The rolled-up path prefix, including a trailing `/` (e.g.

    `/projects/foo/`). Pass this value as `path_prefix` on a subsequent list call to
    drill into the directory.
    """

    type: Literal["memory_prefix"]
