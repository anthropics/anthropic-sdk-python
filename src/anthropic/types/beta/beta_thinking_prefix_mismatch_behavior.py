from typing_extensions import Literal, TypeAlias

__all__ = ["BetaThinkingPrefixMismatchBehavior"]

BetaThinkingPrefixMismatchBehavior: TypeAlias = Literal["error", "drop_block"]
"""
What happens when a thinking block in `messages` fails the conversation
check: it was created in a different conversation, or the messages before
it have changed since. `"error"` (the default) fails the request with a
400 error. `"drop_block"` removes the failing blocks and the request
proceeds; the model no longer sees the dropped reasoning.
"""
