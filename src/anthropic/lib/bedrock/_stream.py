from __future__ import annotations

from typing import TypeVar, Iterator
from typing_extensions import AsyncIterator, override

import httpx

from ..._client import Anthropic, AsyncAnthropic
from ..._streaming import Stream, AsyncStream, ServerSentEvent
from ._stream_decoder import AWSEventStreamDecoder

_T = TypeVar("_T")


class BedrockStream(Stream[_T]):
    # the AWS decoder expects `bytes` instead of `str`
    _decoder: AWSEventStreamDecoder  # type: ignore

    def __init__(
        self,
        *,
        cast_to: type[_T],
        response: httpx.Response,
        client: Anthropic,
    ) -> None:
        super().__init__(cast_to=cast_to, response=response, client=client)

        self._decoder = AWSEventStreamDecoder()

    @override
    def _iter_events(self) -> Iterator[ServerSentEvent]:
        yield from self._decoder.iter(self.response.iter_bytes())


class AsyncBedrockStream(AsyncStream[_T]):
    # the AWS decoder expects `bytes` instead of `str`
    _decoder: AWSEventStreamDecoder  # type: ignore

    def __init__(
        self,
        *,
        cast_to: type[_T],
        response: httpx.Response,
        client: AsyncAnthropic,
    ) -> None:
        super().__init__(cast_to=cast_to, response=response, client=client)

        self._decoder = AWSEventStreamDecoder()

    @override
    async def _iter_events(self) -> AsyncIterator[ServerSentEvent]:
        async for sse in self._decoder.aiter(self.response.aiter_bytes()):
            yield sse
