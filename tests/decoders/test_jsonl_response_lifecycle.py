from __future__ import annotations

import json
from typing import Iterator, AsyncIterator
from typing_extensions import override

import httpx2
import pytest

from anthropic import Anthropic, AsyncAnthropic


class ResultStream(httpx2.SyncByteStream, httpx2.AsyncByteStream):
    def __init__(self, failure: str | None) -> None:
        self.failure = failure
        self.close_calls = 0

    @override
    def __iter__(self) -> Iterator[bytes]:
        # Fill the decoder's 64-byte read buffer before the transport fails.
        line = b'{"custom_id":"first","result":{"type":"canceled"}}'
        yield line + b" " * (63 - len(line)) + b"\n"
        if self.failure == "read":
            raise httpx2.ReadError("interrupted result download")
        if self.failure == "json":
            yield b"invalid json\n" + b" " * 64
        yield b'{"custom_id":"last","result":{"type":"canceled"}}\n'

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self:
            yield chunk

    @override
    def close(self) -> None:
        self.close_calls += 1

    @override
    async def aclose(self) -> None:
        self.close_calls += 1


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
@pytest.mark.parametrize("failure", ["json", "read", None], ids=["invalid-json", "read-error", "complete"])
async def test_batch_results_close_response(sync: bool, failure: str | None) -> None:
    stream = ResultStream(failure)
    requests: list[str] = []

    def handle(request: httpx2.Request) -> httpx2.Response:
        requests.append(request.url.path)
        if request.url.path == "/v1/messages/batches/batch_test":
            return httpx2.Response(200, json={"results_url": "https://example.test/results"})
        assert request.url.path == "/results"
        return httpx2.Response(200, stream=stream)

    transport = httpx2.MockTransport(handle)
    expected_error = json.JSONDecodeError if failure == "json" else httpx2.ReadError
    ids: list[str] = []
    if sync:
        with Anthropic(api_key="test-key", http_client=httpx2.Client(transport=transport)) as client:
            results = client.messages.batches.results("batch_test")
            if failure is None:
                ids = [result.custom_id for result in results]
            else:
                with pytest.raises(expected_error):
                    for result in results:
                        ids.append(result.custom_id)
            assert results.http_response.is_closed
            assert stream.close_calls == 1
    else:
        async with AsyncAnthropic(
            api_key="test-key", http_client=httpx2.AsyncClient(transport=transport)
        ) as async_client:
            async_results = await async_client.messages.batches.results("batch_test")
            if failure is None:
                ids = [result.custom_id async for result in async_results]
            else:
                with pytest.raises(expected_error):
                    async for result in async_results:
                        ids.append(result.custom_id)
            assert async_results.http_response.is_closed
            assert stream.close_calls == 1

    assert ids == (["first", "last"] if failure is None else ["first"])
    assert requests == ["/v1/messages/batches/batch_test", "/results"]
