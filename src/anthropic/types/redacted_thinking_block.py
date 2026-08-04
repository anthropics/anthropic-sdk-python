# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RedactedThinkingBlock"]


class RedactedThinkingBlock(BaseModel):
    data: str
    """
    The contents of this redacted thinking block, returned when portions of the
    model's thinking were safety-redacted. This field is opaque and encrypted, with
    no readable content.

    Pass `redacted_thinking` blocks back to the API unchanged when continuing a
    multi-turn conversation.

    See
    [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#redacted-thinking-blocks)
    for details.
    """

    type: Literal["redacted_thinking"]
