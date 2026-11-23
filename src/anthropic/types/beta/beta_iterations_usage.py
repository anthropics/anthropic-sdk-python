from typing import List, Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_message_iteration_usage import BetaMessageIterationUsage
from .beta_compaction_iteration_usage import BetaCompactionIterationUsage
from .beta_advisor_message_iteration_usage import BetaAdvisorMessageIterationUsage
from .beta_fallback_message_iteration_usage import BetaFallbackMessageIterationUsage

__all__ = ["BetaIterationsUsage", "BetaIterationsUsageItem"]

BetaIterationsUsageItem: TypeAlias = Annotated[
    Union[
        BetaMessageIterationUsage,
        BetaCompactionIterationUsage,
        BetaAdvisorMessageIterationUsage,
        BetaFallbackMessageIterationUsage,
    ],
    UnionDiscriminator("type"),
]

BetaIterationsUsage: TypeAlias = List[BetaIterationsUsageItem]
"""Per-iteration token usage breakdown.

Each entry represents one sampling iteration, with its own input/output token counts and cache statistics, discriminated by `type`. For `message` entries (model sampling iterations, such as the turns of a server-side tool use loop), this allows you to:
- Calculate the context window size from the last `message` entry
- Understand token accumulation across server-side tool use loops

A `compaction` entry reports the token usage of the compaction operation itself — the server-side request that summarizes the context being closed — NOT the size of the context that was compacted away, and its token counts can be much smaller than that closed context (for example, a compaction that closes a ~200k-token context can report only a few thousand tokens). Do not derive the context window size from a `compaction` entry, even when it is the last entry. A `compaction` entry's tokens are not included in the top-level `usage` fields. When an input-token trigger is in effect (the default — 150,000 tokens unless configured otherwise), each `compaction` entry closes a context that had reached at least that threshold, though the context can exceed it by the final iteration's output and tool results.
"""
