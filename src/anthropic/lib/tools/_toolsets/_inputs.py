"""The member input models: what the model sends a browser toolset member.

Member names and input models are read off the generated `tool_use` union
(`anthropic.types.beta.BetaResponseBrowserToolUseBlock`), one variant per member. The union
of the input models is the generated `anthropic.types.beta.BetaBrowserMemberInput`.

Importing this module raises if the generated `anthropic.types.beta.BetaBrowserMemberName` and the generated union
list different names.
"""

from __future__ import annotations

from typing import cast
from typing_extensions import get_args

from ._base import members_from_union
from ....types.beta import BetaBrowserMemberName, BetaBrowserMemberInput, BetaResponseBrowserToolUseBlock

__all__ = ["BROWSER_MEMBER_NAMES", "BROWSER_INPUT_TYPES"]


DERIVED = cast(
    "list[tuple[BetaBrowserMemberName, type[BetaBrowserMemberInput]]]",
    members_from_union(BetaResponseBrowserToolUseBlock, {}),
)
"""Every browser member has a generated input model, so no stand-in is needed."""

BROWSER_INPUT_TYPES: dict[str, type[BetaBrowserMemberInput]] = dict(DERIVED)
"""Member name → the model its `tool_use.input` is parsed into, derived from the generated union."""


BROWSER_MEMBER_NAMES: list[BetaBrowserMemberName] = [name for name, _ in DERIVED]
"""Member names, in the generated union's order."""

if set(BROWSER_MEMBER_NAMES) != set(get_args(BetaBrowserMemberName)):  # pragma: no cover
    raise AssertionError("BetaBrowserMemberName is out of step with the generated browser tool_use union")
