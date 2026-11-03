"""An idle timeout that counts content, not bytes.

`timeout=` on the client bounds how long a single socket read may block. A server that keeps the
connection warm — an SSE comment (`: ping`) or a `ping` event — resets that read timer forever
without ever moving the response forward, so a stalled stream and a slow one are indistinguishable
to the caller: both wait. See #2051.

This module adds the missing bound: if no event carrying content arrives for `seconds`, the stream
raises `APITimeoutError` even though bytes are still arriving.

    stream = client.messages.create(..., stream=True)
    guard_stream(stream, seconds=30)
    for event in stream:
        ...

What counts as content: anything except an SSE comment line and a `ping` event (either
`event: ping`, or a `data:` payload whose type is `"ping"`). Everything else — including `error`
frames — resets the timer, because it is something the caller can act on.

Three properties worth stating, because they are the limits of this approach rather than bugs:

- The check runs when a chunk arrives. If the server stops sending bytes entirely, this guard never
  runs; that case belongs to the transport read timeout, which does fire when nothing arrives.
- A chunk that ends mid-frame is held in a bounded buffer so a keepalive split across two chunks is
  still recognised as a keepalive.
- Lines end where the SDK's SSE decoder says they end — at CR, LF or CRLF — and the held-back buffer
  has a hard ceiling, so a pathological stream cannot grow it without bound.
"""

from __future__ import annotations

import re
import json
import time
from typing import TYPE_CHECKING, Any, TypeVar, Iterator, Optional, AsyncIterator
from typing_extensions import override

import httpx2

from ..._exceptions import APITimeoutError

if TYPE_CHECKING:
    from ..._streaming import Stream

_T = TypeVar("_T")


# Line terminators exactly as the SDK's own SSE decoder sees them: `SSEDecoder` accumulates a whole
# event and then calls `bytes.splitlines()`, which breaks on CR, LF and CRLF and nothing else (see
# the comment above `SSEDecoder.iter_bytes`). There is no reusable per-line splitter to import, so
# the same rule is spelled out here, with CRLF as one terminator and not two.
_LINE_END = re.compile(rb"\r\n|\r|\n")

# The whole line is needed only because a `data:` payload has to be parsed to tell a
# `{"type": "ping"}` frame from a content frame. Keepalive frames are a few dozen bytes, so a line
# that grows past this is content: counting it as content costs at most one missed check on a
# pathological stream, while holding it would let the buffer grow without bound, and unbounded
# growth is what this guard exists to stop. The ceiling wins over the classification.
_MAX_PENDING = 64 * 1024


def _frame_is_keepalive(line: bytes) -> bool:
    if not line or line.startswith(b":"):
        # A comment line is what LiteLLM's proxy sends between events.
        return True
    if line.startswith(b"event:"):
        return line[6:].strip() == b"ping"
    if line.startswith(b"data:"):
        payload = line[5:].strip()
        if not payload:
            return True
        try:
            return json.loads(payload).get("type") == "ping"
        except (ValueError, AttributeError):
            return False
    # id:, retry: and unknown fields neither carry content nor end the turn.
    return True


class _KeepaliveTracker:
    """Decides, chunk by chunk, whether anything that moves the response forward arrived."""

    def __init__(self) -> None:
        self._tail = b""

    def has_content(self, chunk: bytes) -> bool:
        pending = self._tail + chunk
        self._tail = b""

        # A trailing bare CR may be the first half of a CRLF, and the next chunk may carry the LF.
        # Holding it back costs one byte; consuming it now would invent an empty line, and in SSE
        # an empty line ends an event, so the guard would be reading a different stream from the
        # decoder it is supposed to agree with.
        cut = len(pending) - 1 if pending.endswith(b"\r") else len(pending)
        complete, carry = pending[:cut], pending[cut:]

        lines = _LINE_END.split(complete)
        unfinished = lines.pop()  # bytes after the last terminator are still arriving
        self._tail = unfinished + carry

        if len(self._tail) > _MAX_PENDING:
            # A line this long is not a keepalive (see _MAX_PENDING). It has been classified as
            # content, so drop it rather than wait for a terminator that may never come.
            self._tail = b""
            return True

        return any(not _frame_is_keepalive(line) for line in lines)


class _GuardedByteStream(httpx2.SyncByteStream):
    def __init__(self, stream: httpx2.SyncByteStream, response: httpx2.Response, seconds: float) -> None:
        self._stream = stream
        self._request = response.request
        self._seconds = seconds
        self._tracker = _KeepaliveTracker()
        self.idle_timeouts = 0

    @override
    def __iter__(self) -> Iterator[bytes]:
        last_content = time.monotonic()
        for chunk in self._stream:
            now = time.monotonic()
            if self._tracker.has_content(chunk):
                last_content = now
            elif now - last_content >= self._seconds:
                self.idle_timeouts += 1
                raise APITimeoutError(request=self._request)
            yield chunk

    @override
    def close(self) -> None:
        close = getattr(self._stream, "close", None)
        if close is not None:
            close()


class _GuardedAsyncByteStream(httpx2.AsyncByteStream):
    def __init__(self, stream: httpx2.AsyncByteStream, response: httpx2.Response, seconds: float) -> None:
        self._stream = stream
        self._request = response.request
        self._seconds = seconds
        self._tracker = _KeepaliveTracker()
        self.idle_timeouts = 0

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        last_content = time.monotonic()
        async for chunk in self._stream:
            now = time.monotonic()
            if self._tracker.has_content(chunk):
                last_content = now
            elif now - last_content >= self._seconds:
                self.idle_timeouts += 1
                raise APITimeoutError(request=self._request)
            yield chunk

    @override
    async def aclose(self) -> None:
        aclose = getattr(self._stream, "aclose", None)
        if aclose is not None:
            await aclose()


def guard_stream(stream: "Stream[_T] | Any", *, seconds: float) -> "Stream[_T] | Any":
    """Make `stream` raise `APITimeoutError` if no content event arrives for `seconds`.

    Works on the response's byte stream rather than on parsed events, because the SDK discards
    keepalive frames while parsing — by the time an event reaches a caller, the information that a
    keepalive arrived is already gone.

    Returns the same object, so it can be used inline. Raises if the response has already been read.
    """
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    response = getattr(stream, "response", None)
    if response is None:
        raise TypeError("expected a stream with a .response, e.g. the result of messages.create(stream=True)")
    if getattr(response, "is_stream_consumed", False):
        raise RuntimeError("the response has already been read; guard it before iterating")

    inner = response.stream
    if isinstance(inner, _GuardedByteStream | _GuardedAsyncByteStream):
        return stream
    if isinstance(inner, httpx2.AsyncByteStream):
        response.stream = _GuardedAsyncByteStream(inner, response, seconds)
    elif isinstance(inner, httpx2.SyncByteStream):
        response.stream = _GuardedByteStream(inner, response, seconds)
    else:  # pragma: no cover - a mock without a byte stream
        raise TypeError(f"cannot guard {type(inner).__name__}")
    return stream


def idle_timeout_of(stream: Any) -> Optional[float]:
    """The guard's window on this stream, or None when it is not guarded. Useful in tests."""
    inner = getattr(getattr(stream, "response", None), "stream", None)
    return getattr(inner, "_seconds", None)
