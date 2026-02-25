"""Double-buffered context window compaction control.

Implements the "hopping context windows" technique for seamless context
compaction without stop-the-world pauses. Instead of waiting until the
context is full and then blocking to summarize, this approach:

1. **Checkpoint** at a configurable threshold (default 70%) -- summarize
   the conversation and seed a back buffer with that summary.
2. **Concurrent** -- keep working in the active buffer while new messages
   are appended to both the active and back buffers.
3. **Swap** -- when the active buffer hits the swap threshold (default 95%),
   swap to the back buffer seamlessly.

Summaries accumulate across generations up to ``max_generations``, after
which older summaries are recursively compressed.
"""

from __future__ import annotations

import asyncio
import copy
import logging
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from dataclasses import field, dataclass
from typing_extensions import Literal, Required

from ...types.beta import BetaMessage, BetaMessageParam
from ._beta_compaction_control import (
    DEFAULT_THRESHOLD,
    DEFAULT_SUMMARY_PROMPT,
    CompactionControl,
)

if TYPE_CHECKING:
    from ..._client import Anthropic, AsyncAnthropic

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_CHECKPOINT_THRESHOLD_RATIO: float = 0.70
"""Fraction of context_token_threshold at which to trigger the checkpoint."""

DEFAULT_SWAP_THRESHOLD_RATIO: float = 0.95
"""Fraction of context_token_threshold at which to swap to the back buffer."""

DEFAULT_MAX_GENERATIONS: int | None = None
"""Maximum number of summary generations to accumulate before recursive compression.

None means no limit (renewal disabled).
"""

DEFAULT_CHECKPOINT_TIMEOUT: float = 120.0
"""Default timeout in seconds for checkpoint summarization calls."""


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


class RenewalPolicy(str, Enum):
    """Policy for handling accumulated summaries when ``max_generations`` is reached."""

    RECURSIVE = "recursive"
    """Recursively summarize all accumulated summaries into a single new one."""

    TRUNCATE = "truncate"
    """Drop the oldest summaries and keep only the most recent ones."""


class DoubleBufferCompactionControl(CompactionControl, total=False):
    """Extended compaction control that enables double-buffered context hopping.

    Inherits all fields from :class:`CompactionControl` and adds
    configuration for the checkpoint/swap thresholds and summary
    accumulation strategy.
    """

    enabled: Required[bool]

    checkpoint_threshold_ratio: float
    """Fraction of ``context_token_threshold`` at which to create a checkpoint
    summary and seed the back buffer.  Defaults to 0.70."""

    swap_threshold_ratio: float
    """Fraction of ``context_token_threshold`` at which to swap to the back
    buffer.  Defaults to 0.95."""

    max_generations: int | None
    """Maximum number of summary generations to accumulate before applying
    ``renewal_policy``.  None means no limit (renewal disabled)."""

    renewal_policy: Literal["recursive", "truncate"]
    """Policy to apply when ``max_generations`` is reached.
    ``"recursive"`` compresses all accumulated summaries into one.
    ``"truncate"`` drops the oldest summaries.  Defaults to ``"recursive"``."""

    checkpoint_timeout: float
    """Timeout in seconds for checkpoint summarization calls.
    Defaults to 120.0.  If exceeded, the call raises ``TimeoutError``."""


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


@dataclass
class DoubleBufferState:
    """Mutable state for the double-buffer compaction algorithm.

    Tracks the back buffer, accumulated summaries, and whether a
    checkpoint is currently in flight.
    """

    back_buffer: List[BetaMessageParam] = field(default_factory=list)
    """Messages accumulated in the back buffer since the last checkpoint."""

    accumulated_summaries: List[str] = field(default_factory=list)
    """Summaries from previous checkpoint generations."""

    current_generation: int = 0
    """How many checkpoint/swap cycles have been completed."""

    checkpoint_active: bool = False
    """Whether a checkpoint has been taken and the back buffer is being filled."""

    last_checkpoint_tokens: int = 0
    """Token count at the time the last checkpoint was created."""

    checkpoint_index: int = 0
    """Index into the original message list at which the checkpoint was created.

    Only messages at indices >= checkpoint_index should be mirrored to the
    back buffer during the concurrent phase.  This prevents historical
    messages from being re-copied."""


# ---------------------------------------------------------------------------
# Helpers (private)
# ---------------------------------------------------------------------------


def _get_token_count(message: BetaMessage | None) -> int:
    """Extract total token usage from a BetaMessage, returning 0 if unavailable."""
    if message is None:
        return 0
    total_input = (
        message.usage.input_tokens
        + (message.usage.cache_creation_input_tokens or 0)
        + (message.usage.cache_read_input_tokens or 0)
    )
    return total_input + message.usage.output_tokens


def _clean_trailing_tool_use(messages: List[BetaMessageParam]) -> List[BetaMessageParam]:
    """Return a copy of *messages* with any trailing tool_use blocks removed.

    The Anthropic API returns 400 if you send a ``tool_use`` block without a
    corresponding ``tool_result``.  When compacting we strip these.
    """
    messages = list(messages)
    if not messages:
        return messages

    last = messages[-1]
    if last["role"] == "assistant":
        content = last.get("content")
        if isinstance(content, (list, tuple)):
            non_tool_blocks = [
                block for block in content if isinstance(block, dict) and block.get("type") != "tool_use"
            ]
            if non_tool_blocks:
                messages[-1] = {**last, "content": non_tool_blocks}
            else:
                messages.pop()
        # If content is a plain string there are no tool_use blocks to strip.

    return messages


def _build_summary_seed(
    accumulated_summaries: List[str],
    new_summary: str,
) -> str:
    """Combine accumulated summaries and the new checkpoint summary into a
    single seed message for the back buffer."""
    parts: List[str] = []
    if accumulated_summaries:
        parts.append("=== Prior context summaries ===")
        for i, s in enumerate(accumulated_summaries, 1):
            parts.append(f"--- Generation {i} ---\n{s}")
        parts.append("=== End prior summaries ===\n")
    parts.append(new_summary)
    return "\n\n".join(parts)


def _apply_renewal_policy(
    state: DoubleBufferState,
    control: DoubleBufferCompactionControl,
    client: Anthropic,
    model: str,
    max_tokens: int,
) -> None:
    """Compress accumulated summaries according to ``renewal_policy`` (sync)."""
    policy = control.get("renewal_policy", RenewalPolicy.RECURSIVE.value)
    max_gens = control.get("max_generations", DEFAULT_MAX_GENERATIONS)

    if max_gens is None or len(state.accumulated_summaries) < max_gens:
        return

    if policy == RenewalPolicy.TRUNCATE.value:
        keep = max(1, max_gens // 2)
        dropped = len(state.accumulated_summaries) - keep
        state.accumulated_summaries = state.accumulated_summaries[-keep:]
        log.info(
            "Renewal policy 'truncate': dropped %d oldest summaries, kept %d.",
            dropped,
            keep,
        )
        return

    # Default: recursive summarization
    log.info(
        "Renewal policy 'recursive': compressing %d accumulated summaries.",
        len(state.accumulated_summaries),
    )
    combined = "\n\n---\n\n".join(state.accumulated_summaries)
    prompt = (
        "The following are successive summaries of a long-running conversation. "
        "Compress them into a single concise summary that retains all essential "
        "context needed to continue the task.\n\n" + combined
    )
    response = client.beta.messages.create(
        model=model,
        messages=[BetaMessageParam(role="user", content=prompt)],
        max_tokens=max_tokens,
        extra_headers={"X-Stainless-Helper": "double-buffer-renewal"},
    )
    first_content = list(response.content)[0]
    if first_content.type != "text":
        raise ValueError("Renewal compaction response is not text")
    state.accumulated_summaries = [first_content.text]
    log.info("Recursive renewal complete. Summaries compressed to 1.")


async def _apply_renewal_policy_async(
    state: DoubleBufferState,
    control: DoubleBufferCompactionControl,
    client: AsyncAnthropic,
    model: str,
    max_tokens: int,
) -> None:
    """Compress accumulated summaries according to ``renewal_policy`` (async)."""
    policy = control.get("renewal_policy", RenewalPolicy.RECURSIVE.value)
    max_gens = control.get("max_generations", DEFAULT_MAX_GENERATIONS)

    if max_gens is None or len(state.accumulated_summaries) < max_gens:
        return

    if policy == RenewalPolicy.TRUNCATE.value:
        keep = max(1, max_gens // 2)
        dropped = len(state.accumulated_summaries) - keep
        state.accumulated_summaries = state.accumulated_summaries[-keep:]
        log.info(
            "Renewal policy 'truncate': dropped %d oldest summaries, kept %d.",
            dropped,
            keep,
        )
        return

    # Default: recursive summarization
    log.info(
        "Renewal policy 'recursive': compressing %d accumulated summaries.",
        len(state.accumulated_summaries),
    )
    combined = "\n\n---\n\n".join(state.accumulated_summaries)
    prompt = (
        "The following are successive summaries of a long-running conversation. "
        "Compress them into a single concise summary that retains all essential "
        "context needed to continue the task.\n\n" + combined
    )
    response = await client.beta.messages.create(
        model=model,
        messages=[BetaMessageParam(role="user", content=prompt)],
        max_tokens=max_tokens,
        extra_headers={"X-Stainless-Helper": "double-buffer-renewal"},
    )
    first_content = list(response.content)[0]
    if first_content.type != "text":
        raise ValueError("Renewal compaction response is not text")
    state.accumulated_summaries = [first_content.text]
    log.info("Recursive renewal complete. Summaries compressed to 1.")


# ---------------------------------------------------------------------------
# Sync entry point
# ---------------------------------------------------------------------------


def check_and_compact_double_buffer(
    *,
    client: Anthropic,
    messages: List[BetaMessageParam],
    last_message: BetaMessage | None,
    model: str,
    max_tokens: int,
    control: DoubleBufferCompactionControl,
    state: DoubleBufferState,
) -> Optional[List[BetaMessageParam]]:
    """Check token usage and perform double-buffered compaction if needed.

    This follows the same call-site pattern as
    ``BaseSyncToolRunner._check_and_compact`` but returns the new message
    list (or ``None`` when no action was taken) so callers can use it with
    ``set_messages_params``.

    Parameters
    ----------
    client:
        The sync Anthropic client.
    messages:
        The current conversation messages (will **not** be mutated).
    last_message:
        The most recent ``BetaMessage`` response for token counting.
    model:
        The model name (used for summarization calls).
    max_tokens:
        ``max_tokens`` forwarded to summarization calls.
    control:
        The ``DoubleBufferCompactionControl`` configuration dict.
    state:
        A ``DoubleBufferState`` instance that persists across calls.

    Returns
    -------
    ``None`` if no compaction/swap happened.  Otherwise, the new messages
    list that should replace the current conversation.
    """
    if not control.get("enabled", False):
        return None

    tokens_used = _get_token_count(last_message)
    threshold = control.get("context_token_threshold", DEFAULT_THRESHOLD)
    checkpoint_ratio = control.get("checkpoint_threshold_ratio", DEFAULT_CHECKPOINT_THRESHOLD_RATIO)
    swap_ratio = control.get("swap_threshold_ratio", DEFAULT_SWAP_THRESHOLD_RATIO)
    checkpoint_threshold = int(threshold * checkpoint_ratio)
    swap_threshold = int(threshold * swap_ratio)

    # ------------------------------------------------------------------
    # Phase 3: SWAP -- active buffer is near capacity
    # ------------------------------------------------------------------
    if state.checkpoint_active and tokens_used >= swap_threshold:
        log.info(
            "Token usage %d >= swap threshold %d. Swapping to back buffer (generation %d).",
            tokens_used,
            swap_threshold,
            state.current_generation + 1,
        )
        new_messages = list(state.back_buffer)
        state.back_buffer = []
        state.checkpoint_active = False
        state.current_generation += 1
        state.last_checkpoint_tokens = 0

        # Apply renewal policy if needed
        summary_model = control.get("model", model)
        _apply_renewal_policy(state, control, client, summary_model, max_tokens)

        return new_messages

    # ------------------------------------------------------------------
    # Stop-the-world fallback -- at swap threshold with no checkpoint
    # ------------------------------------------------------------------
    # If we've hit the swap threshold but no checkpoint has been taken,
    # we MUST do a synchronous checkpoint + swap.  NEVER skip compaction.
    if not state.checkpoint_active and tokens_used >= swap_threshold:
        log.warning(
            "Stop-the-world: token usage %d >= swap threshold %d but no "
            "checkpoint exists. Performing synchronous checkpoint then swap.",
            tokens_used,
            swap_threshold,
        )

        summary_model = control.get("model", model)
        summary_prompt = control.get("summary_prompt", DEFAULT_SUMMARY_PROMPT)

        compaction_messages = _clean_trailing_tool_use(list(messages))
        compaction_messages.append(
            BetaMessageParam(role="user", content=summary_prompt),
        )

        response = client.beta.messages.create(
            model=summary_model,
            messages=compaction_messages,
            max_tokens=max_tokens,
            extra_headers={"X-Stainless-Helper": "double-buffer-checkpoint"},
        )

        first_content = list(response.content)[0]
        if first_content.type != "text":
            raise ValueError("Stop-the-world checkpoint compaction response is not text")

        summary_text = first_content.text
        log.info(
            "Stop-the-world checkpoint created (%d output tokens). Seeding and swapping immediately.",
            response.usage.output_tokens,
        )

        state.accumulated_summaries.append(summary_text)

        seed_text = _build_summary_seed(
            state.accumulated_summaries[:-1],
            summary_text,
        )
        new_messages: List[BetaMessageParam] = [
            BetaMessageParam(
                role="user",
                content=[{"type": "text", "text": seed_text}],
            ),
        ]
        # Only keep a small tail of recent messages -- NOT the entire
        # history.  The whole point of compaction is to reduce token count.
        # We keep roughly the last 30% of messages (at least 2) so the
        # model has enough immediate context.
        keep_count = max(2, len(messages) * 3 // 10)
        recent_messages = messages[-keep_count:]
        for msg in recent_messages:
            new_messages.append(copy.deepcopy(msg))

        state.back_buffer = []
        state.checkpoint_active = False
        state.current_generation += 1
        state.last_checkpoint_tokens = 0

        _apply_renewal_policy(state, control, client, summary_model, max_tokens)

        return new_messages

    # ------------------------------------------------------------------
    # Phase 1: CHECKPOINT -- create summary, seed back buffer
    # ------------------------------------------------------------------
    if not state.checkpoint_active and tokens_used >= checkpoint_threshold:
        log.info(
            "Token usage %d >= checkpoint threshold %d. Creating checkpoint summary.",
            tokens_used,
            checkpoint_threshold,
        )

        summary_model = control.get("model", model)
        summary_prompt = control.get("summary_prompt", DEFAULT_SUMMARY_PROMPT)

        # Build messages for the summarization call
        compaction_messages = _clean_trailing_tool_use(list(messages))
        compaction_messages.append(
            BetaMessageParam(role="user", content=summary_prompt),
        )

        response = client.beta.messages.create(
            model=summary_model,
            messages=compaction_messages,
            max_tokens=max_tokens,
            extra_headers={"X-Stainless-Helper": "double-buffer-checkpoint"},
        )

        first_content = list(response.content)[0]
        if first_content.type != "text":
            raise ValueError("Checkpoint compaction response is not text")

        summary_text = first_content.text
        log.info(
            "Checkpoint summary created (%d output tokens). Seeding back buffer.",
            response.usage.output_tokens,
        )

        # Accumulate the summary
        state.accumulated_summaries.append(summary_text)

        # Seed back buffer with the combined summary
        seed_text = _build_summary_seed(
            state.accumulated_summaries[:-1],
            summary_text,
        )
        state.back_buffer = [
            BetaMessageParam(
                role="user",
                content=[{"type": "text", "text": seed_text}],
            ),
        ]
        state.checkpoint_active = True
        state.last_checkpoint_tokens = tokens_used
        state.checkpoint_index = len(messages)

        # Return None -- the active buffer is NOT replaced yet; we keep
        # working in the current context window.
        return None

    # ------------------------------------------------------------------
    # Phase 2: CONCURRENT -- checkpoint is active, append to back buffer
    # ------------------------------------------------------------------
    if state.checkpoint_active:
        # Mirror only NEW messages (added after the checkpoint) into the
        # back buffer.  We use checkpoint_index to know where in the
        # original message list the checkpoint was taken, and the number
        # of already-mirrored messages (back_buffer length minus the seed)
        # to avoid re-copying.
        already_mirrored = len(state.back_buffer) - 1  # exclude the seed
        # Start from checkpoint_index + already_mirrored -- these are
        # the messages that appeared after the checkpoint and haven't
        # been copied yet.
        start = state.checkpoint_index + already_mirrored
        if start < len(messages):
            for msg in messages[start:]:
                state.back_buffer.append(copy.deepcopy(msg))

    return None


# ---------------------------------------------------------------------------
# Async entry point
# ---------------------------------------------------------------------------


async def acheck_and_compact_double_buffer(
    *,
    client: AsyncAnthropic,
    messages: List[BetaMessageParam],
    last_message: BetaMessage | None,
    model: str,
    max_tokens: int,
    control: DoubleBufferCompactionControl,
    state: DoubleBufferState,
) -> Optional[List[BetaMessageParam]]:
    """Async variant of :func:`check_and_compact_double_buffer`.

    See the sync version for full parameter documentation.
    """
    if not control.get("enabled", False):
        return None

    tokens_used = _get_token_count(last_message)
    threshold = control.get("context_token_threshold", DEFAULT_THRESHOLD)
    checkpoint_ratio = control.get("checkpoint_threshold_ratio", DEFAULT_CHECKPOINT_THRESHOLD_RATIO)
    swap_ratio = control.get("swap_threshold_ratio", DEFAULT_SWAP_THRESHOLD_RATIO)
    checkpoint_threshold = int(threshold * checkpoint_ratio)
    swap_threshold = int(threshold * swap_ratio)

    # ------------------------------------------------------------------
    # Phase 3: SWAP
    # ------------------------------------------------------------------
    if state.checkpoint_active and tokens_used >= swap_threshold:
        log.info(
            "Token usage %d >= swap threshold %d. Swapping to back buffer (generation %d).",
            tokens_used,
            swap_threshold,
            state.current_generation + 1,
        )
        new_messages = list(state.back_buffer)
        state.back_buffer = []
        state.checkpoint_active = False
        state.current_generation += 1
        state.last_checkpoint_tokens = 0

        summary_model = control.get("model", model)
        await _apply_renewal_policy_async(state, control, client, summary_model, max_tokens)

        return new_messages

    # ------------------------------------------------------------------
    # Stop-the-world fallback (async) -- at swap threshold with no checkpoint
    # ------------------------------------------------------------------
    if not state.checkpoint_active and tokens_used >= swap_threshold:
        log.warning(
            "Stop-the-world (async): token usage %d >= swap threshold %d but no "
            "checkpoint exists. Performing synchronous checkpoint then swap.",
            tokens_used,
            swap_threshold,
        )

        summary_model = control.get("model", model)
        summary_prompt = control.get("summary_prompt", DEFAULT_SUMMARY_PROMPT)

        compaction_messages = _clean_trailing_tool_use(list(messages))
        compaction_messages.append(
            BetaMessageParam(role="user", content=summary_prompt),
        )

        response = await client.beta.messages.create(
            model=summary_model,
            messages=compaction_messages,
            max_tokens=max_tokens,
            extra_headers={"X-Stainless-Helper": "double-buffer-checkpoint"},
        )

        first_content = list(response.content)[0]
        if first_content.type != "text":
            raise ValueError("Stop-the-world checkpoint compaction response is not text")

        summary_text = first_content.text
        log.info(
            "Stop-the-world checkpoint created (%d output tokens). Seeding and swapping immediately.",
            response.usage.output_tokens,
        )

        state.accumulated_summaries.append(summary_text)

        seed_text = _build_summary_seed(
            state.accumulated_summaries[:-1],
            summary_text,
        )
        new_messages: List[BetaMessageParam] = [
            BetaMessageParam(
                role="user",
                content=[{"type": "text", "text": seed_text}],
            ),
        ]
        # Only keep a small tail of recent messages -- NOT the entire
        # history.  The whole point of compaction is to reduce token count.
        keep_count = max(2, len(messages) * 3 // 10)
        recent_messages = messages[-keep_count:]
        for msg in recent_messages:
            new_messages.append(copy.deepcopy(msg))

        state.back_buffer = []
        state.checkpoint_active = False
        state.current_generation += 1
        state.last_checkpoint_tokens = 0

        await _apply_renewal_policy_async(state, control, client, summary_model, max_tokens)

        return new_messages

    # ------------------------------------------------------------------
    # Phase 1: CHECKPOINT
    # ------------------------------------------------------------------
    if not state.checkpoint_active and tokens_used >= checkpoint_threshold:
        log.info(
            "Token usage %d >= checkpoint threshold %d. Creating checkpoint summary.",
            tokens_used,
            checkpoint_threshold,
        )

        summary_model = control.get("model", model)
        summary_prompt = control.get("summary_prompt", DEFAULT_SUMMARY_PROMPT)
        ckpt_timeout = control.get("checkpoint_timeout", DEFAULT_CHECKPOINT_TIMEOUT)

        compaction_messages = _clean_trailing_tool_use(list(messages))
        compaction_messages.append(
            BetaMessageParam(role="user", content=summary_prompt),
        )

        try:
            response = await asyncio.wait_for(
                client.beta.messages.create(
                    model=summary_model,
                    messages=compaction_messages,
                    max_tokens=max_tokens,
                    extra_headers={"X-Stainless-Helper": "double-buffer-checkpoint"},
                ),
                timeout=ckpt_timeout,
            )
        except asyncio.TimeoutError:
            log.error(
                "Async checkpoint timed out after %.1fs. Back buffer not seeded.",
                ckpt_timeout,
            )
            raise

        first_content = list(response.content)[0]
        if first_content.type != "text":
            raise ValueError("Checkpoint compaction response is not text")

        summary_text = first_content.text
        log.info(
            "Checkpoint summary created (%d output tokens). Seeding back buffer.",
            response.usage.output_tokens,
        )

        state.accumulated_summaries.append(summary_text)

        seed_text = _build_summary_seed(
            state.accumulated_summaries[:-1],
            summary_text,
        )
        state.back_buffer = [
            BetaMessageParam(
                role="user",
                content=[{"type": "text", "text": seed_text}],
            ),
        ]
        state.checkpoint_active = True
        state.last_checkpoint_tokens = tokens_used
        state.checkpoint_index = len(messages)

        return None

    # ------------------------------------------------------------------
    # Phase 2: CONCURRENT
    # ------------------------------------------------------------------
    if state.checkpoint_active:
        # Mirror only NEW messages (added after the checkpoint).
        already_mirrored = len(state.back_buffer) - 1  # exclude the seed
        start = state.checkpoint_index + already_mirrored
        if start < len(messages):
            for msg in messages[start:]:
                state.back_buffer.append(copy.deepcopy(msg))

    return None
