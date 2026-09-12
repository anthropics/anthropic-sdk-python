from typing_extensions import Literal, TypeAlias

__all__ = ["BetaThinkingPrefixMismatchBehavior"]

BetaThinkingPrefixMismatchBehavior: TypeAlias = Literal["error", "drop_block"]
