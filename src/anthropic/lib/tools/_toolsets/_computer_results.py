"""What a computer toolset member returns, and the types of its `confirm` hook.

A computer member returns an image, a cursor position, a line of text, or nothing; the two result models are declared
here, with the types of the `confirm` hook.
"""

from __future__ import annotations

from typing import Union, Callable, Awaitable
from typing_extensions import TypeAlias

from ._base import BetaScreenshotResult
from ._runnable import BetaToolsetCallContext
from ...._models import BaseModel
from ._computer_inputs import BetaComputerMemberName, BetaComputerMemberInput

__all__ = [
    "BetaComputerCursorPositionResult",
    "BetaComputerMemberResult",
    "BetaComputerConfirmContext",
    "BetaComputerConfirmCallable",
    "BetaAsyncComputerConfirmCallable",
]


class BetaComputerCursorPositionResult(BaseModel):
    """Where the cursor is, in screenshot pixels; rendered as `X={x},Y={y}`."""

    x: int
    y: int


BetaComputerMemberResult: TypeAlias = Union[BetaScreenshotResult, BetaComputerCursorPositionResult, str, None]
"""Anything a computer member may return: `execute`'s un-narrowed result type."""


class BetaComputerConfirmContext(BetaToolsetCallContext):
    """What the `confirm` callable is told about the call awaiting approval: the member and its parsed input, and
    the `tool_use` block being answered."""

    member: BetaComputerMemberName
    input: BetaComputerMemberInput


BetaComputerConfirmCallable: TypeAlias = Callable[[BetaComputerConfirmContext], bool]
BetaAsyncComputerConfirmCallable: TypeAlias = Callable[[BetaComputerConfirmContext], Union[bool, Awaitable[bool]]]
