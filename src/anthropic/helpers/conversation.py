"""ConversationManager helpers for multi-turn conversation management.

Provides :class:`ConversationManager` (sync) and
:class:`AsyncConversationManager` (async) that maintain multi-turn conversation
history and auto-truncate the oldest messages when approaching a model's
context-window limit.

.. note::
    Each instance is **not** thread-safe.  If you need concurrent access,
    create one :class:`ConversationManager` per thread/task.

Example::

    import anthropic
    from anthropic.helpers import ConversationManager

    client = anthropic.Anthropic()
    mgr = ConversationManager(
        client,
        model="claude-opus-4-5",
        max_tokens=1024,
        system="You are a helpful assistant.",
        context_window_limit=200_000,
    )
    response = mgr.get_response("Hello!")
    print(response.content[0].text)
    print(mgr.last_usage)
"""

from __future__ import annotations

from typing import Any, Optional


class ConversationManager:
    """Sync helper that maintains multi-turn conversation history.

    Parameters
    ----------
    client:
        A synchronous :class:`anthropic.Anthropic` client instance.
    model:
        The model identifier to use for all API calls.
    max_tokens:
        Maximum number of tokens to generate per response.
    system:
        Optional system prompt, passed verbatim to each API call.
    context_window_limit:
        If set, the manager will truncate the oldest message pairs whenever
        the estimated token count approaches this limit (minus the headroom).
    token_budget_headroom:
        Fraction of ``context_window_limit`` to reserve as safety headroom.
        Must be in ``[0.0, 1.0)``.  Defaults to ``0.10`` (10 %).
    accurate_token_counting:
        When ``True`` the manager calls ``client.messages.count_tokens()``
        for accurate truncation decisions (adds one extra API call per
        truncation loop iteration).  When ``False`` (default) it uses the
        ``input_tokens + output_tokens`` from the last response — zero
        extra API calls but slightly less precise.
    """

    def __init__(
        self,
        client: Any,
        *,
        model: str,
        max_tokens: int,
        system: Optional[str] = None,
        context_window_limit: Optional[int] = None,
        token_budget_headroom: float = 0.10,
        accurate_token_counting: bool = False,
    ) -> None:
        if not model:
            raise ValueError("'model' must not be an empty string.")
        if max_tokens < 1:
            raise ValueError(f"'max_tokens' must be >= 1, got {max_tokens}.")
        if context_window_limit is not None and context_window_limit < 1:
            raise ValueError(
                f"'context_window_limit' must be >= 1 when provided, got {context_window_limit}."
            )
        if not (0.0 <= token_budget_headroom < 1.0):
            raise ValueError(
                f"'token_budget_headroom' must be in [0.0, 1.0), got {token_budget_headroom}."
            )

        self._client = client
        self._model = model
        self._max_tokens = max_tokens
        self._system = system
        self._context_window_limit = context_window_limit
        self._token_budget_headroom = token_budget_headroom
        self._accurate_token_counting = accurate_token_counting

        self._history: list[Any] = []
        self._last_usage: Any = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_user_message(self, content: str | list[Any]) -> None:
        """Append a user message to the conversation history.

        Parameters
        ----------
        content:
            The message content — either a plain string or a list of content
            blocks (e.g. image + text).

        Raises
        ------
        ValueError
            If *content* is an empty string or an empty list.
        """
        if isinstance(content, str) and not content:
            raise ValueError("'content' must not be an empty string.")
        if isinstance(content, list) and len(content) == 0:
            raise ValueError("'content' must not be an empty list.")
        if self._history and self._history[-1]["role"] == "user":
            raise ValueError(
                "Cannot add a user message when the last message is already from "
                "the user. The Anthropic API requires strict user/assistant alternation."
            )
        self._history.append({"role": "user", "content": content})

    def get_response(
        self, content: Optional[str | list[Any]] = None, **kwargs: Any
    ) -> Any:
        """Send the current conversation to the API and return the response.

        Parameters
        ----------
        content:
            If provided, it is appended as a user message via
            :meth:`add_user_message` before making the API call.
        **kwargs:
            Additional keyword arguments forwarded verbatim to
            ``client.messages.create()``.

        Returns
        -------
        anthropic.types.Message
            The raw API response object.

        Raises
        ------
        ValueError
            If the conversation history is empty or does not end with a user
            message, or if truncation is impossible.
        """
        if content is not None:
            self.add_user_message(content)

        if not self._history or self._history[-1]["role"] != "user":
            raise ValueError(
                "The conversation history must end with a user message before "
                "calling get_response()."
            )

        if self._context_window_limit is not None:
            self._truncate_if_needed()

        extra: dict[str, Any] = {}
        if self._system is not None:
            extra["system"] = self._system

        response = self._client.messages.create(
            messages=list(self._history),
            model=self._model,
            max_tokens=self._max_tokens,
            **extra,
            **kwargs,
        )

        self._history.append({"role": "assistant", "content": response.content})
        self._last_usage = response.usage
        return response

    def reset(self) -> None:
        """Clear conversation history and last usage.

        Model, system prompt, and all configuration options are preserved.
        """
        self._history = []
        self._last_usage = None

    @property
    def history(self) -> list[Any]:
        """Return a shallow copy of the conversation history."""
        return list(self._history)

    @property
    def last_usage(self) -> Any:
        """Usage object from the most recent API response, or ``None``."""
        return self._last_usage

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _estimate_tokens(self) -> Optional[int]:
        """Return current token estimate or ``None`` if unavailable.

        In **accurate** mode, calls ``count_tokens`` for a precise input-only count.
        In **heuristic** mode, uses ``input_tokens + output_tokens`` from the last
        response — the previous output is now part of the conversation history, so
        summing both provides a conservative (slightly over-) estimate without an
        extra API call.
        """
        if self._accurate_token_counting:
            extra: dict[str, Any] = {}
            if self._system is not None:
                extra["system"] = self._system
            result = self._client.messages.count_tokens(
                messages=list(self._history),
                model=self._model,
                **extra,
            )
            return result.input_tokens
        else:
            if self._last_usage is None:
                return None
            # Previous output tokens are now part of the conversation input,
            # so summing both gives a conservative estimate.
            return self._last_usage.input_tokens + self._last_usage.output_tokens

    def _truncate_if_needed(self) -> None:
        """Drop the oldest user+assistant pairs until under the token threshold."""
        assert self._context_window_limit is not None
        threshold = self._context_window_limit * (1.0 - self._token_budget_headroom)

        estimated = self._estimate_tokens()
        if estimated is None:
            # First call in heuristic mode — skip truncation.
            return

        while estimated >= threshold:
            if len(self._history) < 2:
                raise ValueError(
                    f"Cannot truncate further — a single message pair already "
                    f"exceeds the token threshold for model '{self._model}' "
                    f"(limit={self._context_window_limit}, "
                    f"headroom={self._token_budget_headroom}). "
                    f"Consider increasing 'context_window_limit' or reducing "
                    f"the size of individual messages."
                )
            if (
                self._history[0]["role"] != "user"
                or self._history[1]["role"] != "assistant"
            ):
                raise ValueError(
                    "History role-alternation invariant violated; cannot truncate safely. "
                    "Expected [user, assistant] pair at the start of history."
                )
            pair_fraction = 2 / len(self._history)
            self._history.pop(0)  # oldest user message
            self._history.pop(0)  # oldest assistant message

            if self._accurate_token_counting:
                estimated = self._estimate_tokens()  # type: ignore[assignment]
            else:
                estimated = int(estimated * (1.0 - pair_fraction))

    def __repr__(self) -> str:
        turns = len(self._history) // 2
        limit = self._context_window_limit
        return (
            f"ConversationManager("
            f"model={self._model!r}, "
            f"turns={turns}, "
            f"context_window_limit={limit!r})"
        )


class AsyncConversationManager:
    """Async helper that maintains multi-turn conversation history.

    Mirrors :class:`ConversationManager` but exposes ``async def get_response()``,
    suitable for use inside ``asyncio`` event loops.

    Parameters
    ----------
    client:
        An asynchronous :class:`anthropic.AsyncAnthropic` client instance.
    model:
        The model identifier to use for all API calls.
    max_tokens:
        Maximum number of tokens to generate per response.
    system:
        Optional system prompt, passed verbatim to each API call.
    context_window_limit:
        If set, the manager will truncate the oldest message pairs whenever
        the estimated token count approaches this limit (minus the headroom).
    token_budget_headroom:
        Fraction of ``context_window_limit`` to reserve as safety headroom.
        Must be in ``[0.0, 1.0)``.  Defaults to ``0.10`` (10 %).
    accurate_token_counting:
        When ``True`` the manager calls ``client.messages.count_tokens()``
        for accurate truncation decisions.  When ``False`` (default) it uses
        the ``input_tokens + output_tokens`` from the last response.
    """

    def __init__(
        self,
        client: Any,
        *,
        model: str,
        max_tokens: int,
        system: Optional[str] = None,
        context_window_limit: Optional[int] = None,
        token_budget_headroom: float = 0.10,
        accurate_token_counting: bool = False,
    ) -> None:
        if not model:
            raise ValueError("'model' must not be an empty string.")
        if max_tokens < 1:
            raise ValueError(f"'max_tokens' must be >= 1, got {max_tokens}.")
        if context_window_limit is not None and context_window_limit < 1:
            raise ValueError(
                f"'context_window_limit' must be >= 1 when provided, got {context_window_limit}."
            )
        if not (0.0 <= token_budget_headroom < 1.0):
            raise ValueError(
                f"'token_budget_headroom' must be in [0.0, 1.0), got {token_budget_headroom}."
            )

        self._client = client
        self._model = model
        self._max_tokens = max_tokens
        self._system = system
        self._context_window_limit = context_window_limit
        self._token_budget_headroom = token_budget_headroom
        self._accurate_token_counting = accurate_token_counting

        self._history: list[Any] = []
        self._last_usage: Any = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_user_message(self, content: str | list[Any]) -> None:
        """Append a user message to the conversation history.

        Parameters
        ----------
        content:
            The message content — either a plain string or a list of content
            blocks.

        Raises
        ------
        ValueError
            If *content* is an empty string or an empty list.
        """
        if isinstance(content, str) and not content:
            raise ValueError("'content' must not be an empty string.")
        if isinstance(content, list) and len(content) == 0:
            raise ValueError("'content' must not be an empty list.")
        if self._history and self._history[-1]["role"] == "user":
            raise ValueError(
                "Cannot add a user message when the last message is already from "
                "the user. The Anthropic API requires strict user/assistant alternation."
            )
        self._history.append({"role": "user", "content": content})

    async def get_response(
        self, content: Optional[str | list[Any]] = None, **kwargs: Any
    ) -> Any:
        """Send the current conversation to the API and return the response.

        Parameters
        ----------
        content:
            If provided, it is appended as a user message via
            :meth:`add_user_message` before making the API call.
        **kwargs:
            Additional keyword arguments forwarded verbatim to
            ``client.messages.create()``.

        Returns
        -------
        anthropic.types.Message
            The raw API response object.

        Raises
        ------
        ValueError
            If the conversation history is empty or does not end with a user
            message, or if truncation is impossible.
        """
        if content is not None:
            self.add_user_message(content)

        if not self._history or self._history[-1]["role"] != "user":
            raise ValueError(
                "The conversation history must end with a user message before "
                "calling get_response()."
            )

        if self._context_window_limit is not None:
            await self._truncate_if_needed()

        extra: dict[str, Any] = {}
        if self._system is not None:
            extra["system"] = self._system

        response = await self._client.messages.create(
            messages=list(self._history),
            model=self._model,
            max_tokens=self._max_tokens,
            **extra,
            **kwargs,
        )

        self._history.append({"role": "assistant", "content": response.content})
        self._last_usage = response.usage
        return response

    def reset(self) -> None:
        """Clear conversation history and last usage.

        Model, system prompt, and all configuration options are preserved.
        """
        self._history = []
        self._last_usage = None

    @property
    def history(self) -> list[Any]:
        """Return a shallow copy of the conversation history."""
        return list(self._history)

    @property
    def last_usage(self) -> Any:
        """Usage object from the most recent API response, or ``None``."""
        return self._last_usage

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _estimate_tokens(self) -> Optional[int]:
        """Return current token estimate or ``None`` if unavailable.

        In **accurate** mode, calls ``count_tokens`` for a precise input-only count.
        In **heuristic** mode, uses ``input_tokens + output_tokens`` from the last
        response — the previous output is now part of the conversation history, so
        summing both provides a conservative (slightly over-) estimate without an
        extra API call.
        """
        if self._accurate_token_counting:
            extra: dict[str, Any] = {}
            if self._system is not None:
                extra["system"] = self._system
            result = await self._client.messages.count_tokens(
                messages=list(self._history),
                model=self._model,
                **extra,
            )
            return result.input_tokens
        else:
            if self._last_usage is None:
                return None
            # Previous output tokens are now part of the conversation input,
            # so summing both gives a conservative estimate.
            return self._last_usage.input_tokens + self._last_usage.output_tokens

    async def _truncate_if_needed(self) -> None:
        """Drop the oldest user+assistant pairs until under the token threshold."""
        assert self._context_window_limit is not None
        threshold = self._context_window_limit * (1.0 - self._token_budget_headroom)

        estimated = await self._estimate_tokens()
        if estimated is None:
            # First call in heuristic mode — skip truncation.
            return

        while estimated >= threshold:
            if len(self._history) < 2:
                raise ValueError(
                    f"Cannot truncate further — a single message pair already "
                    f"exceeds the token threshold for model '{self._model}' "
                    f"(limit={self._context_window_limit}, "
                    f"headroom={self._token_budget_headroom}). "
                    f"Consider increasing 'context_window_limit' or reducing "
                    f"the size of individual messages."
                )
            if (
                self._history[0]["role"] != "user"
                or self._history[1]["role"] != "assistant"
            ):
                raise ValueError(
                    "History role-alternation invariant violated; cannot truncate safely. "
                    "Expected [user, assistant] pair at the start of history."
                )
            pair_fraction = 2 / len(self._history)
            self._history.pop(0)  # oldest user message
            self._history.pop(0)  # oldest assistant message

            if self._accurate_token_counting:
                estimated = await self._estimate_tokens()  # type: ignore[assignment]
            else:
                estimated = int(estimated * (1.0 - pair_fraction))

    def __repr__(self) -> str:
        turns = len(self._history) // 2
        limit = self._context_window_limit
        return (
            f"AsyncConversationManager("
            f"model={self._model!r}, "
            f"turns={turns}, "
            f"context_window_limit={limit!r})"
        )
