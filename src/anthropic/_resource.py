# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import time
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._client import Anthropic, AsyncAnthropic


class SyncAPIResource:
    """
    Base class for synchronous API resource handling.

    Attributes:
        _client (Anthropic): The synchronous API client.

    """

    _client: Anthropic

    def __init__(self, client: Anthropic) -> None:
        """
        Initialize the SyncAPIResource instance.

        Args:
            client (Anthropic): The synchronous API client.

        """
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete
        self._get_api_list = client.get_api_list

    def _sleep(self, seconds: float) -> None:
        """
        Suspend execution for a specified number of seconds.

        Args:
            seconds (float): The number of seconds to sleep.

        """
        time.sleep(seconds)


class AsyncAPIResource:
    """
    Base class for asynchronous API resource handling.

    Attributes:
        _client (AsyncAnthropic): The asynchronous API client.

    """

    _client: AsyncAnthropic

    def __init__(self, client: AsyncAnthropic) -> None:
        """
        Initialize the AsyncAPIResource instance.

        Args:
            client (AsyncAnthropic): The asynchronous API client.

        """
        self._client = client
        self._get = client.get
        self._post = client.post
        self._patch = client.patch
        self._put = client.put
        self._delete = client.delete
        self._get_api_list = client.get_api_list

    async def _sleep(self, seconds: float) -> None:
        """
        Asynchronously suspend execution for a specified number of seconds.

        Args:
            seconds (float): The number of seconds to sleep.

        """
        await asyncio.sleep(seconds)
        