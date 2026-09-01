# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaThinkingDroppedInputTransformation"]


class BetaThinkingDroppedInputTransformation(BaseModel):
    path: str
    """
    Where the removed block was in your request, as `messages.{i}.content.{j}`: `i`
    indexes the `messages` array you sent and `j` that message's `content` array —
    the same form error messages use.
    """

    reason: Literal[
        "model_binding_mismatch",
        "prefix_binding_mismatch",
        "organization_binding_mismatch",
        "end_user_binding_mismatch",
    ]
    """
    Which binding check removed the block: `model_binding_mismatch` — it was created
    by a model whose reasoning the requested model may not read;
    `prefix_binding_mismatch` — the conversation before it differs from the
    conversation it was created in (the rest of that turn's consecutive thinking
    blocks are removed with it, each with this reason);
    `organization_binding_mismatch` — it was created under a different organization
    (an Anthropic organization, AWS account or Google Cloud project) and this
    organization is not one of its additional organizations;
    `end_user_binding_mismatch` — it was created for a different end user, or was
    removed by the consumer-organization binding. A block that would fail several
    checks reports one reason, in this order of precedence:
    `organization_binding_mismatch`, `end_user_binding_mismatch`,
    `model_binding_mismatch`, `prefix_binding_mismatch`.
    """

    type: Literal["thinking_dropped"]
    """Always `thinking_dropped` for this entry type."""
