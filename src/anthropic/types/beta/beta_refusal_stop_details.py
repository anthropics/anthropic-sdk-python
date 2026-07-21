# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaRefusalStopDetails"]


class BetaRefusalStopDetails(BaseModel):
    """Structured information about a refusal."""

    category: Optional[Literal["cyber", "bio", "frontier_llm", "reasoning_extraction", "general_harms"]] = None
    """The policy category that triggered a refusal.

    - `cyber` - The request could enable cyber harm, such as malware or exploit
      development. Benign cybersecurity work can also trigger this category.
    - `bio` - The request could enable biological harm, such as dangerous lab
      methods. Beneficial life sciences work can also trigger this category.
    - `frontier_llm` - The request could assist the development of competing AI
      models, which is restricted under
      [Anthropic's commercial terms](https://www.anthropic.com/legal/commercial-terms).
      Benign machine learning work can also trigger this category.
    - `reasoning_extraction` - The request asks the model to reproduce its internal
      reasoning in the response text. To get reasoning in a structured form instead,
      use
      [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking).
    - `general_harms` - The request could be related to an area that was determined
      as harmful. Benign work might sometimes trigger this category.
    """

    explanation: Optional[str] = None
    """Human-readable explanation of the refusal.

    This text is not guaranteed to be stable. `null` when no explanation is
    available for the category.
    """

    fallback_credit_token: Optional[str] = None
    """
    Opaque code that refunds the cache-miss cost when retrying this refused request
    on the fallback model. Pass it as `fallback_credit_token` on the retry request.
    Expires 5 minutes after the refusal.

    The retry is sent either with the same request body (`system`, `messages`,
    `tools`, and other render-shaping fields), or with the same body plus one
    appended `assistant` message whose content is the partial text (with any
    trailing whitespace stripped from the final text block) and paired server-tool
    blocks from this refusal — which also authorizes that appended turn as an
    assistant-prefill continuation on models that otherwise disallow prefill. A
    token minted mid-server-tool-loop whose partial content was continuable may only
    be redeemed the second way — if a same-body retry is rejected with a 400 saying
    the token must be redeemed by continuing the partial response, retry the second
    way instead. Either way: same workspace, same platform; a mismatch is a 400.
    Resending a token for an already-warm prefix is permitted but yields no
    additional credit.

    `null` when the refused model isn't eligible for a fallback credit.
    """

    fallback_has_prefill_claim: Optional[bool] = None
    """
    Whether the accompanying `fallback_credit_token` may be redeemed with the
    appended-assistant retry form. Only set when `fallback_credit_token` is present.

    `true`: retry by resending the same request body plus one appended `assistant`
    message whose content is this response's `content` with any trailing whitespace
    stripped from the final text block and unpaired `tool_use` blocks omitted (the
    same appended-turn shape described on `fallback_credit_token`), with the token
    attached. `false`: retry by resending the original request body unchanged, with
    the token attached — the appended-assistant form is not available for this
    refusal (no continuable partial content, or the request uses `output_format` or
    a `tool_choice` that forces tool use). One exception: when the request used
    `output_format` or a forced `tool_choice` and the refusal arrived after server
    tools (including MCP connector tools) had already executed, the token may not be
    redeemable by either retry form; if the exact-body retry is then rejected with a
    400 saying the token must be redeemed by continuing the partial response,
    discard the token and retry without it.

    Advisory: if an appended-assistant retry is rejected with a 400 despite `true`,
    fall back to resending the original request body with the token.
    """

    recommended_model: Optional[str] = None
    """The server's suggested retry target for this refusal.

    Populated when a fallback attempt could not be made (the fallback model's rate
    limit was exhausted, or it was overloaded); names the fallback model the caller
    can retry directly. Null otherwise.
    """

    type: Literal["refusal"]
