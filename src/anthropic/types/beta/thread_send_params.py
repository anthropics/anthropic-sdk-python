from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, TypedDict

from ..._types import Omit, SequenceNotStr
from ...types.beta import message_create_params
from ..model_param import ModelParam
from .beta_metadata_param import BetaMetadataParam
from .beta_fallbacks_param import BetaFallbacksParam
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_text_block_param import BetaTextBlockParam
from .beta_diagnostics_param import BetaDiagnosticsParam
from .beta_tool_choice_param import BetaToolChoiceParam
from .beta_thinking_config_param import BetaThinkingConfigParam
from .beta_compaction_config_param import BetaCompactionConfigParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from .beta_context_management_config_param import BetaContextManagementConfigParam
from .beta_request_mcp_server_url_definition_param import BetaRequestMCPServerURLDefinitionParam

__all__ = ["ThreadSendParams"]


class ThreadSendParams(TypedDict, total=False):
    """The `create()` fields that a thread's `send()`, `parse()` and `stream()` override for one turn, and `update()`
    for all later turns."""

    max_tokens: int | Omit
    """The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter
    only specifies the absolute maximum number of tokens to generate.

    Set to `0` to populate the
    [prompt cache](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pre-warming-the-cache)
    without generating a response.

    Different models have different maximum values for this parameter. See
    [models](https://platform.claude.com/docs/en/about-claude/models/overview) for
    details.
    """

    model: ModelParam | Omit
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    cache_control: Optional[BetaCacheControlEphemeralParam] | Omit
    """
    Top-level cache control automatically applies a cache_control marker to the last
    cacheable block in the request.
    """

    compaction: Optional[BetaCompactionConfigParam] | Omit
    """Compaction configuration.

    When set on `POST /v1/messages`, the request is a compaction request: the
    conversation in `messages` is summarized and the response holds only the
    resulting `compaction` block (`stop_reason` `"compaction"`), which later
    requests send first in `messages` in place of the messages it summarizes.
    `POST /v1/messages/count_tokens` accepts this parameter and ignores it: the
    count it returns is for the conversation in `messages` as sent. Cannot be
    combined with `context_management`.
    """

    container: Optional[message_create_params.Container] | Omit
    """Container identifier for reuse across requests."""

    context_management: Optional[BetaContextManagementConfigParam] | Omit
    """Context management configuration.

    This allows you to control how Claude manages context across multiple requests,
    such as whether to clear function results or not.
    """

    diagnostics: Optional[BetaDiagnosticsParam] | Omit
    """Request-level diagnostics.

    Supply `previous_message_id` to have the response include
    `diagnostics.cache_miss_reason` explaining any prompt-cache divergence from that
    prior request.
    """

    fallback_credit_token: Optional[message_create_params.FallbackCreditToken] | Omit
    """The `fallback_credit_token` from a prior refusal's `stop_details`.

    When a preceding request was refused and returned a `fallback_credit_token`,
    pass that code here on the retry to have the retry's cache-creation tokens for
    the prefix that was warm on the refused model billed at the cache-read rate.
    Must be redeemed by the same organization and workspace, with the same request
    body (optionally extended by one appended `assistant` message whose content is
    the partial text — with any trailing whitespace stripped from the final text
    block — and paired server-tool blocks streamed before the refusal; the
    appended-assistant form is not available for requests with `output_format` set
    or forced `tool_choice`), on an eligible fallback model, on the same platform,
    and within 5 minutes of the refusal; a mismatch is a 400. A token minted
    mid-server-tool-loop whose partial content was continuable may only be redeemed
    with the appended-assistant form — if an exact-body retry is rejected with a 400
    saying the token must be redeemed by continuing the partial response, retry with
    the appended-assistant form instead.

    When the appended-assistant form is used on a model that otherwise disallows
    assistant-turn prefill, this token also authorizes that one prefill.
    """

    fallbacks: Optional[BetaFallbacksParam] | Omit
    """
    Opt-in server-side retry on one or more substitute models when the requested
    model declines for policy reasons. Tried in order: if the first entry also
    declines, the second is tried, and so on. Some models don't support fallbacks;
    on those models, a list of fallback models returns a 400 error. See
    [Server-side fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback).
    The string "default" requests the requested model's server-defined default
    fallback configuration. On a model that doesn't support fallbacks, the request
    runs on the requested model alone, so a declined request stays declined.
    """

    inference_geo: Optional[str] | Omit
    """Specifies the geographic region for inference processing.

    If not specified, the workspace's `default_inference_geo` is used.
    """

    mcp_servers: Iterable[BetaRequestMCPServerURLDefinitionParam] | Omit
    """MCP servers to be utilized in this request"""

    metadata: BetaMetadataParam | Omit
    """An object describing metadata about the request."""

    service_tier: Literal["auto", "standard_only"] | Omit
    """
    Determines whether to use priority capacity (if available) or standard capacity
    for this request.

    Anthropic offers different levels of service for your API requests. See
    [service-tiers](https://platform.claude.com/docs/en/api/service-tiers) for
    details.
    """

    speed: Optional[Literal["standard", "fast"]] | Omit
    """The inference speed mode for this request.

    `"fast"` enables high output-tokens-per-second inference.

    Some models require the `fast-mode-2026-02-01` beta header for any `speed`
    value. See
    [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for
    which models.
    """

    stop_sequences: SequenceNotStr[str] | Omit
    """Custom text sequences that will cause the model to stop generating.

    Our models will normally stop when they have naturally completed their turn,
    which will result in a response `stop_reason` of `"end_turn"`.

    If you want the model to stop generating when it encounters custom strings of
    text, you can use the `stop_sequences` parameter. If the model encounters one of
    the custom sequences, the response `stop_reason` value will be `"stop_sequence"`
    and the response `stop_sequence` value will contain the matched stop sequence.
    """

    system: Union[str, Iterable[BetaTextBlockParam]] | Omit
    """System prompt.

    A system prompt is a way of providing context and instructions to Claude, such
    as specifying a particular goal or role. See our
    [guide to system prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role).
    """

    thinking: BetaThinkingConfigParam | Omit
    """Configuration for Claude's thinking.

    With `{"type": "adaptive"}`, Claude decides when and how much to think. With
    `{"type": "enabled"}` (manual extended thinking), you set a `budget_tokens` of
    at least 1,024. Thinking tokens count toward your `max_tokens` limit.

    Which `type` values are accepted, and what happens when you omit `thinking`,
    depend on the model. See
    [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#configuring-thinking)
    for each model's behavior.
    """

    tool_choice: BetaToolChoiceParam | Omit
    """How the model should use the provided tools.

    The model can use a specific tool, any available tool, decide by itself, or not
    use tools at all.
    """

    betas: List[AnthropicBetaParam] | Omit
    """Optional header to specify the beta version(s) you want to use."""

    user_profile_id: str | Omit
    """The user profile ID to attribute this request to.

    Use when acting on behalf of a party other than your organization.
    """

    workspace_id: str | Omit
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
