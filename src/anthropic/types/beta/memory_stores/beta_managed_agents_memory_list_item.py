from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_memory import BetaManagedAgentsMemory
from .beta_managed_agents_memory_prefix import BetaManagedAgentsMemoryPrefix

__all__ = ["BetaManagedAgentsMemoryListItem"]

BetaManagedAgentsMemoryListItem: TypeAlias = Annotated[
    Union[BetaManagedAgentsMemory, BetaManagedAgentsMemoryPrefix], UnionDiscriminator("type")
]
"""
One item in a [List Memories](https://platform.claude.com/docs/en/api/beta/memory_stores/memories/list) response: a `memory`, or a `memory_prefix` marker when `depth` is `1`.
"""
