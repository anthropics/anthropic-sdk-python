"""Tests for ConversationManager and AsyncConversationManager helpers."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, call

from anthropic.helpers import ConversationManager, AsyncConversationManager


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------


def _make_usage(*, input_tokens: int = 100, output_tokens: int = 50) -> MagicMock:
    usage = MagicMock()
    usage.input_tokens = input_tokens
    usage.output_tokens = output_tokens
    return usage


def _make_message(
    *, input_tokens: int = 100, output_tokens: int = 50, content_text: str = "Hello"
) -> MagicMock:
    msg = MagicMock()
    content_block = MagicMock()
    content_block.text = content_text
    msg.content = [content_block]
    msg.usage = _make_usage(input_tokens=input_tokens, output_tokens=output_tokens)
    return msg


def _make_sync_client(
    *, input_tokens: int = 100, output_tokens: int = 50, content_text: str = "Hello"
) -> MagicMock:
    """Return a MagicMock that mimics a synchronous Anthropic client."""
    client = MagicMock()
    msg = _make_message(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        content_text=content_text,
    )
    client.messages.create.return_value = msg
    # count_tokens returns an object with .input_tokens
    ct_result = MagicMock()
    ct_result.input_tokens = input_tokens + output_tokens
    client.messages.count_tokens.return_value = ct_result
    return client


def _make_async_client(
    *, input_tokens: int = 100, output_tokens: int = 50, content_text: str = "Hello"
) -> MagicMock:
    """Return a MagicMock that mimics an asynchronous Anthropic client."""
    client = MagicMock()
    msg = _make_message(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        content_text=content_text,
    )
    client.messages.create = AsyncMock(return_value=msg)
    ct_result = MagicMock()
    ct_result.input_tokens = input_tokens + output_tokens
    client.messages.count_tokens = AsyncMock(return_value=ct_result)
    return client


# ---------------------------------------------------------------------------
# TestConversationManager
# ---------------------------------------------------------------------------


class TestConversationManager:
    # --- Constructor validation ---

    def test_empty_model_raises(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="model"):
            ConversationManager(client, model="", max_tokens=512)

    def test_zero_max_tokens_raises(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="max_tokens"):
            ConversationManager(client, model="claude-3", max_tokens=0)

    def test_negative_max_tokens_raises(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="max_tokens"):
            ConversationManager(client, model="claude-3", max_tokens=-1)

    def test_negative_context_window_limit_raises(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="context_window_limit"):
            ConversationManager(
                client, model="claude-3", max_tokens=512, context_window_limit=-1
            )

    def test_zero_context_window_limit_raises(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="context_window_limit"):
            ConversationManager(
                client, model="claude-3", max_tokens=512, context_window_limit=0
            )

    def test_invalid_token_budget_headroom_negative(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="token_budget_headroom"):
            ConversationManager(
                client,
                model="claude-3",
                max_tokens=512,
                token_budget_headroom=-0.1,
            )

    def test_invalid_token_budget_headroom_one(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="token_budget_headroom"):
            ConversationManager(
                client,
                model="claude-3",
                max_tokens=512,
                token_budget_headroom=1.0,
            )

    def test_invalid_token_budget_headroom_greater_than_one(self):
        client = _make_sync_client()
        with pytest.raises(ValueError, match="token_budget_headroom"):
            ConversationManager(
                client,
                model="claude-3",
                max_tokens=512,
                token_budget_headroom=1.5,
            )

    def test_valid_token_budget_headroom_zero(self):
        client = _make_sync_client()
        mgr = ConversationManager(
            client, model="claude-3", max_tokens=512, token_budget_headroom=0.0
        )
        assert mgr is not None

    # --- add_user_message ---

    def test_add_user_message_appends(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.add_user_message("Hi")
        assert len(mgr.history) == 1
        assert mgr.history[0] == {"role": "user", "content": "Hi"}

    def test_add_user_message_empty_string_raises(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        with pytest.raises(ValueError):
            mgr.add_user_message("")

    def test_add_user_message_empty_list_raises(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        with pytest.raises(ValueError):
            mgr.add_user_message([])

    def test_add_user_message_list_content(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        blocks = [{"type": "text", "text": "Hello"}]
        mgr.add_user_message(blocks)
        assert mgr.history[0]["content"] == blocks

    # --- get_response ---

    def test_get_response_calls_api_once(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hello")
        client.messages.create.assert_called_once()

    def test_get_response_returns_message(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        response = mgr.get_response("Hello")
        assert response is client.messages.create.return_value

    def test_get_response_appends_assistant_turn(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hello")
        assert len(mgr.history) == 2
        assert mgr.history[1]["role"] == "assistant"

    def test_get_response_with_prestaged_message(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.add_user_message("Pre-staged question")
        mgr.get_response()  # no content arg
        assert len(mgr.history) == 2
        client.messages.create.assert_called_once()

    def test_multi_turn_four_messages(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("First question")
        mgr.get_response("Second question")
        assert len(mgr.history) == 4
        assert client.messages.create.call_count == 2

    def test_last_usage_none_initially(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        assert mgr.last_usage is None

    def test_last_usage_populated_after_call(self):
        client = _make_sync_client(input_tokens=200, output_tokens=75)
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hi")
        assert mgr.last_usage is not None
        assert mgr.last_usage.input_tokens == 200
        assert mgr.last_usage.output_tokens == 75

    def test_kwargs_forwarded_to_create(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hi", temperature=0.5)
        _, kwargs = client.messages.create.call_args
        assert kwargs.get("temperature") == 0.5

    def test_system_prompt_passed_when_set(self):
        client = _make_sync_client()
        mgr = ConversationManager(
            client, model="claude-3", max_tokens=512, system="You are a pirate."
        )
        mgr.get_response("Arrr")
        _, kwargs = client.messages.create.call_args
        assert kwargs.get("system") == "You are a pirate."

    def test_system_prompt_omitted_when_none(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hello")
        _, kwargs = client.messages.create.call_args
        assert "system" not in kwargs

    def test_no_staged_message_raises(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        with pytest.raises(ValueError):
            mgr.get_response()  # history is empty

    def test_history_last_not_user_raises(self):
        """Calling get_response twice without a new user message should fail."""
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hello")  # history ends with assistant
        with pytest.raises(ValueError):
            mgr.get_response()  # no new user message

    # --- history property ---

    def test_history_returns_copy(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.add_user_message("Hi")
        h = mgr.history
        h.append({"role": "user", "content": "mutated"})
        assert len(mgr.history) == 1  # internal state unchanged

    # --- reset ---

    def test_reset_clears_history(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hello")
        mgr.reset()
        assert mgr.history == []

    def test_reset_clears_last_usage(self):
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.get_response("Hello")
        mgr.reset()
        assert mgr.last_usage is None

    def test_reset_preserves_model_and_system(self):
        client = _make_sync_client()
        mgr = ConversationManager(
            client, model="claude-3", max_tokens=512, system="sys"
        )
        mgr.get_response("Hello")
        mgr.reset()
        assert mgr._model == "claude-3"
        assert mgr._system == "sys"

    # --- Truncation ---

    def test_truncation_no_op_when_limit_none(self):
        client = _make_sync_client(input_tokens=10000, output_tokens=5000)
        mgr = ConversationManager(
            client, model="claude-3", max_tokens=512, context_window_limit=None
        )
        mgr.get_response("Hi")
        assert len(mgr.history) == 2  # no truncation happened

    def test_truncation_no_op_when_under_threshold(self):
        # threshold = 1000 * 0.9 = 900; usage = 100+50 = 150 < 900
        client = _make_sync_client(input_tokens=100, output_tokens=50)
        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        mgr.get_response("First")
        mgr.get_response("Second")
        # After first turn: usage=150, threshold=900 → no truncation on second call
        assert len(mgr.history) == 4

    def test_truncation_drops_oldest_pair(self):
        # After turn 1: usage = 800+100 = 900 tokens
        # threshold = 1000 * 0.9 = 900 → 900 >= 900 → must truncate on turn 2
        client = _make_sync_client(input_tokens=800, output_tokens=100)
        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        mgr.get_response("First")   # 2 messages, usage=900
        mgr.get_response("Second")  # before API call: estimated=900 >= 900 → drop first pair
        # After truncation the first pair is removed; then new user msg is already present,
        # response appended → 2 messages total
        assert len(mgr.history) == 2

    def test_truncation_drops_multiple_pairs(self):
        # Build up 3 turns of history, then on 4th call the estimate is very high
        # We'll do this by controlling what count_tokens returns via accurate mode
        client = _make_sync_client(input_tokens=100, output_tokens=50)
        # Override count_tokens to return a high value first, then low
        ct_high = MagicMock()
        ct_high.input_tokens = 950  # above threshold
        ct_medium = MagicMock()
        ct_medium.input_tokens = 950  # still above
        ct_low = MagicMock()
        ct_low.input_tokens = 800  # below threshold = 1000*0.9=900

        client.messages.count_tokens.side_effect = [ct_high, ct_medium, ct_low]

        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
            accurate_token_counting=True,
        )
        # Seed history with 2 pairs manually (4 messages)
        mgr._history = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
            {"role": "user", "content": "q3"},  # current user message
        ]

        mgr.get_response()  # no content, history already ends with user
        # ct_high → drop pair 1 → ct_medium → drop pair 2 → ct_low → stop
        # Remaining: q3 + assistant response → 2 messages
        assert len(mgr.history) == 2

    def test_truncation_raises_when_single_pair_exceeds_limit(self):
        # Single user message + no prior assistant → cannot drop
        client = _make_sync_client(input_tokens=950, output_tokens=100)
        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        # Seed last_usage so heuristic has data
        mgr._last_usage = _make_usage(input_tokens=950, output_tokens=100)
        mgr._history = [{"role": "user", "content": "single large message"}]

        with pytest.raises(ValueError, match="Cannot truncate further"):
            mgr.get_response()

    def test_no_truncation_on_first_call_heuristic(self):
        # last_usage is None on first call → _estimate_tokens returns None → skip
        client = _make_sync_client(input_tokens=999, output_tokens=999)
        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=100,  # very small limit
            token_budget_headroom=0.10,
        )
        # Should not raise — first call skips truncation
        mgr.get_response("Hello")
        assert len(mgr.history) == 2

    def test_accurate_mode_count_tokens_called(self):
        client = _make_sync_client(input_tokens=50, output_tokens=25)
        # count_tokens returns 50 (below threshold=900 for limit=1000)
        ct = MagicMock()
        ct.input_tokens = 50
        client.messages.count_tokens.return_value = ct

        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
            accurate_token_counting=True,
        )
        mgr.get_response("Hi")
        client.messages.count_tokens.assert_called_once()

    def test_accurate_mode_drops_pairs_until_under_threshold(self):
        client = _make_sync_client(input_tokens=100, output_tokens=50)
        ct_high = MagicMock()
        ct_high.input_tokens = 950
        ct_low = MagicMock()
        ct_low.input_tokens = 800

        client.messages.count_tokens.side_effect = [ct_high, ct_low]

        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
            accurate_token_counting=True,
        )
        mgr._history = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
        ]
        mgr.get_response()
        # q1+a1 dropped, q2+assistant appended → 2 messages
        assert len(mgr.history) == 2
        assert client.messages.count_tokens.call_count == 2

    # --- Role-alternation guard ---

    def test_add_user_message_consecutive_raises(self):
        """Adding a second user message without an assistant reply should fail."""
        client = _make_sync_client()
        mgr = ConversationManager(client, model="claude-3", max_tokens=512)
        mgr.add_user_message("first")
        with pytest.raises(ValueError, match="alternation"):
            mgr.add_user_message("second")

    def test_truncation_invariant_violation_raises(self):
        """If history starts with broken alternation, truncation should raise."""
        client = _make_sync_client(input_tokens=800, output_tokens=100)
        mgr = ConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        mgr._last_usage = _make_usage(input_tokens=800, output_tokens=100)
        # Manually create broken history (assistant first)
        mgr._history = [
            {"role": "assistant", "content": "bad"},
            {"role": "user", "content": "q1"},
            {"role": "user", "content": "q2"},
        ]
        with pytest.raises(ValueError, match="alternation invariant"):
            mgr.get_response()


# ---------------------------------------------------------------------------
# TestAsyncConversationManager
# ---------------------------------------------------------------------------


class TestAsyncConversationManager:
    # --- Constructor validation ---

    def test_empty_model_raises(self):
        client = _make_async_client()
        with pytest.raises(ValueError, match="model"):
            AsyncConversationManager(client, model="", max_tokens=512)

    def test_zero_max_tokens_raises(self):
        client = _make_async_client()
        with pytest.raises(ValueError, match="max_tokens"):
            AsyncConversationManager(client, model="claude-3", max_tokens=0)

    def test_negative_context_window_limit_raises(self):
        client = _make_async_client()
        with pytest.raises(ValueError, match="context_window_limit"):
            AsyncConversationManager(
                client, model="claude-3", max_tokens=512, context_window_limit=-5
            )

    def test_invalid_token_budget_headroom(self):
        client = _make_async_client()
        with pytest.raises(ValueError, match="token_budget_headroom"):
            AsyncConversationManager(
                client,
                model="claude-3",
                max_tokens=512,
                token_budget_headroom=1.0,
            )

    # --- get_response ---

    @pytest.mark.asyncio
    async def test_get_response_calls_api_once(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        await mgr.get_response("Hello")
        client.messages.create.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_response_returns_message(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        response = await mgr.get_response("Hello")
        assert response is client.messages.create.return_value

    @pytest.mark.asyncio
    async def test_get_response_appends_assistant_turn(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        await mgr.get_response("Hello")
        assert len(mgr.history) == 2
        assert mgr.history[1]["role"] == "assistant"

    @pytest.mark.asyncio
    async def test_multi_turn(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        await mgr.get_response("First")
        await mgr.get_response("Second")
        assert len(mgr.history) == 4

    @pytest.mark.asyncio
    async def test_last_usage_none_initially(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        assert mgr.last_usage is None

    @pytest.mark.asyncio
    async def test_last_usage_populated_after_call(self):
        client = _make_async_client(input_tokens=300, output_tokens=60)
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        await mgr.get_response("Hi")
        assert mgr.last_usage.input_tokens == 300
        assert mgr.last_usage.output_tokens == 60

    @pytest.mark.asyncio
    async def test_kwargs_forwarded(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        await mgr.get_response("Hi", temperature=0.7)
        _, kwargs = client.messages.create.call_args
        assert kwargs.get("temperature") == 0.7

    @pytest.mark.asyncio
    async def test_system_prompt_passed(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(
            client, model="claude-3", max_tokens=512, system="Be concise."
        )
        await mgr.get_response("Hello")
        _, kwargs = client.messages.create.call_args
        assert kwargs.get("system") == "Be concise."

    @pytest.mark.asyncio
    async def test_no_staged_message_raises(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        with pytest.raises(ValueError):
            await mgr.get_response()

    @pytest.mark.asyncio
    async def test_history_returns_copy(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        mgr.add_user_message("Hi")
        h = mgr.history
        h.append({"role": "user", "content": "injected"})
        assert len(mgr.history) == 1

    @pytest.mark.asyncio
    async def test_reset(self):
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        await mgr.get_response("Hello")
        mgr.reset()
        assert mgr.history == []
        assert mgr.last_usage is None
        assert mgr._model == "claude-3"

    @pytest.mark.asyncio
    async def test_no_truncation_on_first_call_heuristic(self):
        client = _make_async_client(input_tokens=999, output_tokens=999)
        mgr = AsyncConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=100,
            token_budget_headroom=0.10,
        )
        await mgr.get_response("Hello")
        assert len(mgr.history) == 2

    @pytest.mark.asyncio
    async def test_accurate_mode_count_tokens_called(self):
        client = _make_async_client(input_tokens=50, output_tokens=25)
        ct = MagicMock()
        ct.input_tokens = 50
        client.messages.count_tokens = AsyncMock(return_value=ct)

        mgr = AsyncConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
            accurate_token_counting=True,
        )
        await mgr.get_response("Hi")
        client.messages.count_tokens.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_truncation_drops_oldest_pair(self):
        client = _make_async_client(input_tokens=800, output_tokens=100)
        mgr = AsyncConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        await mgr.get_response("First")    # usage=900
        await mgr.get_response("Second")   # estimated=900 >= 900 → drop first pair
        assert len(mgr.history) == 2

    @pytest.mark.asyncio
    async def test_truncation_raises_when_cannot_truncate(self):
        client = _make_async_client(input_tokens=950, output_tokens=100)
        mgr = AsyncConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        mgr._last_usage = _make_usage(input_tokens=950, output_tokens=100)
        mgr._history = [{"role": "user", "content": "single large message"}]

        with pytest.raises(ValueError, match="Cannot truncate further"):
            await mgr.get_response()

    # --- Role-alternation guard ---

    def test_add_user_message_consecutive_raises(self):
        """Adding a second user message without an assistant reply should fail."""
        client = _make_async_client()
        mgr = AsyncConversationManager(client, model="claude-3", max_tokens=512)
        mgr.add_user_message("first")
        with pytest.raises(ValueError, match="alternation"):
            mgr.add_user_message("second")

    @pytest.mark.asyncio
    async def test_truncation_invariant_violation_raises(self):
        """If history starts with broken alternation, truncation should raise."""
        client = _make_async_client(input_tokens=800, output_tokens=100)
        mgr = AsyncConversationManager(
            client,
            model="claude-3",
            max_tokens=512,
            context_window_limit=1000,
            token_budget_headroom=0.10,
        )
        mgr._last_usage = _make_usage(input_tokens=800, output_tokens=100)
        mgr._history = [
            {"role": "assistant", "content": "bad"},
            {"role": "user", "content": "q1"},
            {"role": "user", "content": "q2"},
        ]
        with pytest.raises(ValueError, match="alternation invariant"):
            await mgr.get_response()
