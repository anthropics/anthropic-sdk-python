from __future__ import annotations

import asyncio
from types import TracebackType
from typing import TYPE_CHECKING, Any, Generic, TypeVar, Callable, cast
from typing_extensions import Iterator, Awaitable, AsyncIterator, override, assert_never

import httpx

from ...._utils import consume_sync_iterator, consume_async_iterator
from ...._models import construct_type
from ...._streaming import Stream, AsyncStream
from ....types.beta.tools import ToolsBetaMessage, ToolsBetaContentBlock, ToolsBetaMessageStreamEvent

if TYPE_CHECKING:
    from ...._client import Anthropic, AsyncAnthropic


class ToolsBetaMessageStream(Stream[ToolsBetaMessageStreamEvent]):
    text_stream: Iterator[str]
    """Iterator over just the text deltas in the stream.

    ```py
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()
    ```
    """

    def __init__(
        self,
        *,
        cast_to: type[ToolsBetaMessageStreamEvent],
        response: httpx.Response,
        client: Anthropic,
    ) -> None:
        super().__init__(cast_to=cast_to, response=response, client=client)

        self.text_stream = self.__stream_text__()
        self.__final_message_snapshot: ToolsBetaMessage | None = None
        self.__events: list[ToolsBetaMessageStreamEvent] = []

    def get_final_message(self) -> ToolsBetaMessage:
        """Waits until the stream has been read to completion and returns
        the accumulated `ToolsBetaMessage` object.
        """
        self.until_done()
        assert self.__final_message_snapshot is not None
        return self.__final_message_snapshot

    def get_final_text(self) -> str:
        """Returns all `text` content blocks concatenated together.

        > [!NOTE]
        > Currently the API will only respond with a single content block.

        Will raise an error if no `text` content blocks were returned.
        """
        message = self.get_final_message()
        text_blocks: list[str] = []
        for block in message.content:
            if block.type == "text":
                text_blocks.append(block.text)

        if not text_blocks:
            raise RuntimeError("Expected to have received at least 1 text block")

        return "".join(text_blocks)

    def until_done(self) -> None:
        """Blocks until the stream has been consumed"""
        consume_sync_iterator(self)

    @override
    def close(self) -> None:
        super().close()
        self.on_end()

    # properties
    @property
    def current_message_snapshot(self) -> ToolsBetaMessage:
        assert self.__final_message_snapshot is not None
        return self.__final_message_snapshot

    # event handlers
    def on_stream_event(self, event: ToolsBetaMessageStreamEvent) -> None:
        """Callback that is fired for every Server-Sent-Event"""

    def on_message(self, message: ToolsBetaMessage) -> None:
        """Callback that is fired when a full Message object is accumulated.

        This corresponds to the `message_stop` SSE type.
        """

    def on_content_block(self, content_block: ToolsBetaContentBlock) -> None:
        """Callback that is fired whenever a full ToolsBetaContentBlock is accumulated.

        This corresponds to the `content_block_stop` SSE type.
        """

    def on_text(self, text: str, snapshot: str) -> None:
        """Callback that is fired whenever a `text` ToolsBetaContentBlock is yielded.

        The first argument is the text delta and the second is the current accumulated
        text, for example:

        ```py
        on_text("Hello", "Hello")
        on_text(" there", "Hello there")
        on_text("!", "Hello there!")
        ```
        """

    def on_input_json(self, delta: str, snapshot: object) -> None:
        """Callback that is fired whenever a `input_json_delta` ToolsBetaContentBlock is yielded.

        The first argument is the json string delta and the second is the current accumulated
        parsed object, for example:

        ```
        on_input_json('{"locations": ["San ', {"locations": []})
        on_input_json('Francisco"]', {"locations": ["San Francisco"]})
        ```
        """

    def on_exception(self, exception: Exception) -> None:
        """Fires if any exception occurs"""

    def on_end(self) -> None:
        ...

    def on_timeout(self) -> None:
        """Fires if the request times out"""

    @override
    def __stream__(self) -> Iterator[ToolsBetaMessageStreamEvent]:
        try:
            for event in super().__stream__():
                self.__events.append(event)

                self.__final_message_snapshot = accumulate_event(
                    event=event,
                    current_snapshot=self.__final_message_snapshot,
                )
                self._emit_sse_event(event)

                yield event
        except (httpx.TimeoutException, asyncio.TimeoutError) as exc:
            self.on_timeout()
            self.on_exception(exc)
            raise
        except Exception as exc:
            self.on_exception(exc)
            raise
        finally:
            self.on_end()

    def __stream_text__(self) -> Iterator[str]:
        for chunk in self:
            if chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                yield chunk.delta.text

    def _emit_sse_event(self, event: ToolsBetaMessageStreamEvent) -> None:
        self.on_stream_event(event)

        if event.type == "message_start":
            # nothing special we want to fire here
            pass
        elif event.type == "message_delta":
            # nothing special we want to fire here
            pass
        elif event.type == "message_stop":
            self.on_message(self.current_message_snapshot)
        elif event.type == "content_block_start":
            # nothing special we want to fire here
            pass
        elif event.type == "content_block_delta":
            content = self.current_message_snapshot.content[event.index]
            if event.delta.type == "text_delta" and content.type == "text":
                self.on_text(event.delta.text, content.text)
            elif event.delta.type == "input_json_delta" and content.type == "tool_use":
                self.on_input_json(event.delta.partial_json, content.input)
        elif event.type == "content_block_stop":
            content = self.current_message_snapshot.content[event.index]
            self.on_content_block(content)
        else:
            # we only want exhaustive checking for linters, not at runtime
            if TYPE_CHECKING:  # type: ignore[unreachable]
                assert_never(event)


ToolsBetaMessageStreamT = TypeVar("ToolsBetaMessageStreamT", bound=ToolsBetaMessageStream)


class ToolsBetaMessageStreamManager(Generic[ToolsBetaMessageStreamT]):
    """Wrapper over MessageStream that is returned by `.stream()`.

    ```py
    with client.beta.tools.messages.stream(...) as stream:
        for chunk in stream:
            ...
    ```
    """

    def __init__(self, api_request: Callable[[], ToolsBetaMessageStreamT]) -> None:
        self.__stream: ToolsBetaMessageStreamT | None = None
        self.__api_request = api_request

    def __enter__(self) -> ToolsBetaMessageStreamT:
        self.__stream = self.__api_request()
        return self.__stream

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.__stream is not None:
            self.__stream.close()


class AsyncToolsBetaMessageStream(AsyncStream[ToolsBetaMessageStreamEvent]):
    text_stream: AsyncIterator[str]
    """Async iterator over just the text deltas in the stream.

    ```py
    async for text in stream.text_stream:
        print(text, end="", flush=True)
    print()
    ```
    """

    def __init__(
        self,
        *,
        cast_to: type[ToolsBetaMessageStreamEvent],
        response: httpx.Response,
        client: AsyncAnthropic,
    ) -> None:
        super().__init__(cast_to=cast_to, response=response, client=client)

        self.text_stream = self.__stream_text__()
        self.__final_message_snapshot: ToolsBetaMessage | None = None
        self.__events: list[ToolsBetaMessageStreamEvent] = []

    async def get_final_message(self) -> ToolsBetaMessage:
        """Waits until the stream has been read to completion and returns
        the accumulated `ToolsBetaMessage` object.
        """
        await self.until_done()
        assert self.__final_message_snapshot is not None
        return self.__final_message_snapshot

    async def get_final_text(self) -> str:
        """Returns all `text` content blocks concatenated together.

        > [!NOTE]
        > Currently the API will only respond with a single content block.

        Will raise an error if no `text` content blocks were returned.
        """
        message = await self.get_final_message()
        text_blocks: list[str] = []
        for block in message.content:
            if block.type == "text":
                text_blocks.append(block.text)

        if not text_blocks:
            raise RuntimeError("Expected to have received at least 1 text block")

        return "".join(text_blocks)

    async def until_done(self) -> None:
        """Waits until the stream has been consumed"""
        await consume_async_iterator(self)

    @override
    async def close(self) -> None:
        await super().close()
        await self.on_end()

    # properties
    @property
    def current_message_snapshot(self) -> ToolsBetaMessage:
        assert self.__final_message_snapshot is not None
        return self.__final_message_snapshot

    # event handlers
    async def on_stream_event(self, event: ToolsBetaMessageStreamEvent) -> None:
        """Callback that is fired for every Server-Sent-Event"""

    async def on_message(self, message: ToolsBetaMessage) -> None:
        """Callback that is fired when a full ToolsBetaMessage object is accumulated.

        This corresponds to the `message_stop` SSE type.
        """

    async def on_content_block(self, content_block: ToolsBetaContentBlock) -> None:
        """Callback that is fired whenever a full ToolsBetaContentBlock is accumulated.

        This corresponds to the `content_block_stop` SSE type.
        """

    async def on_text(self, text: str, snapshot: str) -> None:
        """Callback that is fired whenever a `text` ToolsBetaContentBlock is yielded.

        The first argument is the text delta and the second is the current accumulated
        text, for example:

        ```
        on_text("Hello", "Hello")
        on_text(" there", "Hello there")
        on_text("!", "Hello there!")
        ```
        """

    async def on_input_json(self, delta: str, snapshot: object) -> None:
        """Callback that is fired whenever a `input_json_delta` ToolsBetaContentBlock is yielded.

        The first argument is the json string delta and the second is the current accumulated
        parsed object, for example:

        ```
        on_input_json('{"locations": ["San ', {"locations": []})
        on_input_json('Francisco"]', {"locations": ["San Francisco"]})
        ```
        """

    async def on_final_text(self, text: str) -> None:
        """Callback that is fired whenever a full `text` ToolsBetaContentBlock is accumulated.

        This corresponds to the `content_block_stop` SSE type.
        """

    async def on_exception(self, exception: Exception) -> None:
        """Fires if any exception occurs"""

    async def on_end(self) -> None:
        ...

    async def on_timeout(self) -> None:
        """Fires if the request times out"""

    @override
    async def __stream__(self) -> AsyncIterator[ToolsBetaMessageStreamEvent]:
        try:
            async for event in super().__stream__():
                self.__events.append(event)

                self.__final_message_snapshot = accumulate_event(
                    event=event,
                    current_snapshot=self.__final_message_snapshot,
                )
                await self._emit_sse_event(event)

                yield event
        except (httpx.TimeoutException, asyncio.TimeoutError) as exc:
            await self.on_timeout()
            await self.on_exception(exc)
            raise
        except Exception as exc:
            await self.on_exception(exc)
            raise
        finally:
            await self.on_end()

    async def __stream_text__(self) -> AsyncIterator[str]:
        async for chunk in self:
            if chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                yield chunk.delta.text

    async def _emit_sse_event(self, event: ToolsBetaMessageStreamEvent) -> None:
        await self.on_stream_event(event)

        if event.type == "message_start":
            # nothing special we want to fire here
            pass
        elif event.type == "message_delta":
            # nothing special we want to fire here
            pass
        elif event.type == "message_stop":
            await self.on_message(self.current_message_snapshot)
        elif event.type == "content_block_start":
            # nothing special we want to fire here
            pass
        elif event.type == "content_block_delta":
            content = self.current_message_snapshot.content[event.index]
            if event.delta.type == "text_delta" and content.type == "text":
                await self.on_text(event.delta.text, content.text)
            elif event.delta.type == "input_json_delta" and content.type == "tool_use":
                await self.on_input_json(event.delta.partial_json, content.input)
            else:
                # TODO: warn?
                pass
        elif event.type == "content_block_stop":
            content = self.current_message_snapshot.content[event.index]
            await self.on_content_block(content)

            if content.type == "text":
                await self.on_final_text(content.text)
        else:
            # we only want exhaustive checking for linters, not at runtime
            if TYPE_CHECKING:  # type: ignore[unreachable]
                assert_never(event)


AsyncToolsBetaMessageStreamT = TypeVar("AsyncToolsBetaMessageStreamT", bound=AsyncToolsBetaMessageStream)


class AsyncToolsBetaMessageStreamManager(Generic[AsyncToolsBetaMessageStreamT]):
    """Wrapper over AsyncMessageStream that is returned by `.stream()`
    so that an async context manager can be used without `await`ing the
    original client call.

    ```py
    async with client.beta.tools.messages.stream(...) as stream:
        async for chunk in stream:
            ...
    ```
    """

    def __init__(self, api_request: Awaitable[AsyncToolsBetaMessageStreamT]) -> None:
        self.__stream: AsyncToolsBetaMessageStreamT | None = None
        self.__api_request = api_request

    async def __aenter__(self) -> AsyncToolsBetaMessageStreamT:
        self.__stream = await self.__api_request
        return self.__stream

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.__stream is not None:
            await self.__stream.close()


JSON_BUF_PROPERTY = "__json_buf"


def accumulate_event(
    *,
    event: ToolsBetaMessageStreamEvent,
    current_snapshot: ToolsBetaMessage | None,
) -> ToolsBetaMessage:
    if current_snapshot is None:
        if event.type == "message_start":
            return ToolsBetaMessage.construct(**cast(Any, event.message.to_dict()))

        raise RuntimeError(f'Unexpected event order, got {event.type} before "message_start"')

    if event.type == "content_block_start":
        # TODO: check index
        current_snapshot.content.append(
            cast(
                ToolsBetaContentBlock,
                construct_type(type_=ToolsBetaContentBlock, value=event.content_block.model_dump()),
            ),
        )
    elif event.type == "content_block_delta":
        content = current_snapshot.content[event.index]
        if content.type == "text" and event.delta.type == "text_delta":
            content.text += event.delta.text
        elif content.type == "tool_use" and event.delta.type == "input_json_delta":
            try:
                from pydantic_core import from_json
            except ImportError as exc:
                raise RuntimeError(
                    "Could not import `pydantic_core.from_json` which is required for tool use accumulation, do you have pydantic >= 2.7 installed?"
                ) from exc

            # we need to keep track of the raw JSON string as well so that we can
            # re-parse it for each delta, for now we just store it as an untyped
            # property on the snapshot
            json_buf = cast(str, getattr(content, JSON_BUF_PROPERTY, ""))
            json_buf += event.delta.partial_json

            if json_buf:
                content.input = from_json(json_buf, allow_partial=True)

            setattr(content, JSON_BUF_PROPERTY, json_buf)
    elif event.type == "message_delta":
        current_snapshot.stop_reason = event.delta.stop_reason
        current_snapshot.stop_sequence = event.delta.stop_sequence
        current_snapshot.usage.output_tokens = event.usage.output_tokens

    return current_snapshot
