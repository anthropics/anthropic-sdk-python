"""Tests for double-buffered context window compaction."""

from __future__ import annotations

import logging
from typing import Any, List
from unittest.mock import AsyncMock, MagicMock

import pytest

from anthropic.types.beta import BetaMessageParam
from anthropic.lib.tools._beta_double_buffer_compaction import (
    DEFAULT_CHECKPOINT_TIMEOUT,
    DEFAULT_MAX_GENERATIONS,
    DEFAULT_SWAP_THRESHOLD_RATIO,
    DEFAULT_CHECKPOINT_THRESHOLD_RATIO,
    RenewalPolicy,
    DoubleBufferState,
    DoubleBufferCompactionControl,
    _get_token_count,
    _build_summary_seed,
    _clean_trailing_tool_use,
    check_and_compact_double_buffer,
    acheck_and_compact_double_buffer,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_usage(
    input_tokens: int = 100,
    output_tokens: int = 50,
    cache_creation_input_tokens: int = 0,
    cache_read_input_tokens: int = 0,
) -> MagicMock:
    usage = MagicMock()
    usage.input_tokens = input_tokens
    usage.output_tokens = output_tokens
    usage.cache_creation_input_tokens = cache_creation_input_tokens
    usage.cache_read_input_tokens = cache_read_input_tokens
    return usage


def _make_message(
    input_tokens: int = 100,
    output_tokens: int = 50,
    cache_creation: int = 0,
    cache_read: int = 0,
) -> MagicMock:
    msg = MagicMock()
    msg.usage = _make_usage(input_tokens, output_tokens, cache_creation, cache_read)
    return msg


def _make_summary_response(text: str = "<summary>Test summary</summary>") -> MagicMock:
    content_block = MagicMock()
    content_block.type = "text"
    content_block.text = text

    response = MagicMock()
    response.content = [content_block]
    response.usage = _make_usage(output_tokens=200)
    return response


def _make_control(**overrides: Any) -> DoubleBufferCompactionControl:
    defaults: DoubleBufferCompactionControl = {
        "enabled": True,
        "context_token_threshold": 1000,
    }
    defaults.update(overrides)  # type: ignore[typeddict-item]
    return defaults


def _make_messages(n: int = 3) -> List[BetaMessageParam]:
    messages: List[BetaMessageParam] = []
    for i in range(n):
        role = "user" if i % 2 == 0 else "assistant"
        messages.append(BetaMessageParam(role=role, content=f"Message {i}"))  # type: ignore[arg-type]
    return messages


# ---------------------------------------------------------------------------
# Unit tests: helpers
# ---------------------------------------------------------------------------


class TestGetTokenCount:
    def test_none_message(self) -> None:
        assert _get_token_count(None) == 0

    def test_basic_count(self) -> None:
        msg = _make_message(input_tokens=500, output_tokens=200)
        assert _get_token_count(msg) == 700

    def test_includes_cache_tokens(self) -> None:
        msg = _make_message(
            input_tokens=300,
            output_tokens=100,
            cache_creation=50,
            cache_read=25,
        )
        assert _get_token_count(msg) == 475  # 300 + 50 + 25 + 100


class TestCleanTrailingToolUse:
    def test_empty_messages(self) -> None:
        assert _clean_trailing_tool_use([]) == []

    def test_no_trailing_assistant(self) -> None:
        msgs: List[BetaMessageParam] = [{"role": "user", "content": "hi"}]
        assert _clean_trailing_tool_use(msgs) == msgs

    def test_removes_tool_use_blocks(self) -> None:
        msgs: List[BetaMessageParam] = [
            {"role": "user", "content": "do something"},
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "I'll help"},
                    {"type": "tool_use", "id": "t1", "name": "foo", "input": {}},
                ],
            },
        ]
        result = _clean_trailing_tool_use(msgs)
        assert len(result) == 2
        assert result[1]["content"] == [{"type": "text", "text": "I'll help"}]

    def test_removes_message_if_only_tool_use(self) -> None:
        msgs: List[BetaMessageParam] = [
            {"role": "user", "content": "do something"},
            {
                "role": "assistant",
                "content": [
                    {"type": "tool_use", "id": "t1", "name": "foo", "input": {}},
                ],
            },
        ]
        result = _clean_trailing_tool_use(msgs)
        assert len(result) == 1
        assert result[0]["role"] == "user"

    def test_does_not_mutate_original(self) -> None:
        msgs: List[BetaMessageParam] = [
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "ok"},
                    {"type": "tool_use", "id": "t1", "name": "foo", "input": {}},
                ],
            },
        ]
        _clean_trailing_tool_use(msgs)
        # Original should still have both blocks
        assert len(msgs[0]["content"]) == 2  # type: ignore[arg-type]

    def test_string_content_unchanged(self) -> None:
        msgs: List[BetaMessageParam] = [
            {"role": "assistant", "content": "just text"},
        ]
        result = _clean_trailing_tool_use(msgs)
        assert result == msgs


class TestBuildSummarySeed:
    def test_no_prior_summaries(self) -> None:
        result = _build_summary_seed([], "New summary here")
        assert result == "New summary here"

    def test_with_prior_summaries(self) -> None:
        result = _build_summary_seed(["Summary 1", "Summary 2"], "Summary 3")
        assert "Prior context summaries" in result
        assert "Generation 1" in result
        assert "Summary 1" in result
        assert "Generation 2" in result
        assert "Summary 2" in result
        assert "Summary 3" in result


class TestDoubleBufferState:
    def test_defaults(self) -> None:
        state = DoubleBufferState()
        assert state.back_buffer == []
        assert state.accumulated_summaries == []
        assert state.current_generation == 0
        assert state.checkpoint_active is False
        assert state.last_checkpoint_tokens == 0


class TestRenewalPolicy:
    def test_values(self) -> None:
        assert RenewalPolicy.RECURSIVE.value == "recursive"
        assert RenewalPolicy.TRUNCATE.value == "truncate"


class TestConstants:
    def test_default_ratios(self) -> None:
        assert DEFAULT_CHECKPOINT_THRESHOLD_RATIO == 0.70
        assert DEFAULT_SWAP_THRESHOLD_RATIO == 0.95
        assert DEFAULT_MAX_GENERATIONS is None


# ---------------------------------------------------------------------------
# Sync: check_and_compact_double_buffer
# ---------------------------------------------------------------------------


class TestCheckAndCompactDoubleBuffer:
    def test_disabled_returns_none(self) -> None:
        control = _make_control(enabled=False)
        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=9000, output_tokens=1000),
            model="claude-sonnet-4-5",
            max_tokens=4096,
            control=control,
            state=DoubleBufferState(),
        )
        assert result is None

    def test_below_checkpoint_threshold_no_action(self) -> None:
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()
        msg = _make_message(input_tokens=500, output_tokens=100)  # 600 < 700

        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=msg,
            model="claude-sonnet-4-5",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert result is None
        assert state.checkpoint_active is False

    def test_checkpoint_triggers_at_threshold(self) -> None:
        """Phase 1: When tokens >= 70% of threshold, checkpoint fires."""
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()
        msg = _make_message(input_tokens=600, output_tokens=150)  # 750 >= 700

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("checkpoint summary")

        result = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=msg,
            model="claude-sonnet-4-5",
            max_tokens=4096,
            control=control,
            state=state,
        )

        # Checkpoint does NOT swap yet -- returns None
        assert result is None
        assert state.checkpoint_active is True
        assert len(state.back_buffer) >= 1
        assert state.accumulated_summaries == ["checkpoint summary"]
        mock_client.beta.messages.create.assert_called_once()

    def test_checkpoint_uses_custom_model(self) -> None:
        control = _make_control(
            context_token_threshold=1000,
            model="claude-haiku-4-5",
        )
        state = DoubleBufferState()
        msg = _make_message(input_tokens=600, output_tokens=150)

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response()

        check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=msg,
            model="claude-sonnet-4-5",
            max_tokens=4096,
            control=control,
            state=state,
        )

        call_kwargs = mock_client.beta.messages.create.call_args
        assert call_kwargs.kwargs["model"] == "claude-haiku-4-5"

    def test_concurrent_phase_mirrors_messages(self) -> None:
        """Phase 2: After checkpoint, new messages are mirrored to back buffer."""
        state = DoubleBufferState()
        state.checkpoint_active = True
        state.back_buffer = [
            BetaMessageParam(role="user", content=[{"type": "text", "text": "seed"}]),
        ]

        control = _make_control(context_token_threshold=1000)
        messages = _make_messages(5)
        msg = _make_message(input_tokens=600, output_tokens=100)  # 700 < 950 swap

        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=messages,
            last_message=msg,
            model="claude-sonnet-4-5",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert result is None
        assert state.checkpoint_active is True
        # Back buffer should have the seed + mirrored messages
        assert len(state.back_buffer) > 1

    def test_swap_triggers_at_threshold(self) -> None:
        """Phase 3: When tokens >= 95% of threshold, swap to back buffer."""
        state = DoubleBufferState()
        state.checkpoint_active = True
        state.back_buffer = [
            BetaMessageParam(role="user", content=[{"type": "text", "text": "seed summary"}]),
            BetaMessageParam(role="user", content="mirrored msg 1"),
            BetaMessageParam(role="assistant", content="mirrored msg 2"),
        ]

        control = _make_control(context_token_threshold=1000)
        msg = _make_message(input_tokens=800, output_tokens=200)  # 1000 >= 950

        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=msg,
            model="claude-sonnet-4-5",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert result is not None
        assert len(result) == 3
        assert state.checkpoint_active is False
        assert state.current_generation == 1
        assert state.back_buffer == []

    def test_full_lifecycle(self) -> None:
        """Walks through checkpoint -> concurrent -> swap in sequence."""
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("lifecycle summary")

        # Step 1: Below threshold -- no action
        r = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(2),
            last_message=_make_message(input_tokens=400, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is None
        assert not state.checkpoint_active

        # Step 2: Hit checkpoint threshold (750 >= 700)
        r = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(4),
            last_message=_make_message(input_tokens=600, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is None
        assert state.checkpoint_active
        assert len(state.accumulated_summaries) == 1

        # Step 3: Concurrent phase -- below swap threshold (850 < 950)
        r = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(6),
            last_message=_make_message(input_tokens=700, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is None
        assert state.checkpoint_active

        # Step 4: Hit swap threshold (960 >= 950)
        r = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(8),
            last_message=_make_message(input_tokens=800, output_tokens=160),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is not None
        assert not state.checkpoint_active
        assert state.current_generation == 1

    def test_custom_thresholds(self) -> None:
        """Verify custom checkpoint and swap ratios are respected."""
        control = _make_control(
            context_token_threshold=1000,
            checkpoint_threshold_ratio=0.50,
            swap_threshold_ratio=0.80,
        )
        state = DoubleBufferState()

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response()

        # 550 >= 500 (50% of 1000) -> checkpoint
        r = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=_make_message(input_tokens=400, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is None
        assert state.checkpoint_active

        # 850 >= 800 (80% of 1000) -> swap
        r = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=_make_message(input_tokens=700, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is not None
        assert state.current_generation == 1

    def test_swap_back_buffer_contents_preserved(self) -> None:
        """When we swap, the returned messages match the back buffer exactly."""
        seed = BetaMessageParam(role="user", content=[{"type": "text", "text": "summary"}])
        msg1 = BetaMessageParam(role="user", content="question")
        msg2 = BetaMessageParam(role="assistant", content="answer")

        state = DoubleBufferState()
        state.checkpoint_active = True
        state.back_buffer = [seed, msg1, msg2]

        control = _make_control(context_token_threshold=1000)

        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert result is not None
        assert result[0] == seed
        assert result[1] == msg1
        assert result[2] == msg2

    def test_checkpoint_raises_on_non_text_response(self) -> None:
        """Checkpoint must produce a text response."""
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        bad_content = MagicMock()
        bad_content.type = "image"
        bad_response = MagicMock()
        bad_response.content = [bad_content]

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = bad_response

        with pytest.raises(ValueError, match="not text"):
            check_and_compact_double_buffer(
                client=mock_client,
                messages=_make_messages(),
                last_message=_make_message(input_tokens=600, output_tokens=200),
                model="m",
                max_tokens=4096,
                control=control,
                state=state,
            )

    def test_logging_on_checkpoint(self, caplog: pytest.LogCaptureFixture) -> None:
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response()

        with caplog.at_level(logging.INFO, logger="anthropic.lib.tools._beta_double_buffer_compaction"):
            check_and_compact_double_buffer(
                client=mock_client,
                messages=_make_messages(),
                last_message=_make_message(input_tokens=600, output_tokens=150),
                model="m",
                max_tokens=4096,
                control=control,
                state=state,
            )

        assert any("checkpoint threshold" in r.message.lower() for r in caplog.records)

    def test_logging_on_swap(self, caplog: pytest.LogCaptureFixture) -> None:
        state = DoubleBufferState()
        state.checkpoint_active = True
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(context_token_threshold=1000)

        with caplog.at_level(logging.INFO, logger="anthropic.lib.tools._beta_double_buffer_compaction"):
            check_and_compact_double_buffer(
                client=MagicMock(),
                messages=_make_messages(),
                last_message=_make_message(input_tokens=900, output_tokens=100),
                model="m",
                max_tokens=4096,
                control=control,
                state=state,
            )

        assert any("swap" in r.message.lower() for r in caplog.records)


# ---------------------------------------------------------------------------
# Renewal policy tests (sync)
# ---------------------------------------------------------------------------


class TestRenewalPolicySync:
    def test_recursive_renewal_compresses_summaries(self) -> None:
        state = DoubleBufferState()
        state.accumulated_summaries = [f"Summary {i}" for i in range(5)]
        state.checkpoint_active = True
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(
            context_token_threshold=1000,
            max_generations=5,
            renewal_policy="recursive",
        )

        mock_client = MagicMock()
        # The renewal call
        mock_client.beta.messages.create.return_value = _make_summary_response("compressed")

        check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert state.accumulated_summaries == ["compressed"]

    def test_truncate_renewal_keeps_recent(self) -> None:
        state = DoubleBufferState()
        state.accumulated_summaries = [f"Summary {i}" for i in range(5)]
        state.checkpoint_active = True
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(
            context_token_threshold=1000,
            max_generations=5,
            renewal_policy="truncate",
        )

        check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        # max_gens=5, keep=max(1, 5//2)=2, so should keep last 2
        assert len(state.accumulated_summaries) == 2
        assert state.accumulated_summaries == ["Summary 3", "Summary 4"]

    def test_renewal_not_triggered_below_max_generations(self) -> None:
        state = DoubleBufferState()
        state.accumulated_summaries = ["S1", "S2"]
        state.checkpoint_active = True
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(
            context_token_threshold=1000,
            max_generations=5,
            renewal_policy="recursive",
        )

        mock_client = MagicMock()
        # Should not be called for renewal since we're below max_generations
        mock_client.beta.messages.create.return_value = _make_summary_response()

        check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        # Summaries untouched
        assert state.accumulated_summaries == ["S1", "S2"]
        # The create call should NOT have been made (no renewal needed)
        mock_client.beta.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# Async: acheck_and_compact_double_buffer
# ---------------------------------------------------------------------------


class TestAsyncCheckAndCompactDoubleBuffer:
    @pytest.mark.asyncio
    async def test_disabled_returns_none(self) -> None:
        control = _make_control(enabled=False)
        result = await acheck_and_compact_double_buffer(
            client=AsyncMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=9000, output_tokens=1000),
            model="m",
            max_tokens=4096,
            control=control,
            state=DoubleBufferState(),
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_below_threshold_no_action(self) -> None:
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        result = await acheck_and_compact_double_buffer(
            client=AsyncMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=400, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert result is None
        assert not state.checkpoint_active

    @pytest.mark.asyncio
    async def test_checkpoint_fires_async(self) -> None:
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        mock_client = AsyncMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("async checkpoint")

        result = await acheck_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=_make_message(input_tokens=600, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert result is None
        assert state.checkpoint_active
        assert state.accumulated_summaries == ["async checkpoint"]

    @pytest.mark.asyncio
    async def test_swap_fires_async(self) -> None:
        state = DoubleBufferState()
        state.checkpoint_active = True
        state.back_buffer = [
            BetaMessageParam(role="user", content="seed"),
            BetaMessageParam(role="user", content="mirrored"),
        ]

        control = _make_control(context_token_threshold=1000)

        result = await acheck_and_compact_double_buffer(
            client=AsyncMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert result is not None
        assert len(result) == 2
        assert not state.checkpoint_active
        assert state.current_generation == 1

    @pytest.mark.asyncio
    async def test_full_lifecycle_async(self) -> None:
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        mock_client = AsyncMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("async summary")

        # Below threshold
        r = await acheck_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(2),
            last_message=_make_message(input_tokens=400, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is None
        assert not state.checkpoint_active

        # Checkpoint
        r = await acheck_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(4),
            last_message=_make_message(input_tokens=600, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is None
        assert state.checkpoint_active

        # Swap
        r = await acheck_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(6),
            last_message=_make_message(input_tokens=800, output_tokens=200),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert r is not None
        assert state.current_generation == 1

    @pytest.mark.asyncio
    async def test_async_recursive_renewal(self) -> None:
        state = DoubleBufferState()
        state.accumulated_summaries = [f"S{i}" for i in range(5)]
        state.checkpoint_active = True
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(
            context_token_threshold=1000,
            max_generations=5,
            renewal_policy="recursive",
        )

        mock_client = AsyncMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("compressed async")

        await acheck_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert state.accumulated_summaries == ["compressed async"]


# ---------------------------------------------------------------------------
# Multi-generation tests
# ---------------------------------------------------------------------------


class TestMultiGeneration:
    def test_summaries_accumulate_across_generations(self) -> None:
        """Verify summaries pile up across multiple checkpoint/swap cycles."""
        control = _make_control(context_token_threshold=1000, max_generations=10)
        state = DoubleBufferState()
        mock_client = MagicMock()

        for gen in range(3):
            mock_client.beta.messages.create.return_value = _make_summary_response(f"summary-{gen}")

            # Checkpoint
            check_and_compact_double_buffer(
                client=mock_client,
                messages=_make_messages(4),
                last_message=_make_message(input_tokens=600, output_tokens=150),
                model="m",
                max_tokens=4096,
                control=control,
                state=state,
            )
            assert state.checkpoint_active

            # Swap
            result = check_and_compact_double_buffer(
                client=mock_client,
                messages=_make_messages(6),
                last_message=_make_message(input_tokens=900, output_tokens=100),
                model="m",
                max_tokens=4096,
                control=control,
                state=state,
            )
            assert result is not None
            assert not state.checkpoint_active

        assert state.current_generation == 3
        assert len(state.accumulated_summaries) == 3
        assert state.accumulated_summaries == ["summary-0", "summary-1", "summary-2"]

    def test_back_buffer_seed_includes_prior_summaries(self) -> None:
        """When checkpoint fires with prior summaries, the seed should contain them."""
        control = _make_control(context_token_threshold=1000, max_generations=10)
        state = DoubleBufferState()
        state.accumulated_summaries = ["prior-1", "prior-2"]

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("new checkpoint")

        check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(4),
            last_message=_make_message(input_tokens=600, output_tokens=150),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert state.checkpoint_active
        seed_content = state.back_buffer[0]["content"]
        # The seed should be a list with a single text block
        assert isinstance(seed_content, list)
        seed_text = seed_content[0]["text"]  # type: ignore[index]
        assert "prior-1" in seed_text
        assert "prior-2" in seed_text
        assert "new checkpoint" in seed_text


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_none_last_message_treated_as_zero_tokens(self) -> None:
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=None,
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert result is None
        assert not state.checkpoint_active

    def test_concurrent_with_no_new_messages(self) -> None:
        """Concurrent phase with 1 message total (just seed) should not crash."""
        state = DoubleBufferState()
        state.checkpoint_active = True
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(context_token_threshold=1000)
        # Only 1 message in the conversation, mirrored_count=0, so nothing to mirror
        result = check_and_compact_double_buffer(
            client=MagicMock(),
            messages=[BetaMessageParam(role="user", content="only message")],
            last_message=_make_message(input_tokens=600, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )
        assert result is None

    def test_state_isolation_between_instances(self) -> None:
        """Two state instances should not share mutable defaults."""
        s1 = DoubleBufferState()
        s2 = DoubleBufferState()
        s1.back_buffer.append(BetaMessageParam(role="user", content="only in s1"))
        assert len(s2.back_buffer) == 0

    def test_swap_resets_last_checkpoint_tokens(self) -> None:
        state = DoubleBufferState()
        state.checkpoint_active = True
        state.last_checkpoint_tokens = 750
        state.back_buffer = [BetaMessageParam(role="user", content="seed")]

        control = _make_control(context_token_threshold=1000)

        check_and_compact_double_buffer(
            client=MagicMock(),
            messages=_make_messages(),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert state.last_checkpoint_tokens == 0


# ---------------------------------------------------------------------------
# Stop-the-world fallback tests
# ---------------------------------------------------------------------------


class TestStopTheWorldFallback:
    """When tokens hit swap threshold but no checkpoint exists, we MUST do
    an inline checkpoint+swap.  NEVER skip compaction."""

    def test_sync_stop_the_world_checkpoint_and_swap(self) -> None:
        """Sync: at swap threshold with no checkpoint -> checkpoint+swap in one call."""
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()
        # No checkpoint_active, no back_buffer

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("stw summary")

        # Token usage at swap threshold (960 >= 950) but no checkpoint exists
        result = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(5),
            last_message=_make_message(input_tokens=800, output_tokens=160),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        # Should return new messages (swap happened), NOT None
        assert result is not None
        assert not state.checkpoint_active
        assert state.current_generation == 1
        assert state.back_buffer == []
        # Summary should have been accumulated
        assert "stw summary" in state.accumulated_summaries
        mock_client.beta.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_stop_the_world_checkpoint_and_swap(self) -> None:
        """Async: at swap threshold with no checkpoint -> checkpoint+swap in one call."""
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        mock_client = AsyncMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("async stw")

        result = await acheck_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(5),
            last_message=_make_message(input_tokens=800, output_tokens=160),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        assert result is not None
        assert not state.checkpoint_active
        assert state.current_generation == 1
        assert "async stw" in state.accumulated_summaries

    def test_sync_stop_the_world_never_returns_none(self) -> None:
        """At swap threshold without checkpoint, the function must NEVER return
        None (which would mean 'no compaction happened')."""
        control = _make_control(context_token_threshold=1000)
        state = DoubleBufferState()

        mock_client = MagicMock()
        mock_client.beta.messages.create.return_value = _make_summary_response("forced")

        result = check_and_compact_double_buffer(
            client=mock_client,
            messages=_make_messages(3),
            last_message=_make_message(input_tokens=900, output_tokens=100),
            model="m",
            max_tokens=4096,
            control=control,
            state=state,
        )

        # Must return messages, not None
        assert result is not None
        assert len(result) > 0
