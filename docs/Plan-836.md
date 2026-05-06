# Plan-836: ConversationManager Helper

## Summary

Add a `ConversationManager` (sync) and `AsyncConversationManager` (async) helper to `anthropic.helpers` that maintains multi-turn conversation history and auto-truncates the oldest messages when approaching a model's context window limit.

---

## Problem

Users building chatbots or agentic loops must manually manage `messages[]` history and handle `context_length_exceeded` errors themselves. There is no built-in helper in the SDK that:
- Maintains state across turns
- Protects against context overflow
- Follows the existing helper conventions (`RateLimitedClient`, `ResponseCache`, `RetryObserver`)

---

## Files

| Action   | Path                                                        |
|----------|-------------------------------------------------------------|
| Create   | `src/anthropic/helpers/conversation.py`                     |
| Create   | `tests/helpers/test_conversation.py`                        |
| Create   | `examples/helpers/conversation_example.py`                  |
| Modify   | `src/anthropic/helpers/__init__.py`                         |

---

## Class API

```python
class ConversationManager:
    def __init__(
        self,
        client: Any,
        *,
        model: str,
        max_tokens: int,
        system: str | None = None,
        context_window_limit: int | None = None,
        token_budget_headroom: float = 0.10,
        accurate_token_counting: bool = False,
    ) -> None: ...

    def add_user_message(self, content: str | list[Any]) -> None: ...
    def get_response(self, content: str | list[Any] | None = None, **kwargs: Any) -> Any: ...
    def reset(self) -> None: ...

    @property
    def history(self) -> list[Any]: ...       # shallow copy

    @property
    def last_usage(self) -> Any | None: ...   # Usage from last response
```

`AsyncConversationManager` mirrors the above with `async def get_response(...)`.

### Constructor validation (raises `ValueError`)
- `model` is empty string
- `max_tokens < 1`
- `context_window_limit` provided but `< 1`
- `token_budget_headroom` not in `[0.0, 1.0)`

---

## `get_response()` Flow

```
1. If content is not None → self.add_user_message(content)
2. If history empty or history[-1]["role"] != "user" → raise ValueError
3. If context_window_limit is set → _truncate_if_needed()
4. response = client.messages.create(
       messages=list(self._history),
       model=self._model,
       max_tokens=self._max_tokens,
       **{"system": self._system} if self._system else {},
       **kwargs,
   )
5. Append {"role": "assistant", "content": response.content} to history
6. self._last_usage = response.usage
7. return response
```

---

## Truncation Algorithm (`_truncate_if_needed`)

```
threshold = context_window_limit * (1.0 - token_budget_headroom)

Estimate tokens:
  accurate=True  → call client.messages.count_tokens(history, model, system)
  accurate=False → use last_usage.input_tokens + last_usage.output_tokens
                   (None on first call → skip truncation)

while estimated_tokens >= threshold:
    if len(history) < 2:
        raise ValueError("cannot truncate further — single message pair exceeds limit")
    pair_fraction = 2 / len(history)
    history.pop(0)   # oldest user
    history.pop(0)   # oldest assistant
    if accurate=True:
        re-call count_tokens to refresh estimate
    else:
        estimated_tokens = int(estimated_tokens * (1.0 - pair_fraction))
```

**Design decisions:**
- Drop oldest user+assistant **pairs** to maintain role-alternation invariant
- Heuristic mode (default): uses `last_usage` — zero extra API calls
- Accurate mode: calls `count_tokens()` — precise, adds latency per loop
- First call with `last_usage=None` → skip truncation
- History exhausted before threshold → `ValueError` with model + limit + suggestion

---

## `__init__.py` Changes

```python
from .conversation import ConversationManager, AsyncConversationManager

__all__ = [
    ...,
    "ConversationManager",
    "AsyncConversationManager",
]
```

---

## Test Coverage (`tests/helpers/test_conversation.py`)

### `class TestConversationManager`
- Constructor raises on: empty model, zero `max_tokens`, negative `context_window_limit`, invalid `token_budget_headroom`
- `add_user_message`: appends to history; raises on empty content
- `get_response`: calls API once, returns Message, appends assistant turn
- `get_response` with pre-staged message (no `content` arg)
- Multi-turn: 2 calls → 4 messages in history
- `last_usage` is `None` initially; populated after first call
- `**kwargs` forwarded to `messages.create` (e.g. `temperature=0.5`)
- System prompt passed when set; omitted when `None`
- No staged message raises `ValueError`
- `history` returns a copy (mutating it doesn't affect internal state)
- `reset()` clears history and `last_usage`; model/system unchanged
- Truncation: no-op when `context_window_limit=None`
- Truncation: no-op when under threshold
- Truncation: drops oldest pair when over threshold
- Truncation: drops multiple pairs until under threshold
- Truncation: raises `ValueError` when single pair still exceeds limit
- No truncation on first call (`last_usage=None`, heuristic mode)
- Accurate mode: `count_tokens` called; pairs dropped until under threshold

### `class TestAsyncConversationManager`
- Mirrors key cases using `AsyncMock` for `messages.create` and `messages.count_tokens`

### Mock helpers
```python
def _make_sync_client(*, input_tokens=100, output_tokens=50, content_text="Hello") -> MagicMock
def _make_async_client(*, input_tokens=100, output_tokens=50, content_text="Hello") -> MagicMock
```

---

## Example Script (`examples/helpers/conversation_example.py`)

Demonstrates:
1. Sync `ConversationManager` — two-turn conversation, print usage, reset
2. Async `AsyncConversationManager` — same flow with `asyncio.run()`

---

## Coding Conventions (match existing helpers)

- `from __future__ import annotations` at top
- `from typing import Any, Optional` — use `Any` for client to avoid circular imports
- Module-level docstring with `Example::` block (RST format)
- Keyword-only args after first positional (`client`)
- Validate inputs early, raise `ValueError` with clear messages
- Thread safety: not required (document that each instance is single-threaded)
- Store `response.content` (full `List[ContentBlock]`) as assistant message — not just `.text`
- `__repr__` showing model, turn count, and limit

---

## Verification

```bash
# Run new tests
python -m pytest tests/helpers/test_conversation.py -v

# Run full helper suite
python -m pytest tests/helpers/ -v

# Verify imports
python -c "from anthropic.helpers import ConversationManager, AsyncConversationManager; print('OK')"

# Run example (requires ANTHROPIC_API_KEY)
python examples/helpers/conversation_example.py
```
