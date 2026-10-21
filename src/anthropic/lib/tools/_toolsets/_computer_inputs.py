"""The member input models: what the model sends a computer toolset member.

Member names and input models are read off the generated `tool_use` union
(`anthropic.types.beta.BetaResponseComputerToolUseBlock`), one variant per member. The union of the input models
is the generated `anthropic.types.beta.BetaComputerMemberInput`, and the member names are the generated
`anthropic.types.beta.BetaComputerMemberName`.
"""

from __future__ import annotations

from typing import cast

from ._base import members_from_union
from ....types.beta import (
    BetaComputerMemberName,
    BetaComputerMemberInput,
    BetaComputerScreenshotInput,
    BetaComputerLeftMouseUpInput,
    BetaComputerLeftMouseDownInput,
    BetaComputerCursorPositionInput,
    BetaResponseComputerToolUseBlock,
)

__all__ = [
    "COMPUTER_MEMBER_NAMES",
    "COMPUTER_INPUT_TYPES",
    "BetaComputerMemberName",
    "BetaComputerMemberInput",
    "BetaComputerCursorPositionInput",
    "BetaComputerLeftMouseDownInput",
    "BetaComputerLeftMouseUpInput",
    "BetaComputerScreenshotInput",
]


DERIVED = cast(
    "list[tuple[BetaComputerMemberName, type[BetaComputerMemberInput]]]",
    members_from_union(BetaResponseComputerToolUseBlock, {}),
)

COMPUTER_INPUT_TYPES: dict[str, type[BetaComputerMemberInput]] = dict(DERIVED)
"""Member name → the model its `tool_use.input` is parsed into, derived from the generated union."""

COMPUTER_MEMBER_NAMES: list[BetaComputerMemberName] = [name for name, _ in DERIVED]
"""Member names, in the generated union's order."""
