from ..._models import BaseModel

__all__ = ["BetaDreamUsage"]


class BetaDreamUsage(BaseModel):
    """The tokens that a dream has used so far.

    The counts are zero while the dream is `pending` and update while it is `running`. They can keep changing after a cancel.

    See the [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#billing) for how dreams are billed. See the [prompt caching guide](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#tracking-cache-performance) for how the input token counts add up.
    """

    cache_creation_input_tokens: int
    """
    The dream's input tokens that were written to the prompt cache, for both the
    5-minute and 1-hour cache durations.
    """

    cache_read_input_tokens: int
    """The dream's input tokens that were read from the prompt cache."""

    input_tokens: int
    """The dream's input tokens that weren't read from or written to the prompt cache."""

    output_tokens: int
    """The tokens that the model generated for the dream."""
