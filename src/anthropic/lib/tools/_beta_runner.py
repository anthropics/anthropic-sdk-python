from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Union,
    Generic,
    TypeVar,
    Callable,
    Iterable,
    Iterator,
    Coroutine,
    AsyncIterator,
)
from typing_extensions import TypedDict, override

import httpx

from ..._types import Body, Query, Headers, NotGiven
from ..._utils import consume_sync_iterator, consume_async_iterator
from ...types.beta import BetaMessage, BetaContentBlock, BetaMessageParam
from ._beta_functions import (
    BetaFunctionTool,
    BetaRunnableTool,
    BetaAsyncFunctionTool,
    BetaAsyncRunnableTool,
    BetaBuiltinFunctionTool,
    BetaAsyncBuiltinFunctionTool,
)
from ..streaming._beta_messages import BetaMessageStream, BetaAsyncMessageStream
from ...types.beta.message_create_params import MessageCreateParamsBase
from ...types.beta.beta_tool_result_block_param import BetaToolResultBlockParam

if TYPE_CHECKING:
    from ..._client import Anthropic, AsyncAnthropic


AnyFunctionToolT = TypeVar(
    "AnyFunctionToolT",
    bound=Union[
        BetaFunctionTool[Any], BetaAsyncFunctionTool[Any], BetaBuiltinFunctionTool, BetaAsyncBuiltinFunctionTool
    ],
)
RunnerItemT = TypeVar("RunnerItemT")

log = logging.getLogger(__name__)


class RequestOptions(TypedDict, total=False):
    extra_headers: Headers | None
    extra_query: Query | None
    extra_body: Body | None
    timeout: float | httpx.Timeout | None | NotGiven


class BaseToolRunner(Generic[AnyFunctionToolT]):
    def __init__(
        self,
        *,
        params: MessageCreateParamsBase,
        options: RequestOptions,
        tools: Iterable[AnyFunctionToolT],
        max_iterations: int | None = None,
    ) -> None:
        self._tools_by_name = {tool.name: tool for tool in tools}
        self._params: MessageCreateParamsBase = {
            **params,
            "messages": [message for message in params["messages"]],
        }
        self._options = options
        self._messages_modified = False
        self._cached_tool_call_response: BetaMessageParam | None = None
        self._max_iterations = max_iterations
        self._iteration_count = 0

    def set_messages_params(
        self, params: MessageCreateParamsBase | Callable[[MessageCreateParamsBase], MessageCreateParamsBase]
    ) -> None:
        """
        Update the parameters for the next API call. This invalidates any cached tool responses.

        Args:
            params (MessageCreateParamsBase | Callable): Either new parameters or a function to mutate existing parameters
        """
        if callable(params):
            params = params(self._params)
        self._params = params

    def append_messages(self, *messages: BetaMessageParam | BetaMessage) -> None:
        """Add one or more messages to the conversation history.

        This invalidates the cached tool response, i.e. if tools were already called, then they will
        be called again on the next loop iteration.
        """
        message_params: List[BetaMessageParam] = [
            {"role": message.role, "content": message.content} if isinstance(message, BetaMessage) else message
            for message in messages
        ]
        self._messages_modified = True
        self.set_messages_params(lambda params: {**params, "messages": [*self._params["messages"], *message_params]})
        self._cached_tool_call_response = None

    def _should_stop(self) -> bool:
        if self._max_iterations is not None and self._iteration_count >= self._max_iterations:
            return True
        return False


class BaseSyncToolRunner(BaseToolRunner[BetaRunnableTool], Generic[RunnerItemT], ABC):
    def __init__(
        self,
        *,
        params: MessageCreateParamsBase,
        options: RequestOptions,
        tools: Iterable[BetaRunnableTool],
        client: Anthropic,
        max_iterations: int | None = None,
    ) -> None:
        super().__init__(params=params, options=options, tools=tools, max_iterations=max_iterations)
        self._client = client
        self._iterator = self.__run__()
        self._last_message: Callable[[], BetaMessage] | BetaMessage | None = None

    def __next__(self) -> RunnerItemT:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[RunnerItemT]:
        for item in self._iterator:
            yield item

    @abstractmethod
    def __run__(self) -> Iterator[RunnerItemT]:
        raise NotImplementedError()

    def until_done(self) -> BetaMessage:
        """
        Consumes the tool runner stream and returns the last message if it has not been consumed yet.
        If it has, it simply returns the last message.
        """
        consume_sync_iterator(self)
        last_message = self._get_last_message()
        assert last_message is not None
        return last_message

    def generate_tool_call_response(self) -> BetaMessageParam | None:
        """Generate a MessageParam by calling tool functions with any tool use blocks from the last message.

        Note the tool call response is cached, repeated calls to this method will return the same response.

        None can be returned if no tool call was applicable.
        """
        if self._cached_tool_call_response is not None:
            log.debug("Returning cached tool call response.")
            return self._cached_tool_call_response
        response = self._generate_tool_call_response()
        self._cached_tool_call_response = response
        return response

    def _generate_tool_call_response(self) -> BetaMessageParam | None:
        content = self._get_last_assistant_message_content()
        if not content:
            return None

        tool_use_blocks = [block for block in content if block.type == "tool_use"]
        if not tool_use_blocks:
            return None

        results: list[BetaToolResultBlockParam] = []

        for tool_use in tool_use_blocks:
            tool = self._tools_by_name.get(tool_use.name)
            if tool is None:
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": f"Error: Tool '{tool_use.name}' not found",
                        "is_error": True,
                    }
                )
                continue

            try:
                result = tool.call(tool_use.input)
                results.append({"type": "tool_result", "tool_use_id": tool_use.id, "content": result})
            except Exception as exc:
                log.exception(f"Error occurred while calling tool: {tool.name}", exc_info=exc)
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": repr(exc),
                        "is_error": True,
                    }
                )

        return {"role": "user", "content": results}

    def _get_last_message(self) -> BetaMessage | None:
        if callable(self._last_message):
            return self._last_message()
        return self._last_message

    def _get_last_assistant_message_content(self) -> list[BetaContentBlock] | None:
        last_message = self._get_last_message()
        if last_message is None or last_message.role != "assistant" or not last_message.content:
            return None

        return last_message.content


class BetaToolRunner(BaseSyncToolRunner[BetaMessage]):
    @override
    def __run__(self) -> Iterator[BetaMessage]:
        self._last_message = message = self._client.beta.messages.create(**self._params, **self._options)
        yield message
        self._iteration_count += 1

        while not self._should_stop():
            response = self.generate_tool_call_response()
            if response is None:
                log.debug("Tool call was not requested, exiting from tool runner loop.")
                return

            if not self._messages_modified:
                self.append_messages(message, response)

            self._iteration_count += 1
            self._messages_modified = False
            self._cached_tool_call_response = None
            self._last_message = message = self._client.beta.messages.create(**self._params, **self._options)
            yield message


class BetaStreamingToolRunner(BaseSyncToolRunner[BetaMessageStream]):
    @override
    def __run__(self) -> Iterator[BetaMessageStream]:
        with self._client.beta.messages.stream(**self._params, **self._options) as stream:
            self._last_message = stream.get_final_message
            yield stream
            message = stream.get_final_message()
        self._iteration_count += 1

        while not self._should_stop():
            response = self.generate_tool_call_response()
            if response is None:
                log.debug("Tool call was not requested, exiting from tool runner loop.")
                return

            if not self._messages_modified:
                self.append_messages(message, response)
            self._iteration_count += 1
            self._messages_modified = False

            with self._client.beta.messages.stream(**self._params, **self._options) as stream:
                self._cached_tool_call_response = None
                self._last_message = stream.get_final_message
                yield stream
                message = stream.get_final_message()


class BaseAsyncToolRunner(BaseToolRunner[BetaAsyncRunnableTool], Generic[RunnerItemT], ABC):
    def __init__(
        self,
        *,
        params: MessageCreateParamsBase,
        options: RequestOptions,
        tools: Iterable[BetaAsyncRunnableTool],
        client: AsyncAnthropic,
        max_iterations: int | None = None,
    ) -> None:
        super().__init__(params=params, options=options, tools=tools, max_iterations=max_iterations)
        self._client = client
        self._iterator = self.__run__()
        self._last_message: Callable[[], Coroutine[None, None, BetaMessage]] | BetaMessage | None = None

    async def __anext__(self) -> RunnerItemT:
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[RunnerItemT]:
        async for item in self._iterator:
            yield item

    @abstractmethod
    async def __run__(self) -> AsyncIterator[RunnerItemT]:
        raise NotImplementedError()
        yield  # type: ignore[unreachable]

    async def until_done(self) -> BetaMessage:
        """
        Consumes the tool runner stream and returns the last message if it has not been consumed yet.
        If it has, it simply returns the last message.
        """
        await consume_async_iterator(self)
        last_message = await self._get_last_message()
        assert last_message is not None
        return last_message

    async def generate_tool_call_response(self) -> BetaMessageParam | None:
        """Generate a MessageParam by calling tool functions with any tool use blocks from the last message.

        Note the tool call response is cached, repeated calls to this method will return the same response.

        None can be returned if no tool call was applicable.
        """
        if self._cached_tool_call_response is not None:
            log.debug("Returning cached tool call response.")
            return self._cached_tool_call_response

        response = await self._generate_tool_call_response()
        self._cached_tool_call_response = response
        return response

    async def _get_last_message(self) -> BetaMessage | None:
        if callable(self._last_message):
            return await self._last_message()
        return self._last_message

    async def _get_last_assistant_message_content(self) -> list[BetaContentBlock] | None:
        last_message = await self._get_last_message()
        if last_message is None or last_message.role != "assistant" or not last_message.content:
            return None

        return last_message.content

    async def _generate_tool_call_response(self) -> BetaMessageParam | None:
        content = await self._get_last_assistant_message_content()
        if not content:
            return None

        tool_use_blocks = [block for block in content if block.type == "tool_use"]
        if not tool_use_blocks:
            return None

        results: list[BetaToolResultBlockParam] = []

        for tool_use in tool_use_blocks:
            tool = self._tools_by_name.get(tool_use.name)
            if tool is None:
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": f"Error: Tool '{tool_use.name}' not found",
                        "is_error": True,
                    }
                )
                continue

            try:
                result = await tool.call(tool_use.input)
                results.append({"type": "tool_result", "tool_use_id": tool_use.id, "content": result})
            except Exception as exc:
                log.exception(f"Error occurred while calling tool: {tool.name}", exc_info=exc)
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": repr(exc),
                        "is_error": True,
                    }
                )

        return {"role": "user", "content": results}


class BetaAsyncToolRunner(BaseAsyncToolRunner[BetaMessage]):
    @override
    async def __run__(self) -> AsyncIterator[BetaMessage]:
        self._last_message = message = await self._client.beta.messages.create(**self._params, **self._options)
        yield message
        self._iteration_count += 1

        while not self._should_stop():
            response = await self.generate_tool_call_response()
            if response is None:
                log.debug("Tool call was not requested, exiting from tool runner loop.")
                return

            if not self._messages_modified:
                self.append_messages(message, response)
            self._iteration_count += 1
            self._messages_modified = False
            self._cached_tool_call_response = None
            self._last_message = message = await self._client.beta.messages.create(**self._params, **self._options)
            yield message


class BetaAsyncStreamingToolRunner(BaseAsyncToolRunner[BetaAsyncMessageStream]):
    @override
    async def __run__(self) -> AsyncIterator[BetaAsyncMessageStream]:
        async with self._client.beta.messages.stream(**self._params, **self._options) as stream:
            self._last_message = stream.get_final_message
            yield stream
            message = await stream.get_final_message()
        self._iteration_count += 1

        while not self._should_stop():
            response = await self.generate_tool_call_response()
            if response is None:
                log.debug("Tool call was not requested, exiting from tool runner loop.")
                return

            if not self._messages_modified:
                self.append_messages(message, response)
            self._iteration_count += 1
            self._messages_modified = False

            async with self._client.beta.messages.stream(**self._params, **self._options) as stream:
                self._last_message = stream.get_final_message
                self._cached_tool_call_response = None
                yield stream
                message = await stream.get_final_message()
