# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .messages import Messages, AsyncMessages, MessagesWithRawResponse, AsyncMessagesWithRawResponse
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Beta", "AsyncBeta"]


class Beta(SyncAPIResource):
    @cached_property
    def messages(self) -> Messages:
        return Messages(self._client)

    @cached_property
    def with_raw_response(self) -> BetaWithRawResponse:
        return BetaWithRawResponse(self)


class AsyncBeta(AsyncAPIResource):
    @cached_property
    def messages(self) -> AsyncMessages:
        return AsyncMessages(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBetaWithRawResponse:
        return AsyncBetaWithRawResponse(self)


class BetaWithRawResponse:
    def __init__(self, beta: Beta) -> None:
        self.messages = MessagesWithRawResponse(beta.messages)


class AsyncBetaWithRawResponse:
    def __init__(self, beta: AsyncBeta) -> None:
        self.messages = AsyncMessagesWithRawResponse(beta.messages)
