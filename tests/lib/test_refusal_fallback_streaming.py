from __future__ import annotations

import os
import re
import json
import logging
from typing import Any, List, Protocol, cast
from pathlib import Path

import httpx
import pytest
from respx import MockRouter

from anthropic import (
    Omit,
    Stream,
    Anthropic,
    APIRequest,
    APIResponse,
    AsyncStream,
    AnthropicError,
    AsyncAnthropic,
    BetaFallbackState,
    BetaRefusalFallbackMiddleware,
    omit,
)
from anthropic._models import FinalRequestOptions
from anthropic.types.beta import BetaMessage, BetaFallbackParam, BetaRawMessageStreamEvent
from anthropic.types.anthropic_beta_param import AnthropicBetaParam

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

LOGGER_NAME = "anthropic.lib.middleware"


def error_logs(caplog: pytest.LogCaptureFixture) -> list[str]:
    """Messages the middleware logged at ERROR — refusals surfaced rather than retried."""
    return [
        record.getMessage()
        for record in caplog.records
        if record.name == LOGGER_NAME and record.levelno >= logging.ERROR
    ]


FIXTURES = Path(__file__).parent.parent / "fixtures" / "fable-fallback"
FALLBACK_MODEL = "claude-opus-4-8"
SECOND_MODEL = "claude-sonnet-4-6"
FALLBACKS: List[BetaFallbackParam] = [{"model": FALLBACK_MODEL}]
TWO_FALLBACKS: List[BetaFallbackParam] = [{"model": FALLBACK_MODEL}, {"model": SECOND_MODEL}]

# Wire-shaped synthetic capture — the primary refuses after a thinking +
# partial-text block and mints a credit token; the fallback then completes
# the message.
STREAM_A = (FIXTURES / "stream-a-refusal.sse").read_text()
STREAM_B = (FIXTURES / "stream-b-fallback.sse").read_text()

# Server-tool wire (synthetic, wire-shaped): server_tool_use streams its input
# via input_json_delta after an empty `input:{}`, the web_search_tool_result
# arrives as a single content_block_start carrying full content, and the
# refusal terminal (message_delta + token) lands mid-tool-loop, after a
# partial text block. The token is never redeemed (the mock serves the next
# leg).
STREAM_A_TOOL = (FIXTURES / "stream-a-toolrefusal.sse").read_text()

PARAMS: dict[str, Any] = {
    "model": "claude-fable-5",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hey claudius! Can you tell me what a solar eclipse is?"}],
}


def make_sync_client(**kwargs: Any) -> Anthropic:
    return Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, max_retries=0, **kwargs)


def make_async_client(**kwargs: Any) -> AsyncAnthropic:
    return AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, max_retries=0, **kwargs)


def make_lenient_client(**kwargs: Any) -> Anthropic:
    """A client with the default (non-strict) response validation.

    The fixture wire's terminal refusal delta self-reports a `{type: "message"}`
    iteration without a `model` key, which the generated
    `BetaMessageIterationUsage` type marks required — strict validation rejects
    it. Tests where that wire reaches the parser verbatim (pass-through
    refusals, synthetic closes reusing the refusal's usage) use this client.
    """
    return Anthropic(base_url=base_url, api_key=api_key, max_retries=0, **kwargs)


def sse_response(body: str) -> httpx.Response:
    return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=body.encode("utf-8"))


def json_response(body: Any, status: int) -> httpx.Response:
    return httpx.Response(status, json=body)


def error_response(message: str, status: int) -> httpx.Response:
    return json_response({"type": "error", "error": {"type": "invalid_request_error", "message": message}}, status)


def ev(data: dict[str, Any]) -> str:
    """Serialize one event payload as an SSE frame (its `type` is the event name)."""
    return f"event: {data['type']}\ndata: {json.dumps(data)}\n\n"


def message_start() -> str:
    return ev(
        {
            "type": "message_start",
            "message": {
                "id": "msg_a",
                "type": "message",
                "role": "assistant",
                "model": "claude-fable-5",
                "content": [],
                "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 12, "output_tokens": 1},
            },
        }
    )


def refusal_delta(token: str | None = "tok_abc", has_prefill_claim: bool = True) -> str:
    return ev(
        {
            "type": "message_delta",
            "delta": {
                "stop_reason": "refusal",
                "stop_sequence": None,
                "stop_details": {
                    "type": "refusal",
                    "category": None,
                    "explanation": None,
                    "fallback_credit_token": token,
                    "fallback_has_prefill_claim": has_prefill_claim if token is not None else None,
                },
            },
            "usage": {"output_tokens": 20},
        }
    )


def collect(stream: Stream[BetaRawMessageStreamEvent]) -> list[BetaRawMessageStreamEvent]:
    return list(stream)


class MockRequestCall(Protocol):
    request: httpx.Request


def request_bodies(respx_mock: MockRouter) -> list[dict[str, Any]]:
    calls = cast("list[MockRequestCall]", respx_mock.calls)
    return [cast("dict[str, Any]", json.loads(call.request.content)) for call in calls]


def beta_headers(respx_mock: MockRouter) -> list[str | None]:
    calls = cast("list[MockRequestCall]", respx_mock.calls)
    return [call.request.headers.get("anthropic-beta") for call in calls]


def skeleton(events: list[BetaRawMessageStreamEvent]) -> list[str]:
    """Compact structural skeleton of a spliced stream — no text content."""
    out: list[str] = []
    for event in events:
        if event.type == "content_block_start":
            block = event.content_block
            if block.type == "fallback":
                label = f"fallback{{{block.from_.model}->{block.to.model}}}"
            else:
                label = block.type
            out.append(f"start[{event.index}] {label}")
        elif event.type == "content_block_delta":
            out.append(f"delta[{event.index}] {event.delta.type}")
        elif event.type == "content_block_stop":
            out.append(f"stop[{event.index}]")
        elif event.type == "message_delta":
            iterations = ",".join(f"{i.type}:{i.model}" for i in (event.usage.iterations or []))  # type: ignore[union-attr]
            out.append(f"message_delta {event.delta.stop_reason} iter=[{iterations}]")
        else:
            out.append(event.type)
    return out


def block_starts(events: list[BetaRawMessageStreamEvent]) -> list[tuple[int, str]]:
    return [(e.index, e.content_block.type) for e in events if e.type == "content_block_start"]


def create_stream(
    client: Anthropic, *, betas: List[AnthropicBetaParam] | Omit = omit
) -> Stream[BetaRawMessageStreamEvent]:
    return client.beta.messages.create(
        model="claude-fable-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hey claudius! Can you tell me what a solar eclipse is?"}],
        betas=betas,
        stream=True,
    )


async def create_stream_async(client: AsyncAnthropic) -> "AsyncStream[BetaRawMessageStreamEvent]":
    return await client.beta.messages.create(
        model="claude-fable-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hey claudius! Can you tell me what a solar eclipse is?"}],
        stream=True,
    )


# --- happy path -----------------------------------------------------------


class TestShapeBContinuation:
    @pytest.mark.respx(base_url=base_url)
    def test_splices_the_fallback_onto_the_refused_stream(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        # A's thinking + text are forwarded, a fallback boundary block is emitted
        # at the next monotonic index, then B's blocks continue after it.
        assert block_starts(events) == [
            (0, "thinking"),
            (1, "text"),
            (2, "fallback"),
            (3, "text"),
        ]

        # The fallback block carries the from/to model transition.
        fallback = next(
            e.content_block for e in events if e.type == "content_block_start" and e.content_block.type == "fallback"
        )
        assert fallback.from_.model == "claude-fable-5"
        assert fallback.to.model == FALLBACK_MODEL

        # Exactly one message_start (A's) and one message_stop reach the client —
        # B's message_start is suppressed.
        assert len([e for e in events if e.type == "message_start"]) == 1
        assert len([e for e in events if e.type == "message_stop"]) == 1
        assert len([e for e in events if e.type == "message_delta"]) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_usage_iterations_is_the_two_entry_server_shape(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        message_delta = next(e for e in events if e.type == "message_delta")
        assert message_delta.delta.stop_reason == "end_turn"
        iterations = message_delta.usage.iterations or []
        # the 2-entry server shape, with no spurious `message: None` entry
        assert [(i.type, i.model) for i in iterations] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("fallback_message", FALLBACK_MODEL),
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_builds_request_b_as_a_shape_b_continuation(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        collect(create_stream(client))

        bodies = request_bodies(respx_mock)
        assert len(bodies) == 2
        body_b = bodies[1]

        # Model swapped to the fallback, credit token from A's stop_details set.
        assert body_b["model"] == FALLBACK_MODEL
        assert isinstance(body_b["fallback_credit_token"], str)
        assert len(body_b["fallback_credit_token"]) > 0

        # Mutually exclusive with server-side fallback — both spellings absent.
        assert "fallback" not in body_b
        assert "fallbacks" not in body_b

        # max_tokens untouched (any render-shaping change would 400).
        assert body_b["max_tokens"] == 1024

        # Original turn preserved; one assistant turn appended carrying the
        # [thinking, text] partial output as-is — the prefill claim authorizes
        # it verbatim, so no client-side filtering or trimming.
        assert len(body_b["messages"]) == 2
        assert body_b["messages"][0] == PARAMS["messages"][0]
        appended = body_b["messages"][1]
        assert appended["role"] == "assistant"
        assert [block["type"] for block in appended["content"]] == ["thinking", "text"]
        assert "signature" in appended["content"][0]

    @pytest.mark.respx(base_url=base_url)
    def test_appends_the_fallback_credit_beta_to_both_the_original_and_hop_requests(
        self, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        # the request already carries a beta header; the default is appended to it.
        collect(create_stream(client, betas=["interleaved-thinking-2025-05-14"]))

        assert beta_headers(respx_mock) == [
            "interleaved-thinking-2025-05-14, fallback-credit-2026-06-01",
            "interleaved-thinking-2025-05-14, fallback-credit-2026-06-01",
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_the_betas_option_replaces_the_default_on_every_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware(FALLBACKS, betas=["fallback-credit-2027-01-01"])]
        )

        collect(create_stream(client, betas=["fallback-credit-2026-06-01"]))

        assert beta_headers(respx_mock) == [
            "fallback-credit-2026-06-01, fallback-credit-2027-01-01",
            "fallback-credit-2026-06-01, fallback-credit-2027-01-01",
        ]


# --- edge cases -----------------------------------------------------------


class TestEdgeCases:
    @pytest.mark.respx(base_url=base_url)
    def test_a_refusal_without_a_prefill_claim_falls_back_to_shape_a(self, respx_mock: MockRouter) -> None:
        # fallback_has_prefill_claim: false — the partial output may not be
        # resent, so the middleware omits the prefill and resends the original
        # body with just the token attached.
        no_claim = "".join(
            [
                message_start(),
                ev(
                    {
                        "type": "content_block_start",
                        "index": 0,
                        "content_block": {"type": "thinking", "thinking": "", "signature": ""},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "thinking_delta", "thinking": "considering the request"},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "signature_delta", "signature": "sig=="},
                    }
                ),
                ev({"type": "content_block_stop", "index": 0}),
                refusal_delta("tok_abc", False),
                ev({"type": "message_stop"}),
            ]
        )
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(no_claim), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        collect(create_stream(client))

        bodies = request_bodies(respx_mock)
        assert bodies[1]["fallback_credit_token"] == "tok_abc"
        # No appended assistant turn — identical body (shape-A).
        assert bodies[1]["messages"] == PARAMS["messages"]

    @pytest.mark.respx(base_url=base_url)
    def test_refusal_with_no_credit_token_passes_a_through_and_logs_an_error(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        no_token = re.sub(r'"fallback_credit_token":"[^"]*"', '"fallback_credit_token":null', STREAM_A)
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(no_token)])
        client = make_lenient_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        # Only the original request was made — no fallback.
        assert len(respx_mock.calls) == 1
        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "no fallback_credit_token" in errors[0]

        # A passes through unchanged, ending in its own refusal (no fallback block).
        assert not any(e.type == "content_block_start" and e.content_block.type == "fallback" for e in events)
        assert next(e for e in events if e.type == "message_delta").delta.stop_reason == "refusal"

    @pytest.mark.respx(base_url=base_url)
    def test_a_400_on_the_prefill_form_retries_the_same_hop_without_the_partial(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                error_response("bad prefill", 400),
                sse_response(STREAM_B),
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        # Attempt 1 appends A's partial; the 400 drops it and attempt 2 redeems
        # the same token against the unchanged body.
        bodies = request_bodies(respx_mock)
        assert len(bodies) == 3
        assert len(bodies[1]["messages"]) == 2
        assert bodies[2]["model"] == FALLBACK_MODEL
        assert bodies[2]["fallback_credit_token"] == bodies[1]["fallback_credit_token"]
        assert bodies[2]["messages"] == PARAMS["messages"]

        # The recovered hop is not a failure: one boundary, a normal completion.
        assert error_logs(caplog) == []
        boundaries = [e for e in events if e.type == "content_block_start" and e.content_block.type == "fallback"]
        assert len(boundaries) == 1
        assert next(e for e in events if e.type == "message_delta").delta.stop_reason == "end_turn"

    @pytest.mark.respx(base_url=base_url)
    def test_a_failed_fallback_request_replays_the_refusal_and_logs_an_error(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                # the prefill form 400s, the same-body retry 400s too — only
                # then does the hop count as failed
                error_response("nope", 400),
                error_response("nope", 400),
            ]
        )
        client = make_lenient_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        assert len(respx_mock.calls) == 3
        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "HTTP 400" in errors[0]
        assert FALLBACK_MODEL in errors[0]

        # The failed hop was never reached, so it leaves no seam; A's suppressed
        # refusal is replayed — its credit token intact for a manual retry, with
        # no model recommendation (the failure was not a capacity error) — then
        # message_stop closes the stream.
        assert not any(e.type == "content_block_start" and e.content_block.type == "fallback" for e in events)
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_reason == "refusal"
        assert delta.delta.stop_details is not None
        assert delta.delta.stop_details.fallback_credit_token is not None
        assert delta.delta.stop_details.recommended_model is None
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
        ]
        assert events[-1].type == "message_stop"

    @pytest.mark.respx(base_url=base_url)
    def test_a_capacity_failed_fallback_request_stamps_the_recommended_model(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                json_response({"type": "error", "error": {"type": "overloaded_error", "message": "later"}}, 529),
            ]
        )
        client = make_lenient_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "HTTP 529" in errors[0]
        # a capacity failure (429/529) stamps the failed model as the recommendation
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_details is not None
        assert delta.delta.stop_details.recommended_model == FALLBACK_MODEL

    @pytest.mark.respx(base_url=base_url)
    def test_a_fallback_request_that_raises_replays_the_refusal(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[sse_response(STREAM_A), httpx.ConnectError("connection reset")]
        )
        client = make_lenient_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        errors = error_logs(caplog)
        assert len(errors) == 1
        # the raised error reaches the log as the SDK's connection error
        assert "Connection error." in errors[0]
        assert FALLBACK_MODEL in errors[0]

        # The stream still closes cleanly: A's refusal is replayed and
        # message_stop follows — not a hard stream error.
        assert next(e for e in events if e.type == "message_delta").delta.stop_reason == "refusal"
        assert events[-1].type == "message_stop"

    @pytest.mark.respx(base_url=base_url)
    def test_pass_through_preserves_sse_fields_beyond_event_and_data(self, respx_mock: MockRouter) -> None:
        wire = (
            "retry: 1500\nevent: message_start\ndata: "
            + json.dumps(
                {
                    "type": "message_start",
                    "message": {
                        "id": "msg_a",
                        "type": "message",
                        "role": "assistant",
                        "model": "claude-fable-5",
                        "content": [],
                        "stop_reason": None,
                        "stop_sequence": None,
                        "usage": {"input_tokens": 10, "output_tokens": 1},
                    },
                }
            )
            + "\n\n"
            + ": keep-alive\nid: 42\nevent: message_delta\ndata: "
            + json.dumps(
                {
                    "type": "message_delta",
                    "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                    "usage": {"output_tokens": 3},
                }
            )
            + "\n\n"
            + "event: message_stop\ndata: "
            + json.dumps({"type": "message_stop"})
            + "\n\n"
        )
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(wire)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        stream = create_stream(client)
        raw = stream.response.read()

        assert raw.decode("utf-8") == wire

    @pytest.mark.respx(base_url=base_url)
    def test_a_non_refusal_stream_is_passed_through_untouched(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        normal = "".join(
            [
                message_start(),
                ev({"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "text_delta", "text": "Sure!"},
                    }
                ),
                ev({"type": "content_block_stop", "index": 0}),
                ev(
                    {
                        "type": "message_delta",
                        "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                        "usage": {"output_tokens": 3},
                    }
                ),
                ev({"type": "message_stop"}),
            ]
        )
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(normal)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        assert len(respx_mock.calls) == 1
        assert error_logs(caplog) == []
        assert skeleton(events) == [
            "message_start",
            "start[0] text",
            "delta[0] text_delta",
            "stop[0]",
            "message_delta end_turn iter=[]",
            "message_stop",
        ]

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_server_side_fallbacks_raise_an_error(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A)])
        client = make_lenient_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        with pytest.raises(
            AnthropicError, match=r"Sending the `fallbacks:` request param is not supported when using the `BetaRefusalFallbackMiddleware`\. You should either remove the middleware and send `fallbacks:` with the `server-side-fallback-2026-06-01` beta header to let the API handle refusal fallbacks, or omit the `fallbacks:` param if you'd like `BetaRefusalFallbackMiddleware` to handle fallbacks on the client side\."
        ):
            client.beta.messages.create(
                model="claude-fable-5",
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hey claudius! Can you tell me what a solar eclipse is?"}],
                fallbacks=[{"model": "server-fallback"}],
                stream=True,
            )
        # the error is raised before any request is sent
        assert len(respx_mock.calls) == 0


# --- fallback state pinning -------------------------------------------------


class TestFallbackState:
    @pytest.mark.respx(base_url=base_url)
    def test_pins_the_state_to_the_hop_that_served(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        state = BetaFallbackState()
        with state:
            collect(create_stream(client))

        assert state.index == 0

    @pytest.mark.respx(base_url=base_url)
    def test_a_pinned_state_starts_on_the_pinned_entry_and_chains_past_it(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(TWO_FALLBACKS)])

        state = BetaFallbackState()
        state.index = 0
        with state:
            collect(create_stream(client))

        bodies = request_bodies(respx_mock)
        assert len(bodies) == 2
        # The initial request already carries the pinned entry's params; the
        # mid-stream refusal then chains to the entry after the pin.
        assert bodies[0]["model"] == FALLBACK_MODEL
        assert bodies[1]["model"] == SECOND_MODEL
        assert state.index == 1

    @pytest.mark.respx(base_url=base_url)
    def test_warns_once_when_falling_back_without_a_state(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                sse_response(STREAM_B),
                sse_response(STREAM_A),
                sse_response(STREAM_B),
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            # drain the spliced stream so the fallback actually fires
            collect(create_stream(client))
            collect(create_stream(client))

        warnings = [record for record in caplog.records if record.name == LOGGER_NAME]
        assert len(warnings) == 1
        assert "BetaFallbackState" in warnings[0].getMessage()


# --- fallback chain ---------------------------------------------------------


def hop_refusal(token: str | None = "tok_b", has_prefill_claim: bool = True) -> str:
    """A fallback hop that contributes one text block, then refuses with a fresh token."""
    return "".join(
        [
            message_start(),
            ev({"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}),
            ev(
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": "Partial from B. "},
                }
            ),
            ev({"type": "content_block_stop", "index": 0}),
            refusal_delta(token, has_prefill_claim),
            ev({"type": "message_stop"}),
        ]
    )


class TestFallbackChain:
    @pytest.mark.respx(base_url=base_url)
    def test_a_refused_hop_splices_its_partial_and_chains_to_the_next_entry(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[sse_response(STREAM_A), sse_response(hop_refusal()), sse_response(STREAM_B)]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(TWO_FALLBACKS)])

        events = collect(create_stream(client))

        bodies = request_bodies(respx_mock)
        assert len(bodies) == 3

        # Hop 1 redeems A's token; hop 2 redeems the fresh token minted by hop 1's
        # refusal, with hop 1's partial extending the same turn as-is.
        assert bodies[1]["model"] == FALLBACK_MODEL
        assert bodies[2]["model"] == SECOND_MODEL
        assert bodies[2]["fallback_credit_token"] == "tok_b"
        assert bodies[2]["fallback_credit_token"] != bodies[1]["fallback_credit_token"]
        assert bodies[2]["messages"][1]["content"] == [
            *bodies[1]["messages"][1]["content"],
            {"type": "text", "text": "Partial from B. "},
        ]

        # One continuous message: A's blocks, boundary, hop 1's partial, boundary,
        # hop 2's blocks — indices stay monotonic across all three streams.
        assert block_starts(events) == [
            (0, "thinking"),
            (1, "text"),
            (2, "fallback"),
            (3, "text"),
            (4, "fallback"),
            (5, "text"),
        ]
        boundaries = [
            e.content_block for e in events if e.type == "content_block_start" and e.content_block.type == "fallback"
        ]
        assert (boundaries[0].from_.model, boundaries[0].to.model) == ("claude-fable-5", FALLBACK_MODEL)
        assert (boundaries[1].from_.model, boundaries[1].to.model) == (FALLBACK_MODEL, SECOND_MODEL)

        # Hop 1's refusal delta is suppressed; the terminal delta carries every hop.
        deltas = [e for e in events if e.type == "message_delta"]
        assert len(deltas) == 1
        assert deltas[0].delta.stop_reason == "end_turn"
        assert [(i.type, i.model) for i in (deltas[0].usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("message", FALLBACK_MODEL),
            ("fallback_message", SECOND_MODEL),
        ]
        assert len([e for e in events if e.type == "message_stop"]) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_a_refused_hop_without_a_prefill_claim_drops_its_partial_from_the_next_request(
        self, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                sse_response(hop_refusal("tok_b", False)),
                sse_response(STREAM_B),
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(TWO_FALLBACKS)])

        collect(create_stream(client))

        bodies = request_bodies(respx_mock)
        assert len(bodies) == 3
        assert bodies[2]["fallback_credit_token"] == "tok_b"
        # Hop 2 redeems the fresh token against the body it was minted for —
        # hop 1's request, including its appended turn — without hop 1's own
        # (unclaimed) partial output.
        assert bodies[2]["messages"] == bodies[1]["messages"]

    @pytest.mark.respx(base_url=base_url)
    def test_an_http_failed_hop_is_skipped_and_the_unredeemed_token_carries_to_the_next_entry(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                json_response({"type": "error", "error": {"type": "overloaded_error", "message": "later"}}, 529),
                sse_response(STREAM_B),
            ]
        )
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": FALLBACK_MODEL}, {"model": SECOND_MODEL}])]
        )

        events = collect(create_stream(client))

        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "HTTP 529" in errors[0]
        assert FALLBACK_MODEL in errors[0]
        assert len(respx_mock.calls) == 3

        # Same token and continuation — the failed hop never redeemed them.
        bodies = request_bodies(respx_mock)
        assert bodies[2]["model"] == SECOND_MODEL
        assert bodies[2]["fallback_credit_token"] == bodies[1]["fallback_credit_token"]
        assert bodies[2]["messages"] == bodies[1]["messages"]

        # The failed hop was never reached: no seam for it — one boundary, from
        # A straight to the entry that served.
        boundaries = [
            e.content_block for e in events if e.type == "content_block_start" and e.content_block.type == "fallback"
        ]
        assert [(b.from_.model, b.to.model) for b in boundaries] == [
            ("claude-fable-5", SECOND_MODEL),
        ]

        # The failed hop is absent from iterations (no usage came back).
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_reason == "end_turn"
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("fallback_message", SECOND_MODEL),
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_a_terminal_refusal_with_no_entries_left_is_emitted_with_the_full_iteration_chain(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(hop_refusal())])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        assert len(respx_mock.calls) == 2
        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "no fallback entries remain" in errors[0]
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_reason == "refusal"
        # The fresh token reaches the client for a manual retry.
        assert delta.delta.stop_details is not None
        assert delta.delta.stop_details.fallback_credit_token == "tok_b"
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("fallback_message", FALLBACK_MODEL),
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_a_token_less_refusal_on_the_final_hop_is_still_logged(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(hop_refusal(None))])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "no fallback_credit_token" in errors[0]
        assert next(e for e in events if e.type == "message_delta").delta.stop_reason == "refusal"

    def test_an_empty_chain_passes_the_stream_through_untouched(self, caplog: pytest.LogCaptureFixture) -> None:
        middleware = BetaRefusalFallbackMiddleware([])
        client = make_sync_client()

        options = FinalRequestOptions.construct(
            method="post", url="/v1/messages?beta=true", json_data=dict(PARAMS), headers={}
        )
        request = APIRequest(
            options=options,
            cast_to=BetaMessage,
            stream=True,
            stream_cls=Stream[BetaRawMessageStreamEvent],
        )
        response = APIResponse(
            raw=sse_response(STREAM_A),
            cast_to=BetaMessage,
            client=client,
            stream=True,
            stream_cls=Stream[BetaRawMessageStreamEvent],
            options=options,
        )

        calls: list[APIRequest] = []

        def call_next(req: APIRequest) -> APIResponse[Any]:
            calls.append(req)
            return response

        out = middleware.handle(request, call_next)

        # With nothing to hop to, the response isn't even wrapped — no per-event
        # decode/re-encode overhead, and no error: this is the steady state of an
        # exhausted or fully-pinned chain.
        assert out is response
        assert len(calls) == 1
        assert error_logs(caplog) == []

    @pytest.mark.respx(base_url=base_url)
    def test_a_hop_whose_request_raises_is_skipped_and_the_unredeemed_token_carries(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(STREAM_A),
                httpx.ConnectError("connection reset"),
                sse_response(STREAM_B),
            ]
        )
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": FALLBACK_MODEL}, {"model": SECOND_MODEL}])]
        )

        events = collect(create_stream(client))

        errors = error_logs(caplog)
        assert len(errors) == 1
        assert "Connection error." in errors[0]
        assert FALLBACK_MODEL in errors[0]
        assert len(respx_mock.calls) == 3

        # Same token — the raising hop never redeemed it.
        bodies = request_bodies(respx_mock)
        assert bodies[2]["model"] == SECOND_MODEL
        assert bodies[2]["fallback_credit_token"] == bodies[1]["fallback_credit_token"]

        # The stream completes normally from the next entry.
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_reason == "end_turn"
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("fallback_message", SECOND_MODEL),
        ]


# --- pre-stream refusals ------------------------------------------------------


def serving_stream(model: str = FALLBACK_MODEL, message_id: str = "msg_b") -> str:
    return "".join(
        [
            ev(
                {
                    "type": "message_start",
                    "message": {
                        "id": message_id,
                        "type": "message",
                        "role": "assistant",
                        "model": model,
                        "content": [],
                        "stop_reason": None,
                        "stop_sequence": None,
                        "usage": {"input_tokens": 12, "output_tokens": 1},
                    },
                }
            ),
            ev({"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}),
            ev({"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Happy to help."}}),
            ev({"type": "content_block_stop", "index": 0}),
            ev(
                {
                    "type": "message_delta",
                    "delta": {"stop_reason": "end_turn", "stop_sequence": None},
                    "usage": {"output_tokens": 9},
                }
            ),
            ev({"type": "message_stop"}),
        ]
    )


class TestPreStreamRefusals:
    """A refusal that arrives before any output streamed: the retry is free and
    invisible, so it fires even without a credit token, and the serving hop's
    message_start opens the wire carrying the primary's message id."""

    pre_stream_refusal = "".join([message_start(), refusal_delta("tok_abc", False), ev({"type": "message_stop"})])

    @pytest.mark.respx(base_url=base_url)
    def test_the_serving_start_opens_the_wire_with_the_primary_message_id(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[sse_response(self.pre_stream_refusal), sse_response(serving_stream())]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        # The refused hop's message_start never reaches the client; the serving
        # hop's opens the wire, rewritten to the primary's message id.
        starts = [e for e in events if e.type == "message_start"]
        assert len(starts) == 1
        assert starts[0].message.model == FALLBACK_MODEL
        assert starts[0].message.id == "msg_a"

        # One seam at index 0, then the serving hop's content after it.
        assert block_starts(events) == [(0, "fallback"), (1, "text")]
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_reason == "end_turn"
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("fallback_message", FALLBACK_MODEL),
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_a_token_less_pre_stream_refusal_still_retries(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        token_less = "".join([message_start(), refusal_delta(None), ev({"type": "message_stop"})])
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(token_less), sse_response(serving_stream())])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        # nothing had streamed, so the retry fired despite the missing token
        assert error_logs(caplog) == []
        bodies = request_bodies(respx_mock)
        assert len(bodies) == 2
        assert bodies[1]["model"] == FALLBACK_MODEL
        assert "fallback_credit_token" not in bodies[1]
        assert next(e for e in events if e.type == "message_delta").delta.stop_reason == "end_turn"

    @pytest.mark.respx(base_url=base_url)
    def test_a_chain_of_pre_stream_declines_queues_every_seam_in_order(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                sse_response(self.pre_stream_refusal),
                sse_response("".join([message_start(), refusal_delta("tok_b"), ev({"type": "message_stop"})])),
                sse_response(serving_stream(SECOND_MODEL)),
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(TWO_FALLBACKS)])

        events = collect(create_stream(client))

        # serving start first, then both seams, then the serving content
        assert events[0].type == "message_start"
        assert events[0].message.id == "msg_a"
        starts = [(e.index, e.content_block) for e in events if e.type == "content_block_start"]
        assert [(i, b.type) for i, b in starts] == [(0, "fallback"), (1, "fallback"), (2, "text")]
        seam_one, seam_two = starts[0][1], starts[1][1]
        assert seam_one.type == "fallback" and seam_two.type == "fallback"
        assert (seam_one.from_.model, seam_one.to.model) == ("claude-fable-5", FALLBACK_MODEL)
        assert (seam_two.from_.model, seam_two.to.model) == (FALLBACK_MODEL, SECOND_MODEL)
        delta = next(e for e in events if e.type == "message_delta")
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("message", FALLBACK_MODEL),
            ("fallback_message", SECOND_MODEL),
        ]


# --- history seam replay ------------------------------------------------------


class TestHistorySeamReplay:
    """Pinning is explicit-state-only: a `fallback` seam block replayed in the
    request history never pins — without a `BetaFallbackState` the first request
    goes to the original model. The seam blocks themselves are this middleware's
    client-side markers, so they are filtered out of the wire request, and an
    assistant turn that was only a seam is dropped whole — `content: []` is an
    invalid body."""

    @pytest.mark.respx(base_url=base_url)
    def test_a_history_seam_without_a_state_does_not_pin(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(serving_stream("claude-fable-5"))])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(TWO_FALLBACKS)])

        stream = client.beta.messages.create(
            model="claude-fable-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "hello"},
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "fallback",
                            "from": {"model": "claude-fable-5"},
                            "to": {"model": FALLBACK_MODEL},
                        },
                        {"type": "text", "text": "earlier turn"},
                    ],
                },
                {"role": "user", "content": "and again?"},
            ],
            stream=True,
        )
        collect(stream)

        bodies = request_bodies(respx_mock)
        assert len(bodies) == 1
        # no state, no pin — the first request goes to the original model
        assert bodies[0]["model"] == "claude-fable-5"
        # the seam block is the middleware's own marker — filtered off the wire
        assert bodies[0]["messages"][1]["content"] == [{"type": "text", "text": "earlier turn"}]
        assert beta_headers(respx_mock) == ["fallback-credit-2026-06-01"]

    @pytest.mark.respx(base_url=base_url)
    def test_a_seam_only_assistant_turn_is_dropped_whole(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(serving_stream("claude-fable-5"))])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        stream = client.beta.messages.create(
            model="claude-fable-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "hello"},
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "fallback",
                            "from": {"model": "claude-fable-5"},
                            "to": {"model": FALLBACK_MODEL},
                        }
                    ],
                },
                {"role": "user", "content": "and again?"},
            ],
            stream=True,
        )
        collect(stream)

        bodies = request_bodies(respx_mock)
        assert len(bodies) == 1
        # stripping left the assistant turn empty, so the turn is omitted —
        # not sent as `content: []`, which the server rejects
        assert bodies[0]["messages"] == [
            {"role": "user", "content": "hello"},
            {"role": "user", "content": "and again?"},
        ]
        # the rest of the request is intact
        assert bodies[0]["model"] == "claude-fable-5"
        assert bodies[0]["max_tokens"] == 1024
        assert beta_headers(respx_mock) == ["fallback-credit-2026-06-01"]


# --- per-hop overrides ----------------------------------------------------------


class TestPerHopOverrides:
    @pytest.mark.respx(base_url=base_url)
    def test_entry_overrides_apply_to_the_hop_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": FALLBACK_MODEL, "max_tokens": 32}])]
        )

        collect(create_stream(client))

        bodies = request_bodies(respx_mock)
        assert bodies[0]["max_tokens"] == 1024
        # the entry's overrides are merged over the hop's body, applied to the
        # serving hop only
        assert bodies[1]["max_tokens"] == 32
        assert bodies[1]["model"] == FALLBACK_MODEL


# --- cancellation -----------------------------------------------------------


class TestCancellation:
    @pytest.mark.respx(base_url=base_url)
    def test_closing_the_stream_mid_passthrough_tears_down_without_a_fallback_request(
        self, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        stream = create_stream(client)
        seen = 0
        for _event in stream:
            seen += 1
            if seen == 2:
                break
        stream.close()

        # The splice never reached A's refusal, so no hop request was issued and
        # teardown released the underlying response without error.
        assert len(respx_mock.calls) == 1


# --- tool-use refusals ----------------------------------------------------
#
# Synthetic SSE (web_search-shaped) built from the documented wire shapes:
# server_tool_use streams its input via input_json_delta after an empty
# `input:{}`, and *_tool_result blocks arrive as a single content_block_start
# with full content (no deltas). The server decides prefillability and
# signals it via `fallback_has_prefill_claim`; the client's only rewrite is
# reassembling tool inputs from their accumulated JSON deltas.

TOOL_USE_ID = "srvtoolu_01"


class TestToolUseRefusals:
    @pytest.mark.respx(base_url=base_url)
    def test_refusal_after_a_completed_server_tool(self, respx_mock: MockRouter) -> None:
        stream_a = "".join(
            [
                message_start(),
                ev(
                    {
                        "type": "content_block_start",
                        "index": 0,
                        "content_block": {"type": "thinking", "thinking": "", "signature": ""},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "thinking_delta", "thinking": "let me look this up"},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "signature_delta", "signature": "sig=="},
                    }
                ),
                ev({"type": "content_block_stop", "index": 0}),
                # server_tool_use: real input arrives via input_json_delta, not content_block_start.
                ev(
                    {
                        "type": "content_block_start",
                        "index": 1,
                        "content_block": {
                            "type": "server_tool_use",
                            "id": TOOL_USE_ID,
                            "name": "web_search",
                            "input": {},
                        },
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 1,
                        "delta": {"type": "input_json_delta", "partial_json": '{"query":"solar eclipse"}'},
                    }
                ),
                ev({"type": "content_block_stop", "index": 1}),
                # web_search_tool_result: full content in the start frame, no deltas.
                ev(
                    {
                        "type": "content_block_start",
                        "index": 2,
                        "content_block": {
                            "type": "web_search_tool_result",
                            "tool_use_id": TOOL_USE_ID,
                            "content": [
                                {
                                    "type": "web_search_result",
                                    "url": "https://example.com",
                                    "title": "x",
                                    "encrypted_content": "e",
                                    "page_age": None,
                                }
                            ],
                        },
                    }
                ),
                ev({"type": "content_block_stop", "index": 2}),
                ev({"type": "content_block_start", "index": 3, "content_block": {"type": "text", "text": ""}}),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 3,
                        "delta": {"type": "text_delta", "text": "Based on that, "},
                    }
                ),
                ev({"type": "content_block_stop", "index": 3}),
                refusal_delta(),
                ev({"type": "message_stop"}),
            ]
        )
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(stream_a), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        # A's four blocks forwarded, fallback boundary at index 4, B continues at 5.
        assert block_starts(events) == [
            (0, "thinking"),
            (1, "server_tool_use"),
            (2, "web_search_tool_result"),
            (3, "text"),
            (4, "fallback"),
            (5, "text"),
        ]

        appended = request_bodies(respx_mock)[1]["messages"][1]
        assert appended["role"] == "assistant"
        assert [block["type"] for block in appended["content"]] == [
            "thinking",
            "server_tool_use",
            "web_search_tool_result",
            "text",
        ]
        # The tool input is the parsed input_json_delta payload, not the empty
        # `{}` from content_block_start.
        assert appended["content"][1] == {
            "type": "server_tool_use",
            "id": TOOL_USE_ID,
            "name": "web_search",
            "input": {"query": "solar eclipse"},
        }
        # The result keeps its pairing id and content.
        assert appended["content"][2]["tool_use_id"] == TOOL_USE_ID

    @pytest.mark.respx(base_url=base_url)
    def test_full_fixture_tool_wire(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A_TOOL), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        events = collect(create_stream(client))

        assert block_starts(events) == [
            (0, "server_tool_use"),
            (1, "web_search_tool_result"),
            (2, "text"),
            (3, "fallback"),
            (4, "text"),
        ]

        appended = request_bodies(respx_mock)[1]["messages"][1]
        assert [block["type"] for block in appended["content"]] == [
            "server_tool_use",
            "web_search_tool_result",
            "text",
        ]
        # Tool input reassembled from the accumulated input_json_delta chunks.
        assert appended["content"][0] == {
            "type": "server_tool_use",
            "id": "srvtoolu_fixture_a_0001",
            "name": "web_search",
            "input": {"query": "solar eclipse viewing safety news 2026"},
        }
        # The result block keeps its pairing id.
        assert appended["content"][1]["tool_use_id"] == "srvtoolu_fixture_a_0001"
        assert appended["content"][1]["type"] == "web_search_tool_result"

    @pytest.mark.respx(base_url=base_url)
    def test_mid_loop_refusal_ending_in_thinking_strips_the_trailing_thinking_block(
        self, respx_mock: MockRouter
    ) -> None:
        # [server_tool_use, result, thinking] — the server granted a prefill
        # claim, but an assistant turn cannot end in a thinking block (the
        # server 400s it), so the trailing thinking is stripped from the
        # appended turn while everything before it is resent verbatim.
        stream_a = "".join(
            [
                message_start(),
                ev(
                    {
                        "type": "content_block_start",
                        "index": 0,
                        "content_block": {
                            "type": "server_tool_use",
                            "id": TOOL_USE_ID,
                            "name": "web_search",
                            "input": {},
                        },
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "input_json_delta", "partial_json": '{"query":"x"}'},
                    }
                ),
                ev({"type": "content_block_stop", "index": 0}),
                ev(
                    {
                        "type": "content_block_start",
                        "index": 1,
                        "content_block": {
                            "type": "web_search_tool_result",
                            "tool_use_id": TOOL_USE_ID,
                            "content": [],
                        },
                    }
                ),
                ev({"type": "content_block_stop", "index": 1}),
                ev(
                    {
                        "type": "content_block_start",
                        "index": 2,
                        "content_block": {"type": "thinking", "thinking": "", "signature": ""},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 2,
                        "delta": {"type": "thinking_delta", "thinking": "hmm"},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 2,
                        "delta": {"type": "signature_delta", "signature": "sig=="},
                    }
                ),
                ev({"type": "content_block_stop", "index": 2}),
                refusal_delta(),
                ev({"type": "message_stop"}),
            ]
        )
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(stream_a), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        collect(create_stream(client))

        body_b = request_bodies(respx_mock)[1]
        assert body_b["fallback_credit_token"] == "tok_abc"
        appended = body_b["messages"][1]
        assert appended["role"] == "assistant"
        assert [block["type"] for block in appended["content"]] == [
            "server_tool_use",
            "web_search_tool_result",
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_a_partial_of_only_thinking_falls_back_to_the_same_body_form(self, respx_mock: MockRouter) -> None:
        # The refusal cut the stream while only a thinking block had streamed:
        # stripping the trailing thinking empties the continuation, so no
        # assistant turn is appended and the token is redeemed against the
        # same body.
        stream_a = "".join(
            [
                message_start(),
                ev(
                    {
                        "type": "content_block_start",
                        "index": 0,
                        "content_block": {"type": "thinking", "thinking": "", "signature": ""},
                    }
                ),
                ev(
                    {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "thinking_delta", "thinking": "hmm"},
                    }
                ),
                ev({"type": "content_block_stop", "index": 0}),
                refusal_delta(),
                ev({"type": "message_stop"}),
            ]
        )
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(stream_a), sse_response(STREAM_B)])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        collect(create_stream(client))

        body_b = request_bodies(respx_mock)[1]
        assert body_b["fallback_credit_token"] == "tok_abc"
        assert body_b["messages"] == PARAMS["messages"]


# --- async ------------------------------------------------------------------


class TestAsyncSplicing:
    @pytest.mark.respx(base_url=base_url)
    async def test_splices_the_fallback_onto_the_refused_stream(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A), sse_response(STREAM_B)])
        client = make_async_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        state = BetaFallbackState()
        with state:
            stream = await create_stream_async(client)
            events: List[BetaRawMessageStreamEvent] = [event async for event in stream]

        assert block_starts(events) == [
            (0, "thinking"),
            (1, "text"),
            (2, "fallback"),
            (3, "text"),
        ]
        assert len([e for e in events if e.type == "message_start"]) == 1
        assert len([e for e in events if e.type == "message_stop"]) == 1
        delta = next(e for e in events if e.type == "message_delta")
        assert delta.delta.stop_reason == "end_turn"
        assert [(i.type, i.model) for i in (delta.usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("fallback_message", FALLBACK_MODEL),
        ]
        assert state.index == 0

        bodies = request_bodies(respx_mock)
        assert bodies[1]["model"] == FALLBACK_MODEL
        assert isinstance(bodies[1]["fallback_credit_token"], str)
        appended = bodies[1]["messages"][1]
        assert appended["role"] == "assistant"
        assert [block["type"] for block in appended["content"]] == ["thinking", "text"]

    @pytest.mark.respx(base_url=base_url)
    async def test_a_refused_hop_splices_its_partial_and_chains_to_the_next_entry(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[sse_response(STREAM_A), sse_response(hop_refusal()), sse_response(STREAM_B)]
        )
        client = make_async_client(middleware=[BetaRefusalFallbackMiddleware(TWO_FALLBACKS)])

        stream = await create_stream_async(client)
        events: List[BetaRawMessageStreamEvent] = [event async for event in stream]

        assert block_starts(events) == [
            (0, "thinking"),
            (1, "text"),
            (2, "fallback"),
            (3, "text"),
            (4, "fallback"),
            (5, "text"),
        ]
        deltas = [e for e in events if e.type == "message_delta"]
        assert len(deltas) == 1
        assert [(i.type, i.model) for i in (deltas[0].usage.iterations or [])] == [  # type: ignore[union-attr]
            ("message", "claude-fable-5"),
            ("message", FALLBACK_MODEL),
            ("fallback_message", SECOND_MODEL),
        ]
        bodies = request_bodies(respx_mock)
        assert bodies[2]["fallback_credit_token"] == "tok_b"

    @pytest.mark.respx(base_url=base_url)
    async def test_closing_the_stream_mid_passthrough_tears_down_without_a_fallback_request(
        self, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse_response(STREAM_A)])
        client = make_async_client(middleware=[BetaRefusalFallbackMiddleware(FALLBACKS)])

        stream = await create_stream_async(client)
        seen = 0
        async for _event in stream:
            seen += 1
            if seen == 2:
                break
        await stream.close()

        assert len(respx_mock.calls) == 1
