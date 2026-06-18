from __future__ import annotations

import copy as _copy
import json
import logging
from typing import (
    Any,
    Dict,
    List,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Generator,
    AsyncIterator,
    AsyncGenerator,
    cast,
)
from contextvars import Token, ContextVar
from typing_extensions import Literal, override

import httpx

from ..._utils import is_dict
from ..._models import BaseModel
from ..._request import APIRequest
from ..._response import APIResponse, AsyncAPIResponse
from ..._streaming import Stream, AsyncStream, ServerSentEvent
from ..._exceptions import AnthropicError
from ..._middleware import CallNext, Middleware, AsyncCallNext
from ..._base_client import merge_headers
from ...types.message import Message
from .._stainless_helpers import helper_header
from ...types.beta.beta_message import BetaMessage
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_fallback_param import BetaFallbackParam

__all__ = [
    "BetaFallbackState",
    "BetaRefusalFallbackMiddleware",
]

# the documented logger name is the public package, not this private submodule
log: logging.Logger = logging.getLogger("anthropic.lib.middleware")

_MESSAGES_PATH = "/v1/messages"

DEFAULT_BETAS: tuple[AnthropicBetaParam, ...] = ("fallback-credit-2026-06-01",)
"""Betas sent by default; override with the `betas` option."""


class BetaFallbackState:
    """Tracks which fallback a sequence of requests is pinned to.

    Create one and enter it (`with state:` — the same context manager works for
    both clients) around every request that should share the pin — the turns of
    one conversation, or any wider scope the stickiness should apply to;
    `BetaRefusalFallbackMiddleware` mutates it in place when a model refuses.
    """

    index: int | None
    """Index into the fallback chain the requests are pinned to.

    `None` (or -1) targets the original request params; the middleware sets it
    to the index of the fallback that accepted the request.
    """

    def __init__(self) -> None:
        self.index = None

    def __enter__(self) -> BetaFallbackState:
        token = _fallback_state.set(self)
        _fallback_state_tokens.set((*_fallback_state_tokens.get(), token))
        return self

    def __exit__(self, *exc_info: object) -> None:
        tokens = _fallback_state_tokens.get()
        _fallback_state_tokens.set(tokens[:-1])
        _fallback_state.reset(tokens[-1])


_fallback_state: ContextVar[BetaFallbackState | None] = ContextVar("anthropic_beta_fallback_state", default=None)

# The reset tokens for every `with state:` block the current context is inside,
# innermost last. Kept in a ContextVar — NOT on the state instance — so that one
# state shared across threads/tasks (the documented usage) has each context
# entering and exiting with its own tokens; a `Token` can only be reset in the
# context that created it.
_fallback_state_tokens: ContextVar[tuple[Token[BetaFallbackState | None], ...]] = ContextVar(
    "anthropic_beta_fallback_state_tokens", default=()
)


class BetaRefusalFallbackMiddleware(Middleware):
    """Middleware that retries refused beta `/v1/messages` requests down a
    fallback chain, reproducing the server-side `fallbacks` wire shape
    client-side.

    Only `client.beta.messages` requests are handled — refusals minted by the
    first-party `client.messages` surface carry no `fallback_credit_token`, so
    those requests pass through untouched.

    Non-streaming: when a response comes back with `stop_reason: "refusal"`, the
    request is retried with each entry of `fallbacks` merged over the original
    params — passing along the refusal's `fallback_credit_token` when it minted
    one — until a model accepts or the chain is exhausted. A `fallback` seam
    block per model boundary is prepended to the served message's content —
    the same block shape the streaming splice emits. The served hop's `usage`
    is left verbatim (streaming rewrites it to per-hop `usage.iterations`).

    Streaming: when the stream ends in `stop_reason: "refusal"`, a second
    request is issued to the fallback model. It carries the refusal's
    `fallback_credit_token`, plus the refused model's partial output as a
    trailing assistant prefill when the refusal grants one
    (`fallback_has_prefill_claim`). The fallback's events are then spliced onto
    the still-open stream, so the client sees one continuous message in the
    server-side `fallbacks` wire shape: a `fallback` content block at each
    model boundary, monotonic block indices, and per-hop `usage.iterations` on
    the final `message_delta`. A refusal before any output streamed retries
    even without a credit token, and the serving hop's `message_start` opens
    the wire carrying the primary's message id.

    The fallback-credit beta the credit tokens require is sent by default on
    every request the middleware handles; the `betas` option controls this.

    In both modes a fallback that itself refuses with a fresh credit token
    continues down the chain. A streaming fallback whose appended prefill the
    server rejects (HTTP 400 body mismatch) is retried once without it; a
    fallback whose request fails outright is skipped — its token was never
    redeemed, so it carries to the next entry. When every remaining entry fails
    over HTTP, the suppressed refusal is replayed to the client with
    `recommended_model` stamped from the final failure (the failed model for
    capacity errors, `null` otherwise). A refusal surfaced to the client rather
    than retried is reported through the `anthropic.lib.middleware` logger.

    To keep later requests on the model that accepted, run them inside a shared
    `BetaFallbackState` context; requests sharing that state start directly at
    the pinned fallback. Reuse one state across whatever scope the pin should
    apply to — typically a conversation. The state is the only pin: `fallback`
    seam blocks replayed in the request history are stripped from the outgoing
    request (an assistant turn left empty by the strip is dropped whole), never
    read back as a pin.

    ```py
    client = Anthropic(middleware=[BetaRefusalFallbackMiddleware([{"model": "claude-opus-4-8"}])])

    state = BetaFallbackState()
    with state:
        message = client.beta.messages.create(**params)
    ```
    """

    def __init__(
        self,
        fallbacks: Iterable[BetaFallbackParam],
        *,
        betas: Iterable[AnthropicBetaParam] | None = None,
    ) -> None:
        """
        Args:
            fallbacks: The fallback chain, tried in order. An empty chain disables
                the middleware.

            betas: Betas added to the `anthropic-beta` header of every `/v1/messages`
                request this middleware handles — the original request included, since
                refusals only carry a `fallback_credit_token` when the beta is enabled.
                Defaults to `("fallback-credit-2026-06-01",)`; pass `()` to send none.
        """
        self._fallbacks = tuple(fallbacks)
        self._betas = DEFAULT_BETAS if betas is None else tuple(betas)
        self._warned_missing_state = False

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> APIResponse[Any]:
        body = self._applicable_body(request)
        if body is None:
            return call_next(request)

        state = _fallback_state.get()
        start_index = self._start_index(state)
        pin = self._make_pin(state)

        # Send the configured betas on this and every hop request derived from it,
        # and tag this and every hop with the middleware's helper telemetry.
        request = _with_middleware_headers(request, self._betas)

        # The seam blocks this middleware splices into streams are client-side
        # markers — the server rejects them as unknown tags — so a history that
        # replays them is rewritten without them.
        body = _strip_seam_blocks(body)
        initial_body = body if start_index == -1 else {**body, **self._fallbacks[start_index]}
        initial_request = request.copy(body=initial_body)

        response = call_next(initial_request)
        if not response.http_response.is_success:
            return response

        if request.stream:
            first_hop = start_index + 1
            # Splicing needs at least one entry left to hop to; otherwise the
            # stream passes through untouched.
            if first_hop >= len(self._fallbacks):
                return response
            return self._splice_fallback_stream(
                request=initial_request,
                body=initial_body,
                response=response,
                call_next=call_next,
                first_hop=first_hop,
                pin=pin,
            )

        index = start_index
        res = response
        from_model = str(initial_body.get("model") or "")
        seams: list[dict[str, Any]] = []
        while index < len(self._fallbacks) - 1 and res.http_response.is_success:
            message = res.parse()
            if not isinstance(message, (Message, BetaMessage)) or message.stop_reason != "refusal":
                break

            index += 1
            pin(index)
            token = _credit_token(message)
            category = _refusal_category(message)
            res = call_next(request.copy(body=_merged_body(body, self._fallbacks[index], token)))
            if res.http_response.is_success:
                to_model = str(self._fallbacks[index]["model"])
                seams.append(_seam_block(from_model, to_model, category))
                from_model = to_model

        if seams and res.http_response.is_success:
            served = res.parse()
            if isinstance(served, (Message, BetaMessage)) and served.stop_reason != "refusal":
                # Prepend one `fallback` seam block per model boundary to the
                # serving hop's content — the same block shape the streaming
                # splice emits.
                return _prepend_seam_blocks(res, seams)
        return res

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> AsyncAPIResponse[Any]:
        body = self._applicable_body(request)
        if body is None:
            return await call_next(request)

        state = _fallback_state.get()
        start_index = self._start_index(state)
        pin = self._make_pin(state)

        # Send the configured betas on this and every hop request derived from it,
        # and tag this and every hop with the middleware's helper telemetry.
        request = _with_middleware_headers(request, self._betas)

        # The seam blocks this middleware splices into streams are client-side
        # markers — the server rejects them as unknown tags — so a history that
        # replays them is rewritten without them.
        body = _strip_seam_blocks(body)
        initial_body = body if start_index == -1 else {**body, **self._fallbacks[start_index]}
        initial_request = request.copy(body=initial_body)

        response = await call_next(initial_request)
        if not response.http_response.is_success:
            return response

        if request.stream:
            first_hop = start_index + 1
            # Splicing needs at least one entry left to hop to; otherwise the
            # stream passes through untouched.
            if first_hop >= len(self._fallbacks):
                return response
            return self._splice_fallback_stream_async(
                request=initial_request,
                body=initial_body,
                response=response,
                call_next=call_next,
                first_hop=first_hop,
                pin=pin,
            )

        index = start_index
        res = response
        from_model = str(initial_body.get("model") or "")
        seams: list[dict[str, Any]] = []
        while index < len(self._fallbacks) - 1 and res.http_response.is_success:
            message = await res.parse()
            if not isinstance(message, (Message, BetaMessage)) or message.stop_reason != "refusal":
                break

            index += 1
            pin(index)
            token = _credit_token(message)
            category = _refusal_category(message)
            res = await call_next(request.copy(body=_merged_body(body, self._fallbacks[index], token)))
            if res.http_response.is_success:
                to_model = str(self._fallbacks[index]["model"])
                seams.append(_seam_block(from_model, to_model, category))
                from_model = to_model

        if seams and res.http_response.is_success:
            served = await res.parse()
            if isinstance(served, (Message, BetaMessage)) and served.stop_reason != "refusal":
                # Prepend one `fallback` seam block per model boundary to the
                # serving hop's content — the same block shape the streaming
                # splice emits.
                return _prepend_seam_blocks_async(res, seams)
        return res

    def _applicable_body(self, request: APIRequest) -> dict[str, Any] | None:
        """The request's JSON body when this middleware applies to it, `None` otherwise."""
        body = _as_dict(request.json)
        url = httpx.URL(request.url)
        if (
            # an empty chain disables this middleware
            not self._fallbacks
            # this middleware only applies to the beta messages API
            # (`client.beta.messages`, marked by the `beta=true` query param) —
            # only the beta surface mints fallback credit tokens
            or request.method.lower() != "post"
            or url.path != _MESSAGES_PATH
            or url.params.get("beta") != "true"
            or body is None
        ):
            return None
        if body.get("fallbacks") is not None:
            raise AnthropicError(
                "Sending the `fallbacks:` request param is not supported when using the "
                "`BetaRefusalFallbackMiddleware`. You should either remove the middleware and send `fallbacks:` with the "
                "`server-side-fallback-2026-06-01` beta header to let the API handle refusal fallbacks, or omit the "
                "`fallbacks:` param if you'd like `BetaRefusalFallbackMiddleware` to handle "
                "fallbacks on the client side."
            )
        return body

    def _start_index(self, state: BetaFallbackState | None) -> int:
        """The chain entry this request starts at (-1 = the original params).

        Only an explicit `BetaFallbackState` pin moves the start; without one
        the request starts at the original params.
        """
        if state is None or state.index is None:
            return -1
        start_index = state.index
        if not -1 <= start_index < len(self._fallbacks):
            raise AnthropicError(
                f"BetaFallbackState.index {start_index} is out of bounds for a chain of "
                f"{len(self._fallbacks)} fallback(s); was the state shared with a different middleware?"
            )
        return start_index

    def _make_pin(self, state: BetaFallbackState | None) -> Callable[[int], None]:
        """Pin requests sharing the state to the entry being tried (or warn that there is none)."""

        def pin(index: int) -> None:
            if state is not None:
                state.index = index
            elif not self._warned_missing_state:
                self._warned_missing_state = True
                log.warning(
                    "anthropic-sdk: BetaRefusalFallbackMiddleware fell back without an active "
                    "BetaFallbackState; follow-up requests will retry models that already refused. "
                    "Run them inside a shared `with BetaFallbackState():` block to pin them to the "
                    "accepted model."
                )

        return pin

    def _splice_fallback_stream(
        self,
        *,
        request: APIRequest,
        body: dict[str, Any],
        response: APIResponse[Any],
        call_next: CallNext,
        first_hop: int,
        pin: Callable[[int], None],
    ) -> APIResponse[Any]:
        """Wrap the refusable stream in a response whose body passes events through
        until a retryable refusal, then splices the fallback chain's events on.

        Closing the returned response (or the `Stream` parsed from it) tears down
        whichever stream is being read and abandons any in-flight fallback request.
        """
        frames = self._spliced_frames(
            request=request,
            body=body,
            response=response,
            call_next=call_next,
            first_hop=first_hop,
            pin=pin,
        )
        return APIResponse(
            raw=_spliced_http_response(response.http_response, _FrameByteStream(frames)),
            cast_to=response._cast_to,
            client=response._client,
            stream=True,
            stream_cls=response._stream_cls,
            options=response._options,
            retries_taken=response.retries_taken,
        )

    def _splice_fallback_stream_async(
        self,
        *,
        request: APIRequest,
        body: dict[str, Any],
        response: AsyncAPIResponse[Any],
        call_next: AsyncCallNext,
        first_hop: int,
        pin: Callable[[int], None],
    ) -> AsyncAPIResponse[Any]:
        frames = self._spliced_frames_async(
            request=request,
            body=body,
            response=response,
            call_next=call_next,
            first_hop=first_hop,
            pin=pin,
        )
        return AsyncAPIResponse(
            raw=_spliced_http_response(response.http_response, _AsyncFrameByteStream(frames)),
            cast_to=response._cast_to,
            client=response._client,
            stream=True,
            stream_cls=response._stream_cls,
            options=response._options,
            retries_taken=response.retries_taken,
        )

    # --- streaming fallback (credit-token continuation) -------------------------
    #
    # The retry uses the appended-assistant form documented on
    # `fallback_credit_token`: the refused request's body, extended by one
    # trailing assistant turn carrying the refused model's partial output. The
    # token authorizes that turn as a prefill continuation and applies the
    # fallback credit. The refusal's `fallback_has_prefill_claim` says whether
    # the partial output may be resent: when true the accumulated blocks are
    # appended (trailing thinking blocks stripped — an assistant turn cannot
    # end in one); when false the refused hop's output is dropped and the
    # token is redeemed against the same body.
    #
    # Wire-shape rules (pinned by the fable-fallback conformance suites):
    #
    # * A refusal that arrives MID-STREAM keeps the primary's `message_start`
    #   on the wire; the seam block's `to.model` carries the serving model.
    #   A refusal BEFORE any output (pre-stream) holds the wire instead: the
    #   serving hop's `message_start` opens it, with its `id` rewritten to the
    #   primary's, followed by one queued seam per hop that was reached.
    # * The seam's `from.model` echoes the model string the caller sent (alias
    #   or canonical) while the declining hop is the requested model; fallback
    #   hops use their entry's model id.
    # * A hop's seam is emitted only once its response arrives OK — a hop whose
    #   request fails over HTTP was never reached and leaves no seam and no
    #   iterations entry; its token and continuation carry to the next entry.
    # * Refusal text streamed before the refusal stays in the message and is
    #   resent as-is — the appended turn must match the partial output verbatim.

    def _spliced_frames(
        self,
        *,
        request: APIRequest,
        body: dict[str, Any],
        response: APIResponse[Any],
        call_next: CallNext,
        first_hop: int,
        pin: Callable[[int], None],
    ) -> Generator[bytes, None, None]:
        fallbacks = self._fallbacks
        # the response whose body is currently being consumed; closed on teardown
        current: httpx.Response | None = response.http_response

        try:
            # --- stream A: pass through until a chainable refusal ---
            stream_a = response.http_response
            reader = _HopReader(
                index_base=0,
                # the caller guarantees first_hop < len(fallbacks)
                has_next=True,
                splice=None,
                wire_open=False,
                primary_id=None,
                seam_frames=[],
            )
            outcome = yield from _drive_hop(stream_a, reader)
            if outcome.refused is None:
                return  # non-refusal or not-retryable: pure pass-through.
            stream_a.close()
            current = None

            # --- fallback chain: try each entry in order ---
            chain = _ChainState.begin(body, outcome)

            for hop in range(first_hop, len(fallbacks)):
                entry = fallbacks[hop]
                model = str(entry["model"])
                has_next = hop + 1 < len(fallbacks)
                pin(hop)

                # --- build the request: appended-assistant continuation ---
                # First attempt carries the newest partial appended (when its
                # refusal granted a prefill claim); a 400 on that form is taken
                # as the server rejecting the prefill, so the hop is retried
                # once without it — the same-body form the token always
                # supports.
                continuation = chain.continuation()
                res_b: APIResponse[Any] | None = None
                failure: _HopFailure | None = None
                for attempt in range(2):
                    hop_request = request.copy(body=chain.hop_body(entry, continuation))
                    try:
                        res_b = call_next(hop_request)
                    except Exception as err:
                        log.error(
                            "anthropic-sdk: BetaRefusalFallbackMiddleware: fallback request to %s failed: %s",
                            model,
                            err,
                        )
                        failure = _HopFailure(model=model, status=None)
                        break
                    if res_b.http_response.is_success:
                        current = res_b.http_response
                        break
                    err_body = _read_json(res_b.http_response)
                    res_b.http_response.close()
                    if attempt == 0 and res_b.status_code == 400 and continuation:
                        log.warning(
                            "anthropic-sdk: BetaRefusalFallbackMiddleware: fallback request with the "
                            "partial output appended was rejected (HTTP 400: %s); retrying without it",
                            _json_dumps(err_body),
                        )
                        continuation = chain.base
                        res_b = None
                        continue
                    log.error(
                        "anthropic-sdk: BetaRefusalFallbackMiddleware: fallback request to %s failed: HTTP %s: %s",
                        model,
                        res_b.status_code,
                        _json_dumps(err_body),
                    )
                    failure = _HopFailure(model=model, status=res_b.status_code)
                    break

                if failure is not None:
                    # The token was never redeemed — retry it against the next entry.
                    if has_next:
                        continue
                    # Every remaining entry failed: degrade to the suppressed
                    # refusal, stamped with the final failure's recommendation.
                    for frame in chain.terminal_failure_frames(failure):
                        yield frame
                    return

                # --- splice: queued seam, monotonic indices, usage.iterations ---
                assert res_b is not None
                hop_response = res_b.http_response
                chain.queue_seam(model)
                reader = _HopReader(
                    index_base=chain.next_index,
                    has_next=has_next,
                    splice=_SpliceInfo(iterations=chain.iterations, model=model),
                    wire_open=chain.wire_open,
                    primary_id=chain.primary_id,
                    seam_frames=chain.pending_seam_frames(),
                )
                outcome = yield from _drive_hop(hop_response, reader)
                if outcome.opened:
                    chain.mark_opened()
                if outcome.refused is None:
                    return
                hop_response.close()
                current = None

                # This hop refused too: its emitted partial (if any) stays in
                # the client's message, becomes the next partial segment, and
                # the chain continues.
                chain.absorb_refusal(outcome, model, continuation)
        finally:
            if current is not None:
                current.close()

    async def _spliced_frames_async(
        self,
        *,
        request: APIRequest,
        body: dict[str, Any],
        response: AsyncAPIResponse[Any],
        call_next: AsyncCallNext,
        first_hop: int,
        pin: Callable[[int], None],
    ) -> AsyncGenerator[bytes, None]:
        fallbacks = self._fallbacks
        # the response whose body is currently being consumed; closed on teardown
        current: httpx.Response | None = response.http_response

        try:
            # --- stream A: pass through until a chainable refusal ---
            stream_a = response.http_response
            reader = _HopReader(
                index_base=0,
                # the caller guarantees first_hop < len(fallbacks)
                has_next=True,
                splice=None,
                wire_open=False,
                primary_id=None,
                seam_frames=[],
            )
            async for frame in _drive_hop_async(stream_a, reader):
                yield frame
            outcome = reader.finish()
            if outcome.refused is None:
                return  # non-refusal or not-retryable: pure pass-through.
            await stream_a.aclose()
            current = None

            chain = _ChainState.begin(body, outcome)

            for hop in range(first_hop, len(fallbacks)):
                entry = fallbacks[hop]
                model = str(entry["model"])
                has_next = hop + 1 < len(fallbacks)
                pin(hop)

                continuation = chain.continuation()
                res_b: AsyncAPIResponse[Any] | None = None
                failure: _HopFailure | None = None
                for attempt in range(2):
                    hop_request = request.copy(body=chain.hop_body(entry, continuation))
                    try:
                        res_b = await call_next(hop_request)
                    except Exception as err:
                        log.error(
                            "anthropic-sdk: BetaRefusalFallbackMiddleware: fallback request to %s failed: %s",
                            model,
                            err,
                        )
                        failure = _HopFailure(model=model, status=None)
                        break
                    if res_b.http_response.is_success:
                        current = res_b.http_response
                        break
                    err_body = await _read_json_async(res_b.http_response)
                    await res_b.http_response.aclose()
                    if attempt == 0 and res_b.status_code == 400 and continuation:
                        log.warning(
                            "anthropic-sdk: BetaRefusalFallbackMiddleware: fallback request with the "
                            "partial output appended was rejected (HTTP 400: %s); retrying without it",
                            _json_dumps(err_body),
                        )
                        continuation = chain.base
                        res_b = None
                        continue
                    log.error(
                        "anthropic-sdk: BetaRefusalFallbackMiddleware: fallback request to %s failed: HTTP %s: %s",
                        model,
                        res_b.status_code,
                        _json_dumps(err_body),
                    )
                    failure = _HopFailure(model=model, status=res_b.status_code)
                    break

                if failure is not None:
                    # The token was never redeemed — retry it against the next entry.
                    if has_next:
                        continue
                    for frame in chain.terminal_failure_frames(failure):
                        yield frame
                    return

                assert res_b is not None
                hop_response = res_b.http_response
                chain.queue_seam(model)
                reader = _HopReader(
                    index_base=chain.next_index,
                    has_next=has_next,
                    splice=_SpliceInfo(iterations=chain.iterations, model=model),
                    wire_open=chain.wire_open,
                    primary_id=chain.primary_id,
                    seam_frames=chain.pending_seam_frames(),
                )
                async for frame in _drive_hop_async(hop_response, reader):
                    yield frame
                outcome = reader.finish()
                if outcome.opened:
                    chain.mark_opened()
                if outcome.refused is None:
                    return
                await hop_response.aclose()
                current = None

                chain.absorb_refusal(outcome, model, continuation)
        finally:
            if current is not None:
                await current.aclose()


# --- hop consumption ---------------------------------------------------------


class _Refusal(BaseModel):
    token: Optional[str]
    """The minted credit token; `None` for a token-less start-of-stream refusal."""

    category: Optional[str]
    """The policy category that triggered the refusal; `None` when not surfaced."""

    has_prefill_claim: bool
    usage: Dict[str, Any]
    event: Dict[str, Any]
    """The suppressed refusal `message_delta` event, verbatim — replayed if every
    remaining entry fails over HTTP."""


class _SpliceInfo(BaseModel):
    """Splice context for fallback hops; `None` for stream A."""

    iterations: List[Dict[str, Any]]
    model: str


class _HopFailure(BaseModel):
    """A fallback hop whose request failed; stamps `recommended_model` when it
    ends the chain."""

    model: str
    status: Optional[int]
    """The HTTP status, or `None` when the request raised instead of resolving."""


class _HopOutcome(BaseModel):
    """The outcome of consuming one hop's stream."""

    refused: Optional[_Refusal]
    """Set when the hop refused and an entry remained to chain to."""

    model: Optional[str]
    """The hop's serving model, from its message_start."""

    start_event: Optional[Dict[str, Any]]
    """The hop's message_start event, parsed."""

    blocks: List[Dict[str, Any]]
    """The hop's accumulated content blocks, in start order — the next partial segment."""

    next_index: int
    """One past the highest (shifted) block index emitted — where the next boundary goes."""

    opened: bool
    """Whether this hop emitted output (its frames opened or continued the wire)."""

    last_fallback_to: Optional[str]
    """`to.model` of the last `fallback` seam block seen in this hop's stream —
    a server-stitched envelope's last decliner."""


class _HopReader:
    """Consumes one hop's SSE events, producing the frames to forward to the
    client while accumulating its content blocks.

    Events are held until the hop produces output (a content block or a
    terminal event), so a refusal that arrives before any output — a pre-stream
    decline — leaves no trace on the wire and chains silently. On open, stream
    A's held `message_start` is flushed in its original wire bytes; a spliced
    hop's is suppressed when the wire is already open, or emitted with its `id`
    rewritten to the primary's when this hop's start opens the wire. Queued
    seam frames for every hop reached so far are flushed right after.

    A spliced hop has its block indices shifted by `index_base` and its
    terminal message_delta's usage rewritten to the `usage.iterations` chain
    shape.

    A refusal that can be chained — an entry remains, and either a
    `fallback_credit_token` was minted or nothing has streamed yet — ends the
    hop early: open blocks are closed, the terminal message_delta +
    message_stop are suppressed, and the refusal is set on the outcome so the
    caller can issue the next hop. Any other refusal is logged and passes
    through to the client.
    """

    outcome: _HopOutcome | None
    """Set when a chainable refusal ended the hop early; the driver stops feeding."""

    def __init__(
        self,
        *,
        index_base: int,
        has_next: bool,
        splice: _SpliceInfo | None,
        wire_open: bool,
        primary_id: str | None,
        seam_frames: list[bytes],
    ) -> None:
        self._tracker = _BlockTracker(index_base)
        self._has_next = has_next
        self._splice = splice
        self._wire_open = wire_open
        self._primary_id = primary_id
        self._seam_frames = seam_frames
        self._model: str | None = None
        self._start_usage: dict[str, Any] | None = None
        self._start_event: dict[str, Any] | None = None
        self._held_start: ServerSentEvent | None = None
        self._held: list[ServerSentEvent] = []
        self._opened = False
        self._last_fallback_to: str | None = None
        self.outcome = None

    @property
    def opened(self) -> bool:
        return self._opened

    def feed(self, sse: ServerSentEvent) -> list[bytes]:
        """Process one event, returning the frames to forward for it."""
        event = _as_dict(_safe_json(sse.data))
        event_type = event.get("type") if event is not None else None
        splice = self._splice

        if event_type == "message_start" and event is not None:
            message = _as_dict(event.get("message"))
            if message is not None:
                model = message.get("model")
                self._model = model if isinstance(model, str) else None
                self._start_usage = _as_dict(message.get("usage"))
            self._start_event = event
            self._held_start = sse
            return []
        elif event_type == "content_block_start" and event is not None:
            frames = self._open()
            content_block = _as_dict(event.get("content_block"))
            if content_block is not None and content_block.get("type") == "fallback":
                to = _as_dict(content_block.get("to"))
                to_model = to.get("model") if to is not None else None
                if isinstance(to_model, str):
                    self._last_fallback_to = to_model
            self._tracker.start(event)
            return (
                [*frames, _emit("content_block_start", event)]
                if splice is not None
                else [*frames, _passthrough_sse(sse)]
            )
        elif event_type == "content_block_delta" and event is not None:
            frames = self._open()
            self._tracker.delta(event)
            return (
                [*frames, _emit("content_block_delta", event)]
                if splice is not None
                else [*frames, _passthrough_sse(sse)]
            )
        elif event_type == "content_block_stop" and event is not None:
            frames = self._open()
            self._tracker.stop(event)
            return (
                [*frames, _emit("content_block_stop", event)]
                if splice is not None
                else [*frames, _passthrough_sse(sse)]
            )
        elif event_type == "message_delta" and event is not None:
            delta = _as_dict(event.get("delta")) or {}
            if delta.get("stop_reason") == "refusal":
                stop_details = _as_dict(delta.get("stop_details"))
                details = stop_details if stop_details is not None and stop_details.get("type") == "refusal" else None
                token = details.get("fallback_credit_token") if details is not None else None
                token = token if isinstance(token, str) and token else None
                pre_stream = not self._opened and not self._tracker.content_blocks()
                # A mid-stream refusal chains only when it minted a credit token;
                # a pre-stream refusal chains even without one — nothing has
                # streamed, so the retry is free and invisible.
                if self._has_next and (token is not None or pre_stream):
                    usage = _backfill(_as_dict(event.get("usage")), self._start_usage)
                    frames = list(self._tracker.close_open_blocks())
                    # suppress this hop's message_delta + message_stop (and, for a
                    # pre-stream decline, everything held before them)
                    self._held_start = None
                    self._held.clear()
                    self.outcome = _HopOutcome(
                        refused=_Refusal(
                            token=token,
                            category=details.get("category") if details is not None else None,
                            has_prefill_claim=details is not None and details.get("fallback_has_prefill_claim") is True,
                            usage=usage,
                            event=event,
                        ),
                        model=self._model,
                        start_event=self._start_event,
                        blocks=self._tracker.content_blocks(),
                        next_index=self._tracker.next_index,
                        opened=self._opened,
                        last_fallback_to=self._last_fallback_to,
                    )
                    return frames
                if not token:
                    log.error(
                        "anthropic-sdk: BetaRefusalFallbackMiddleware: refusal stop_details has no "
                        "fallback_credit_token; surfacing the refusal"
                    )
                else:
                    log.error(
                        "anthropic-sdk: BetaRefusalFallbackMiddleware: refusal but no fallback "
                        "entries remain; surfacing the refusal"
                    )
            frames = self._open()
            if splice is not None:
                if delta.get("stop_reason") == "refusal":
                    # the terminal refusal's stop_details always carries a model
                    # recommendation slot in the stitched shape
                    stop_details = _as_dict(delta.get("stop_details"))
                    if stop_details is not None:
                        stop_details.setdefault("recommended_model", None)
                # Terminal hop. Replace iterations, don't append: this hop's own
                # message_delta self-reports its iterations without a `model` (a
                # fresh non-fallback request doesn't know it served a chain).
                # Server-side `fallbacks` relabels the whole chain instead —
                # refused hops as `message`, the serving hop as
                # `fallback_message` — so the recorded chain replaces the
                # self-report, with this hop's own entry relabeled as the
                # `fallback_message` completer.
                usage = _as_dict(event.get("usage")) or {}
                usage["iterations"] = [
                    *splice.iterations,
                    _serving_iteration_entry(usage, splice.model),
                ]
                event["usage"] = usage
                return [*frames, _emit("message_delta", event)]
            return [*frames, _passthrough_sse(sse)]

        if not self._opened:
            # ping, error, unrecognised — held until the wire-open decision
            self._held.append(sse)
            return []
        # message_stop, ping, error, unrecognised — and for stream A every
        # event — pass through in their original wire bytes.
        return [_passthrough_sse(sse)]

    def _open(self) -> list[bytes]:
        """Open the wire for this hop: its message_start (raw for stream A;
        suppressed or id-rewritten for a spliced hop), the queued seam frames,
        then anything else held."""
        if self._opened:
            return []
        self._opened = True
        frames: list[bytes] = []
        if self._splice is None:
            if self._held_start is not None:
                frames.append(_passthrough_sse(self._held_start))
        elif not self._wire_open and self._start_event is not None:
            start_event = _copy.deepcopy(self._start_event)
            message = _as_dict(start_event.get("message"))
            if message is not None and self._primary_id is not None:
                message["id"] = self._primary_id
            frames.append(_emit("message_start", start_event))
        frames.extend(self._seam_frames)
        frames.extend(_passthrough_sse(held) for held in self._held)
        self._held_start = None
        self._held.clear()
        return frames

    def finish_frames(self) -> list[bytes]:
        """Frames still owed when the stream ends without a chainable refusal."""
        if self.outcome is not None or self._opened:
            return []
        return self._open()

    def finish(self) -> _HopOutcome:
        """The outcome once the hop's stream is fully consumed (or cut early)."""
        if self.outcome is not None:
            return self.outcome
        return _HopOutcome(
            refused=None,
            model=self._model,
            start_event=self._start_event,
            blocks=self._tracker.content_blocks(),
            next_index=self._tracker.next_index,
            opened=self._opened,
            last_fallback_to=self._last_fallback_to,
        )


def _drive_hop(response: httpx.Response, reader: _HopReader) -> Generator[bytes, None, _HopOutcome]:
    """Feed one hop's SSE events through `reader`, yielding the frames to forward."""
    for sse in Stream.raw_events(response):
        for frame in reader.feed(sse):
            yield frame
        if reader.outcome is not None:
            break
    for frame in reader.finish_frames():
        yield frame
    return reader.finish()


async def _drive_hop_async(response: httpx.Response, reader: _HopReader) -> AsyncIterator[bytes]:
    """Feed one hop's SSE events through `reader`, yielding the frames to forward.

    The outcome is read from `reader.finish()` afterwards — async generators
    cannot return a value.
    """
    async for sse in AsyncStream.raw_events(response):
        for frame in reader.feed(sse):
            yield frame
        if reader.outcome is not None:
            break
    for frame in reader.finish_frames():
        yield frame


class _ChainState:
    """Bookkeeping shared across the hops of one spliced stream."""

    next_index: int
    """Monotonic block index across all spliced streams."""

    wire_open: bool
    """Whether a message_start has reached the client yet."""

    primary_id: str | None
    """The primary's message id — stamped onto the message_start that opens the
    wire when the primary declined pre-stream."""

    primary_model: str
    """The model string the caller sent, alias or canonical — echoed by the first
    seam's `from.model` and the first iterations entry."""

    token: str | None
    base: List[Any]
    partial: List[Any]
    from_model: str
    last_refusal: _Refusal
    last_start_event: Dict[str, Any] | None
    iterations: List[Dict[str, Any]]
    """One `message` entry per hop that was reached and declined, in order — the
    primary first. Failed hops are skipped (no usage came back); the serving hop
    is appended as `fallback_message` when its message_delta arrives."""

    def __init__(self, body: dict[str, Any]) -> None:
        self._body = body
        self._pending_seams: list[bytes] = []

    @classmethod
    def begin(cls, body: dict[str, Any], outcome: _HopOutcome) -> _ChainState:
        """The chain state after stream A's chainable refusal."""
        assert outcome.refused is not None
        chain = cls(body)
        chain.primary_model = str(body.get("model") or "")
        chain.next_index = outcome.next_index
        chain.wire_open = outcome.opened
        start_message = _as_dict((outcome.start_event or {}).get("message"))
        start_id = start_message.get("id") if start_message is not None else None
        chain.primary_id = start_id if isinstance(start_id, str) else None
        chain.token = outcome.refused.token
        chain.base = []
        chain.partial = _to_prefill_blocks(outcome.blocks) if outcome.refused.has_prefill_claim else []
        # A server-stitched envelope's last decliner is the model the first
        # client-side seam hands off from; a plain stream hands off from the
        # caller-spelled primary.
        chain.from_model = outcome.last_fallback_to or chain.primary_model
        chain.last_refusal = outcome.refused
        chain.last_start_event = outcome.start_event
        chain.iterations = _declined_iteration_entries(outcome.refused, chain.primary_model)
        return chain

    def queue_seam(self, to_model: str) -> None:
        """Queue the reached hop's `fallback` seam block at the next monotonic index.

        Queued seams are flushed by the hop reader once output reaches the wire,
        so a chain of pre-stream declines lines its seams up after the serving
        hop's message_start.
        """
        seam_index = self.next_index
        self.next_index += 1
        self._pending_seams.extend(
            [
                _emit(
                    "content_block_start",
                    {
                        "type": "content_block_start",
                        "index": seam_index,
                        "content_block": _seam_block(self.from_model, to_model, self.last_refusal.category),
                    },
                ),
                _emit("content_block_stop", {"type": "content_block_stop", "index": seam_index}),
            ]
        )
        self.from_model = to_model

    def pending_seam_frames(self) -> list[bytes]:
        return list(self._pending_seams)

    def mark_opened(self) -> None:
        self.wire_open = True
        self._pending_seams.clear()

    def continuation(self) -> list[Any]:
        return [*self.base, *self.partial]

    def hop_body(self, entry: BetaFallbackParam, continuation: list[Any]) -> dict[str, Any]:
        """The hop's request body: the refused request's, with the entry's
        overrides merged over it and extended by the continuation.

        The server-side `fallbacks` param is stripped — it is mutually exclusive
        with a credit-token retry. When the refusal granted no prefill claim the
        appended turn is omitted entirely and the same-body form is sent.
        """
        body: dict[str, Any] = {key: value for key, value in {**self._body, **entry}.items() if key != "fallbacks"}
        if self.token is not None:
            body["fallback_credit_token"] = self.token
        if continuation:
            messages = body.get("messages")
            body["messages"] = [
                *(messages if isinstance(messages, list) else []),
                {"role": "assistant", "content": continuation},
            ]
        return body

    def absorb_refusal(self, outcome: _HopOutcome, model: str, continuation: list[Any]) -> None:
        """Fold a refused hop's outcome in, readying the next hop."""
        assert outcome.refused is not None
        self.token = outcome.refused.token
        self.base = continuation
        self.partial = _to_prefill_blocks(outcome.blocks) if outcome.refused.has_prefill_claim else []
        self.iterations.extend(_declined_iteration_entries(outcome.refused, model))
        self.last_refusal = outcome.refused
        if outcome.start_event is not None:
            self.last_start_event = outcome.start_event
        self.next_index = outcome.next_index

    def terminal_failure_frames(self, failure: _HopFailure) -> list[bytes]:
        """Degrade to the suppressed refusal when every remaining entry failed
        over HTTP: replay its message_delta verbatim — `recommended_model`
        stamped from the final failure (the failed model for capacity errors,
        `null` otherwise) and `usage.iterations` carrying the recorded chain —
        then message_stop.
        """
        frames: list[bytes] = []
        if not self.wire_open and self.last_start_event is not None:
            start_event = _copy.deepcopy(self.last_start_event)
            message = _as_dict(start_event.get("message"))
            if message is not None and self.primary_id is not None:
                message["id"] = self.primary_id
            frames.append(_emit("message_start", start_event))
        frames.extend(self._pending_seams)

        event = _copy.deepcopy(self.last_refusal.event)
        delta = _as_dict(event.get("delta"))
        if delta is not None:
            details = _as_dict(delta.get("stop_details"))
            if details is not None:
                details["recommended_model"] = failure.model if failure.status in (429, 529) else None
        usage = _as_dict(event.get("usage")) or {}
        usage["iterations"] = _copy.deepcopy(self.iterations)
        event["usage"] = usage
        frames.append(_emit("message_delta", event))
        frames.append(_emit("message_stop", {"type": "message_stop"}))
        return frames


def _declined_iteration_entries(refusal: _Refusal, model_label: str) -> list[dict[str, Any]]:
    """The `usage.iterations` entries a declined hop contributes to the chain.

    The hop's refusal self-reports its iterations: adopt them, retyped to
    `message` (every one of them declined — a server-stitched envelope labels
    its last hop `fallback_message`). A single-entry self-report describes the
    hop itself and gains its model — `model_label`, the caller-spelled primary
    or the chain entry's id — when the wire didn't name one; a multi-entry
    self-report (a server-tool loop) is kept verbatim. Without a self-report,
    one entry is built from the refusal's usage.
    """
    reported = refusal.usage.get("iterations")
    if isinstance(reported, list) and reported:
        dict_entries = (_as_dict(entry) for entry in cast("List[Any]", reported))
        entries: list[dict[str, Any]] = [{**entry, "type": "message"} for entry in dict_entries if entry is not None]
        if entries:
            if len(entries) == 1 and not isinstance(entries[0].get("model"), str):
                entries[0]["model"] = model_label
            return entries
    return [_to_iteration_usage("message", model_label, refusal.usage)]


def _serving_iteration_entry(delta_usage: dict[str, Any], model: str) -> dict[str, Any]:
    """The serving hop's `fallback_message` completer entry: its own
    self-reported iteration relabeled, or one built from its delta usage."""
    reported = delta_usage.get("iterations")
    if isinstance(reported, list) and reported:
        last = _as_dict(cast("List[Any]", reported)[-1])
        if last is not None:
            return {**last, "type": "fallback_message", "model": last.get("model") or model}
    return _to_iteration_usage("fallback_message", model, delta_usage)


class _BlockTracker:
    """Block bookkeeping for one stream of the splice: accumulates each content
    block from its deltas (for the continuation prefill), shifts wire indices
    by `index_base` so they stay monotonic across hops, and tracks which blocks
    are still open so a refusal that cuts mid-block can close them.
    """

    next_index: int
    """One past the highest shifted block index seen."""

    def __init__(self, index_base: int = 0) -> None:
        self._index_base = index_base
        self.next_index = index_base
        # the stream's accumulated blocks keyed by their original wire index
        self._blocks: list[tuple[int, dict[str, Any]]] = []
        # shifted indices of blocks started but not yet stopped
        self._open: list[int] = []

    def content_blocks(self) -> list[dict[str, Any]]:
        """The accumulated content blocks, in start order."""
        return [block for _, block in self._blocks]

    def start(self, event: dict[str, Any]) -> None:
        """Track a content_block_start, shifting `event["index"]`."""
        index = event.get("index")
        if not isinstance(index, int):
            return
        content_block = _as_dict(event.get("content_block"))
        self._blocks.append((index, dict(content_block) if content_block is not None else {}))
        shifted = index + self._index_base
        event["index"] = shifted
        self._open.append(shifted)
        self.next_index = max(self.next_index, shifted + 1)

    def delta(self, event: dict[str, Any]) -> None:
        """Apply a content_block_delta to its accumulating block, shifting `event["index"]`."""
        index = event.get("index")
        if not isinstance(index, int):
            return
        delta = _as_dict(event.get("delta"))
        if delta is not None:
            _apply_delta(self._blocks, index, delta)
        event["index"] = index + self._index_base

    def stop(self, event: dict[str, Any]) -> None:
        """Track a content_block_stop, shifting `event["index"]`."""
        index = event.get("index")
        if not isinstance(index, int):
            return
        shifted = index + self._index_base
        event["index"] = shifted
        if shifted in self._open:
            self._open.remove(shifted)
        self.next_index = max(self.next_index, shifted + 1)

    def close_open_blocks(self) -> Iterator[bytes]:
        """content_block_stop events for any blocks still open."""
        for index in self._open:
            yield _emit("content_block_stop", {"type": "content_block_stop", "index": index})
        self._open.clear()


# --- block accumulation & prefill conversion -------------------------------


def _apply_delta(blocks: list[tuple[int, dict[str, Any]]], index: int, delta: dict[str, Any]) -> None:
    """Apply a content_block_delta to the accumulating block at `index`."""
    block = next((block for block_index, block in blocks if block_index == index), None)
    if block is None:
        return
    delta_type = delta.get("type")
    if delta_type == "text_delta":
        block["text"] = str(block.get("text") or "") + str(delta.get("text") or "")
    elif delta_type == "input_json_delta":
        block["_partial_json"] = str(block.get("_partial_json") or "") + str(delta.get("partial_json") or "")
    elif delta_type == "citations_delta":
        citations = block.get("citations")
        if not isinstance(citations, list):
            citations = []
            block["citations"] = citations
        cast("List[Any]", citations).append(delta.get("citation"))
    elif delta_type == "thinking_delta":
        block["thinking"] = str(block.get("thinking") or "") + str(delta.get("thinking") or "")
    elif delta_type == "signature_delta":
        block["signature"] = delta.get("signature")


def _to_prefill_blocks(response_blocks: list[dict[str, Any]]) -> list[Any]:
    """Convert a hop's accumulated response blocks to the appended assistant turn.

    A `fallback_has_prefill_claim` refusal guarantees the partial output is
    resendable, so the blocks go out near-verbatim. Three rewrites apply:
    `fallback` seam blocks (wire markers, not content) are dropped, tool inputs
    are reassembled from their accumulated `input_json_delta` JSON
    (content_block_start carries `input: {}`), and trailing thinking blocks are
    stripped — the server rejects an assistant turn whose final block is
    `thinking`, so a refusal that cut the stream mid-thought would otherwise
    400 the continuation. A partial that was nothing but thinking strips to
    empty, and the hop falls back to the same-body form.
    """
    out: list[Any] = []
    for block in response_blocks:
        if block.get("type") == "fallback":
            continue
        partial_json = block.get("_partial_json")
        if not isinstance(partial_json, str):
            out.append(block)
            continue
        block = {key: value for key, value in block.items() if key != "_partial_json"}
        parsed = _safe_json(partial_json)
        block["input"] = parsed if parsed is not None else block.get("input")
        out.append(block)
    while out and out[-1].get("type") in ("thinking", "redacted_thinking"):
        out.pop()
    return out


# --- helpers --------------------------------------------------------------


def _strip_seam_blocks(body: dict[str, Any]) -> dict[str, Any]:
    """A copy of `body` with `{type: "fallback"}` seam blocks filtered out of the
    replayed message history; `body` itself when there are none.

    An assistant turn left with no content by the strip — a seam-only turn — is
    dropped whole; the server rejects empty-content turns."""
    messages = body.get("messages")
    if not isinstance(messages, list):
        return body
    stripped = False
    stripped_messages: list[Any] = []
    for message in cast("List[Any]", messages):
        message_dict = _as_dict(message)
        content = message_dict.get("content") if message_dict is not None else None
        if message_dict is None or not isinstance(content, list):
            stripped_messages.append(message)
            continue
        content_list = cast("List[Any]", content)
        kept = [block for block in content_list if not (is_dict(block) and block.get("type") == "fallback")]
        if len(kept) == len(content_list):
            stripped_messages.append(message)
            continue
        stripped = True
        if not kept and message_dict.get("role") == "assistant":
            continue
        stripped_messages.append({**message_dict, "content": kept})
    if not stripped:
        return body
    return {**body, "messages": stripped_messages}


def _with_middleware_headers(request: APIRequest, betas: tuple[AnthropicBetaParam, ...]) -> APIRequest:
    """A copy of `request` with `betas` appended to its `anthropic-beta` header
    (skipping values already present) and the middleware's helper-telemetry tag
    appended to `x-stainless-helper`. Single `request.copy()` for both.
    """
    # httpx.Headers for the case-insensitive read; Omit-valued entries can't be
    # the beta header's value and are carried over untouched below.
    current = httpx.Headers({k: v for k, v in request.headers.items() if isinstance(v, str)}).get("anthropic-beta", "")
    existing = {value.strip() for value in current.split(",")}
    additions = dict.fromkeys(str(beta) for beta in betas if str(beta) not in existing)
    headers = {k: v for k, v in request.headers.items() if k.lower() != "anthropic-beta"}
    if current or additions:
        headers["anthropic-beta"] = ", ".join(filter(None, [current, *additions]))
    return request.copy(headers=merge_headers(headers, helper_header("fallback-refusal-middleware")))


def _credit_token(message: Message | BetaMessage) -> str | None:
    """The refusal's minted credit token; only the beta surface carries one."""
    if isinstance(message, BetaMessage) and message.stop_details is not None:
        return message.stop_details.fallback_credit_token
    return None


def _refusal_category(message: Message | BetaMessage) -> str | None:
    """The policy category that caused the refusal; only the beta surface carries one."""
    if isinstance(message, BetaMessage) and message.stop_details is not None:
        return message.stop_details.category
    return None


def _seam_block(from_model: str, to_model: str, category: str | None) -> dict[str, Any]:
    """The synthetic `fallback` content block marking one model boundary."""
    return {
        "type": "fallback",
        "from": {"model": from_model},
        "to": {"model": to_model},
        "trigger": {"type": "refusal", "category": category},
    }


def _seamed_http_response(original: httpx.Response, seams: list[dict[str, Any]]) -> httpx.Response | None:
    """A copy of the served hop's response with `seams` prepended to its
    `content`, or `None` when the body isn't the expected message shape.

    The caller has already parsed the response, so its body is buffered.
    """
    message = _as_dict(_safe_json(original.content.decode("utf-8")))
    if message is None or not isinstance(message.get("content"), list):
        return None
    body = _json_dumps({**message, "content": [*seams, *cast("List[Any]", message["content"])]}).encode("utf-8")
    headers = original.headers.copy()
    for header in ("content-encoding", "content-length"):
        if header in headers:
            del headers[header]
    return httpx.Response(
        status_code=original.status_code,
        headers=headers,
        content=body,
        request=original.request,
    )


def _prepend_seam_blocks(response: APIResponse[Any], seams: list[dict[str, Any]]) -> APIResponse[Any]:
    raw = _seamed_http_response(response.http_response, seams)
    if raw is None:
        return response
    return APIResponse(
        raw=raw,
        cast_to=response._cast_to,
        client=response._client,
        stream=False,
        stream_cls=response._stream_cls,
        options=response._options,
        retries_taken=response.retries_taken,
    )


def _prepend_seam_blocks_async(response: AsyncAPIResponse[Any], seams: list[dict[str, Any]]) -> AsyncAPIResponse[Any]:
    raw = _seamed_http_response(response.http_response, seams)
    if raw is None:
        return response
    return AsyncAPIResponse(
        raw=raw,
        cast_to=response._cast_to,
        client=response._client,
        stream=False,
        stream_cls=response._stream_cls,
        options=response._options,
        retries_taken=response.retries_taken,
    )


def _merged_body(body: dict[str, Any], fallback: BetaFallbackParam, credit_token: str | None) -> dict[str, Any]:
    """The non-streaming retry body: the fallback entry merged whole over the
    original params, plus the refusal's credit token when it minted one."""
    merged: dict[str, Any] = {**body, **fallback}
    if credit_token:
        merged["fallback_credit_token"] = credit_token
    return merged


def _safe_json(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        return None


def _json_dumps(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"))


def _as_dict(value: object) -> dict[str, Any] | None:
    return cast("Dict[str, Any]", value) if is_dict(value) else None


def _read_json(response: httpx.Response) -> Any:
    try:
        return json.loads(response.read())
    except Exception:
        return None


async def _read_json_async(response: httpx.Response) -> Any:
    try:
        return json.loads(await response.aread())
    except Exception:
        return None


def _emit(event: str, payload: dict[str, Any]) -> bytes:
    return _serialize_sse(event=event, data=_json_dumps(payload)).encode("utf-8")


def _passthrough_sse(sse: ServerSentEvent) -> bytes:
    """Forward a decoded event in its original wire bytes, preserving SSE fields
    beyond `event:`/`data:` (`id:`, `retry:`, comment lines). Falls back to
    re-serializing for events with no raw lines.
    """
    if sse.raw:
        return ("\n".join(sse.raw) + "\n\n").encode("utf-8")
    return _serialize_sse(event=sse.event, data=sse.data).encode("utf-8")


def _serialize_sse(*, event: str | None, data: str) -> str:
    """Serialize an event back to its SSE wire form (`event: ...\\ndata: ...\\n\\n`).

    Multi-line `data` is emitted as one `data:` line per line, matching the
    spec. The inverse of the decoder behind `Stream.raw_events`.
    """
    out = ""
    if event is not None:
        out += f"event: {event}\n"
    for line in data.split("\n"):
        out += f"data: {line}\n"
    return out + "\n"


def _to_iteration_usage(
    type: Literal["message", "fallback_message"], model: str, usage: dict[str, Any] | None
) -> dict[str, Any]:
    u = usage or {}
    return {
        "type": type,
        "model": model,
        "input_tokens": u.get("input_tokens") or 0,
        "output_tokens": u.get("output_tokens") or 0,
        "cache_read_input_tokens": u.get("cache_read_input_tokens") or 0,
        "cache_creation_input_tokens": u.get("cache_creation_input_tokens") or 0,
        "cache_creation": u.get("cache_creation"),
    }


def _backfill(primary: dict[str, Any] | None, fallback: dict[str, Any] | None) -> dict[str, Any]:
    """Fill `None` fields on `primary` from `fallback`."""
    fallback = fallback or {}
    out: dict[str, Any] = {**fallback, **(primary or {})}
    for key, value in out.items():
        if value is None and fallback.get(key) is not None:
            out[key] = fallback[key]
    return out


def _spliced_http_response(
    original: httpx.Response, stream: httpx.SyncByteStream | httpx.AsyncByteStream
) -> httpx.Response:
    """A synthetic response standing in for `original`, with `stream` as its body.

    The spliced frames are emitted post-decode, so the original's
    content-encoding/length headers no longer describe the body.
    """
    headers = original.headers.copy()
    for header in ("content-encoding", "content-length"):
        if header in headers:
            del headers[header]
    return httpx.Response(
        status_code=original.status_code,
        headers=headers,
        stream=stream,
        request=original.request,
    )


class _FrameByteStream(httpx.SyncByteStream):
    def __init__(self, frames: Generator[bytes, None, None]) -> None:
        self._frames = frames

    @override
    def __iter__(self) -> Iterator[bytes]:
        return self._frames

    @override
    def close(self) -> None:
        self._frames.close()


class _AsyncFrameByteStream(httpx.AsyncByteStream):
    def __init__(self, frames: AsyncGenerator[bytes, None]) -> None:
        self._frames = frames

    @override
    def __aiter__(self) -> AsyncIterator[bytes]:
        return self._frames

    @override
    async def aclose(self) -> None:
        await self._frames.aclose()
