# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .tools import (
    Tools,
    AsyncTools,
    ToolsWithRawResponse,
    AsyncToolsWithRawResponse,
    ToolsWithStreamingResponse,
    AsyncToolsWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .tools.tools import Tools, AsyncTools

__all__ = ["Beta", "AsyncBeta"]


class Beta(SyncAPIResource):
    @cached_property
    def tools(self) -> Tools:
        return Tools(self._client)

    @cached_property
    def with_raw_response(self) -> BetaWithRawResponse:
        return BetaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BetaWithStreamingResponse:
        return BetaWithStreamingResponse(self)


class AsyncBeta(AsyncAPIResource):
    @cached_property
    def tools(self) -> AsyncTools:
        return AsyncTools(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBetaWithRawResponse:
        return AsyncBetaWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBetaWithStreamingResponse:
        return AsyncBetaWithStreamingResponse(self)


class BetaWithRawResponse:
    def __init__(self, beta: Beta) -> None:
        self._beta = beta

    @cached_property
    def tools(self) -> ToolsWithRawResponse:
        return ToolsWithRawResponse(self._beta.tools)


class AsyncBetaWithRawResponse:
    def __init__(self, beta: AsyncBeta) -> None:
        self._beta = beta

    @cached_property
    def tools(self) -> AsyncToolsWithRawResponse:
        return AsyncToolsWithRawResponse(self._beta.tools)


class BetaWithStreamingResponse:
    def __init__(self, beta: Beta) -> None:
        self._beta = beta

    @cached_property
    def tools(self) -> ToolsWithStreamingResponse:
        return ToolsWithStreamingResponse(self._beta.tools)


class AsyncBetaWithStreamingResponse:
    def __init__(self, beta: AsyncBeta) -> None:
        self._beta = beta

    @cached_property
    def tools(self) -> AsyncToolsWithStreamingResponse:
        return AsyncToolsWithStreamingResponse(self._beta.tools)
