from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaThinkingMismatchAllowedInputTransformation"]


class BetaThinkingMismatchAllowedInputTransformation(BaseModel):
    path: str
    """
    Where the block is in your request, as `messages.{i}.content.{j}`: `i` indexes
    the `messages` array you sent and `j` that message's `content` array — the same
    form error messages use.
    """

    reason: Literal[
        "model_binding_mismatch",
        "prefix_binding_mismatch",
        "organization_binding_mismatch",
        "end_user_binding_mismatch",
    ]
    """
    Which binding check the block failed; the block was shown to the model all the
    same. Always `prefix_binding_mismatch` today — the conversation before the block
    differs from the conversation it was created in, or the block carries no record
    of one on a model that requires it. Were the check enforced for this request,
    the block would have been removed or the request rejected
    (`thinking.block_binding.prefix_mismatch_behavior`). A removal also takes the
    rest of that turn's consecutive thinking blocks, whereas here each block is
    checked on its own, so `thinking_mismatch_allowed` entries are a lower bound on
    what enforcement would remove.
    """

    type: Literal["thinking_mismatch_allowed"]
    """Always `thinking_mismatch_allowed` for this entry type."""
