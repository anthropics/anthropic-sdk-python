# Note: initially copied from https://github.com/florimondmanca/httpx-sse/blob/master/src/httpx_sse/_decoders.py
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Generic, Iterator, AsyncIterator

import httpx

from ._types import ResponseT

if TYPE_CHECKING:
    from ._base_client import SyncAPIClient, AsyncAPIClient


class Stream(Generic[ResponseT]):
    """Provides the core interface to iterate over a synchronous stream response.

    Args:
        cast_to (type[ResponseT]): The type to cast the response data to.
        response (httpx.Response): The HTTP response object.
        client (SyncAPIClient): The synchronous API client.

    Attributes:
        response (httpx.Response): The HTTP response object.

    """

    response: httpx.Response

    def __init__(
        self,
        *,
        cast_to: type[ResponseT],
        response: httpx.Response,
        client: SyncAPIClient,
    ) -> None:
        """
        Initialize a Stream instance.

        Args:
            cast_to (type[ResponseT]): The type to cast the response to.
            response (httpx.Response): The HTTP response object.
            client (SyncAPIClient): The synchronous API client.

        """
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = SSEDecoder()
        self._iterator = self.__stream__()

    def __next__(self) -> ResponseT:
        """
        Get the next item from the stream.

        Returns:
            ResponseT: The next item in the stream.

        """
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ResponseT]:
        """
        Iterate over the items in the stream.

        Yields:
            ResponseT: The next item in the stream.

        """
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[ServerSentEvent]:
        """
        Iterate over server-sent events in the response.

        Yields:
            ServerSentEvent: The next server-sent event.

        """
        yield from self._decoder.iter(self.response.iter_lines())

    def __stream__(self) -> Iterator[ResponseT]:
        """
        Iterate over the stream and process events.

        Yields:
            ResponseT: The next processed item from the stream.

        """
        cast_to = self._cast_to
        response = self.response
        process_data = self._client._process_response_data

        for sse in self._iter_events():
            if sse.event == "completion":
                yield process_data(data=sse.json(), cast_to=cast_to, response=response)

            if sse.event == "ping":
                continue

            if sse.event == "error":
                body = sse.data

                try:
                    body = sse.json()
                    err_msg = f"{body}"
                except Exception:
                    err_msg = sse.data or f"Error code: {response.status_code}"

                raise self._client._make_status_error(
                    err_msg,
                    body=body,
                    response=self.response,
                    request=self.response.request,
                )


class AsyncStream(Generic[ResponseT]):
    """
    Provides the core interface to iterate over an asynchronous stream response.

    Attributes:
        response (httpx.Response): The HTTP response object.

    """ 

    response: httpx.Response

    def __init__(
        self,
        *,
        cast_to: type[ResponseT],
        response: httpx.Response,
        client: AsyncAPIClient,
    ) -> None:
        """
        Initialize the AsyncStream instance.

        Args:
            cast_to (Type[ResponseT]): The type to cast the response to.
            response (httpx.Response): The HTTP response object.
            client (AsyncAPIClient): The asynchronous API client.

        """
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = SSEDecoder()
        self._iterator = self.__stream__()

    async def __anext__(self) -> ResponseT:
        """
        Get the next item from the asynchronous stream.

        Returns:
            ResponseT: The next item from the stream.

        """
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[ResponseT]:
        """
        Initialize an asynchronous iterator.

        Returns:
            AsyncIterator[ResponseT]: An asynchronous iterator over the stream.

        """
        async for item in self._iterator:
            yield item

    async def _iter_events(self) -> AsyncIterator[ServerSentEvent]:
        """
        Iterate over Server-Sent Events (SSE) in the response.

        Yields:
            ServerSentEvent: An SSE object from the stream.

        """
        async for sse in self._decoder.aiter(self.response.aiter_lines()):
            yield sse

    async def __stream__(self) -> AsyncIterator[ResponseT]:
        """
        Initialize an asynchronous iterator for the stream.

        Yields:
            ResponseT: An item from the asynchronous stream.

        """
        cast_to = self._cast_to
        response = self.response
        process_data = self._client._process_response_data

        async for sse in self._iter_events():
            if sse.event == "completion":
                yield process_data(data=sse.json(), cast_to=cast_to, response=response)

            if sse.event == "ping":
                continue

            if sse.event == "error":
                body = sse.data

                try:
                    body = sse.json()
                    err_msg = f"{body}"
                except Exception:
                    err_msg = sse.data or f"Error code: {response.status_code}"

                raise self._client._make_status_error(
                    err_msg,
                    body=body,
                    response=self.response,
                    request=self.response.request,
                )


class ServerSentEvent:
    """
    Represents a Server-Sent Event (SSE).

    Args:
        event (str | None, optional): The event type. Defaults to None.
        data (str | None, optional): The event data. Defaults to None.
        id (str | None, optional): The event ID. Defaults to None.
        retry (int | None, optional): The retry interval. Defaults to None.

    Attributes:
        event (str | None): The event type.
        id (str | None): The event ID.
        retry (int | None): The retry interval.
        data (str): The event data.

    """

    def __init__(
        self,
        *,
        event: str | None = None,
        data: str | None = None,
        id: str | None = None,
        retry: int | None = None,
    ) -> None:
        """
        Initialize a ServerSentEvent instance.

        Args:
            event (str | None, optional): The event type. Defaults to None.
            data (str | None, optional): The event data. Defaults to None.
            id (str | None, optional): The event ID. Defaults to None.
            retry (int | None, optional): The retry interval. Defaults to None.

        """
        if data is None:
            data = ""

        self._id = id
        self._data = data
        self._event = event or None
        self._retry = retry

    @property
    def event(self) -> str | None:
        """
        Get the event type.

        Returns:
            str | None: The event type.

        """
        return self._event

    @property
    def id(self) -> str | None:
        """
        Get the event ID.

        Returns:
            str | None: The event ID.

        """
        return self._id

    @property
    def retry(self) -> int | None:
        """
        Get the retry interval.

        Returns:
            int | None: The retry interval.

        """
        return self._retry

    @property
    def data(self) -> str:
        """
        Get the event data.

        Returns:
            str: The event data.

        """
        return self._data

    def json(self) -> Any:
        """
        Parse the event data as JSON.

        Returns:
            Any: The parsed JSON data.

        """
        return json.loads(self.data)

    def __repr__(self) -> str:
        """
        Get a string representation of the ServerSentEvent.

        Returns:
            str: A string representation of the event.

        """
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"


class SSEDecoder:
    """
    Decodes Server-Sent Event (SSE) data from a stream.

    Attributes:
        _data (list[str]): A list to store event data lines.
        _event (str | None): The current event type.
        _retry (int | None): The retry interval for reconnection.
        _last_event_id (str | None): The last event ID.

    """

    _data: list[str]
    _event: str | None
    _retry: int | None
    _last_event_id: str | None

    def __init__(self) -> None:
        """
        Initialize the SSEDecoder instance.

        """
        self._event = None
        self._data = []
        self._last_event_id = None
        self._retry = None

    def iter(self, iterator: Iterator[str]) -> Iterator[ServerSentEvent]:
        """
        Given an iterator that yields lines, iterate over it and yield every event encountered.

        Args:
            iterator (Iterator[str]): An iterator yielding lines of SSE data.

        Yields:
            ServerSentEvent: A decoded SSE event.

        """
        for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    async def aiter(self, iterator: AsyncIterator[str]) -> AsyncIterator[ServerSentEvent]:
        """
        Given an async iterator that yields lines, iterate over it and yield every event encountered.

        Args:
            iterator (AsyncIterator[str]): An async iterator yielding lines of SSE data.

        Yields:
            ServerSentEvent: A decoded SSE event.

        """
        async for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    def decode(self, line: str) -> ServerSentEvent | None:
        """
        Decode a single line of SSE data.

        Args:
            line (str): A line of SSE data.

        Returns:
            ServerSentEvent | None: A decoded SSE event or None if not a valid event line.

        """
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation

        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None

            sse = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None

            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None
    