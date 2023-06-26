# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._client import Anthropic, AsyncAnthropic


class SyncAPIResource:
    _client: Anthropic

    def __init__(self, client: Anthropic) -> None:
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete
        self._get_api_list = client.get_api_list


class AsyncAPIResource:
    _client: AsyncAnthropic

    def __init__(self, client: AsyncAnthropic) -> None:
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete
        self._get_api_list = client.get_api_list
