from __future__ import annotations

import os
import json
import logging
import threading
from typing import Any, List, Protocol, cast

import httpx
import pytest
from respx import MockRouter

from anthropic import (
    Omit,
    Anthropic,
    AnthropicError,
    AsyncAnthropic,
    BetaFallbackState,
    BetaRefusalFallbackMiddleware,
    omit,
)
from anthropic.types.beta import BetaMessage, BetaFallbackParam
from anthropic.lib.middleware._fallbacks import _fallback_state
from anthropic.types.anthropic_beta_param import AnthropicBetaParam

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

LOGGER_NAME = "anthropic.lib.middleware"


def make_sync_client(**kwargs: Any) -> Anthropic:
    return Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, max_retries=0, **kwargs)


def make_async_client(**kwargs: Any) -> AsyncAnthropic:
    return AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, max_retries=0, **kwargs)


def message(model: str, **overrides: Any) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "msg_1",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": [],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
            **overrides,
        },
    )


def refusal(model: str, fallback_credit_token: str | None = None) -> httpx.Response:
    return message(
        model,
        stop_reason="refusal",
        stop_details={
            "type": "refusal",
            "category": None,
            "explanation": None,
            "fallback_credit_token": fallback_credit_token,
        },
    )


class MockRequestCall(Protocol):
    request: httpx.Request


def create_message(
    client: Anthropic,
    *,
    betas: List[AnthropicBetaParam] | Omit = omit,
    fallbacks: List[BetaFallbackParam] | Omit = omit,
) -> BetaMessage:
    return client.beta.messages.create(
        model="primary-model",
        max_tokens=1024,
        messages=[{"role": "user", "content": "hi"}],
        betas=betas,
        fallbacks=fallbacks,
    )


async def create_message_async(client: AsyncAnthropic) -> BetaMessage:
    return await client.beta.messages.create(
        model="primary-model",
        max_tokens=1024,
        messages=[{"role": "user", "content": "hi"}],
    )


def request_bodies(respx_mock: MockRouter) -> list[dict[str, Any]]:
    calls = cast("list[MockRequestCall]", respx_mock.calls)
    return [cast("dict[str, Any]", json.loads(call.request.content)) for call in calls]


def beta_headers(respx_mock: MockRouter) -> list[str | None]:
    calls = cast("list[MockRequestCall]", respx_mock.calls)
    return [call.request.headers.get("anthropic-beta") for call in calls]


class TestRefusalFallback:
    @pytest.mark.respx(base_url=base_url)
    def test_retries_a_refusal_with_the_fallback_params_and_credit_token(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model", "credit-token"), message("fallback-model")]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        result = create_message(client)

        assert result.model == "fallback-model"
        assert result.stop_reason == "end_turn"
        # a `fallback` seam block is prepended at the model boundary — the same
        # block shape the streaming splice emits
        assert [block.to_dict() for block in result.content] == [
            {"type": "fallback", "from": {"model": "primary-model"}, "to": {"model": "fallback-model"}, "trigger": {"type": "refusal", "category": None}}
        ]
        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["primary-model", "fallback-model"]
        assert bodies[1]["fallback_credit_token"] == "credit-token"

    @pytest.mark.respx(base_url=base_url)
    def test_pins_the_conversation_to_the_accepted_fallback_via_state(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model"), message("fallback-model"), message("fallback-model")]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        state = BetaFallbackState()
        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            with state:
                create_message(client)
            assert state.index == 0

            # the follow-up goes straight to the pinned fallback in a single request
            with state:
                create_message(client)

        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["primary-model", "fallback-model", "fallback-model"]
        assert not [record for record in caplog.records if record.name == LOGGER_NAME]

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_raises_if_state_index_is_out_of_bounds_for_the_chain(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("fallback-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        state = BetaFallbackState()
        state.index = 1
        with state:
            with pytest.raises(
                AnthropicError, match=r"BetaFallbackState\.index 1 is out of bounds for a chain of 1 fallback\(s\)"
            ):
                create_message(client)
        assert len(respx_mock.calls) == 0

    @pytest.mark.respx(base_url=base_url)
    def test_warns_once_when_falling_back_without_a_state(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                refusal("primary-model"),
                message("fallback-model"),
                refusal("primary-model"),
                message("fallback-model"),
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
            create_message(client)
            create_message(client)

        warnings = [record for record in caplog.records if record.name == LOGGER_NAME]
        assert len(warnings) == 1
        assert "BetaFallbackState" in warnings[0].getMessage()

    @pytest.mark.respx(base_url=base_url)
    def test_a_separate_conversation_is_unaffected_by_another_state(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model"), message("fallback-model"), message("primary-model")]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        with BetaFallbackState():
            create_message(client)
        with BetaFallbackState():
            create_message(client)

        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["primary-model", "fallback-model", "primary-model"]

    @pytest.mark.respx(base_url=base_url)
    def test_leaves_accepted_requests_and_the_response_untouched(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        state = BetaFallbackState()
        with state:
            result = create_message(client)

        assert result.model == "primary-model"
        bodies = request_bodies(respx_mock)
        assert len(bodies) == 1
        assert "fallback_credit_token" not in bodies[0]
        assert state.index is None

    @pytest.mark.respx(base_url=base_url)
    def test_walks_each_hop_through_the_chain_until_a_model_accepts(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                refusal("primary-model"),
                refusal("mid-model"),
                message("last-model", content=[{"type": "text", "text": "ok"}]),
            ]
        )
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": "mid-model"}, {"model": "last-model"}])]
        )

        state = BetaFallbackState()
        with state:
            result = create_message(client)

        assert result.model == "last-model"
        assert state.index == 1
        # one seam per model boundary, in hop order, ahead of the served content
        assert [block.to_dict() for block in result.content] == [
            {"type": "fallback", "from": {"model": "primary-model"}, "to": {"model": "mid-model"}, "trigger": {"type": "refusal", "category": None}},
            {"type": "fallback", "from": {"model": "mid-model"}, "to": {"model": "last-model"}, "trigger": {"type": "refusal", "category": None}},
            {"type": "text", "text": "ok"},
        ]
        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["primary-model", "mid-model", "last-model"]

    @pytest.mark.respx(base_url=base_url)
    def test_a_pinned_continuation_seams_from_the_pinned_model(self, respx_mock: MockRouter) -> None:
        # the pinned entry refuses and the chain advances — the first seam's
        # `from.model` must be the pinned entry (the model actually queried),
        # not the caller's original body model
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("mid-model"), message("last-model", content=[{"type": "text", "text": "ok"}])]
        )
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": "mid-model"}, {"model": "last-model"}])]
        )

        state = BetaFallbackState()
        state.index = 0
        with state:
            result = create_message(client)

        assert result.model == "last-model"
        assert [block.to_dict() for block in result.content] == [
            {"type": "fallback", "from": {"model": "mid-model"}, "to": {"model": "last-model"}, "trigger": {"type": "refusal", "category": None}},
            {"type": "text", "text": "ok"},
        ]
        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["mid-model", "last-model"]

    @pytest.mark.respx(base_url=base_url)
    def test_returns_the_final_refusal_once_the_chain_is_exhausted(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[refusal("primary-model"), refusal("fallback-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        result = create_message(client)

        assert result.model == "fallback-model"
        assert result.stop_reason == "refusal"
        # terminal refusal is surfaced verbatim — no seam blocks prepended
        assert result.content == []
        assert len(respx_mock.calls) == 2

    @pytest.mark.respx(base_url=base_url)
    def test_entry_overrides_are_merged_whole_over_the_body(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[refusal("primary-model"), message("fallback-model")])
        client = make_sync_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model", "max_tokens": 32}])]
        )

        create_message(client)

        bodies = request_bodies(respx_mock)
        assert bodies[0]["max_tokens"] == 1024
        assert bodies[1]["max_tokens"] == 32

    @pytest.mark.respx(base_url=base_url)
    def test_a_hop_http_error_surfaces_to_the_app(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                refusal("primary-model", "credit-token"),
                httpx.Response(
                    400, json={"type": "error", "error": {"type": "invalid_request_error", "message": "nope"}}
                ),
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        from anthropic import BadRequestError

        with pytest.raises(BadRequestError):
            create_message(client)
        assert len(respx_mock.calls) == 2

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_server_side_fallbacks_raise_an_error(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[refusal("primary-model", "credit-token")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        with pytest.raises(
            AnthropicError,
            match=r"Sending the `fallbacks:` request param is not supported when using the `BetaRefusalFallbackMiddleware`\. You should either remove the middleware and send `fallbacks:` with the `server-side-fallback-2026-06-01` beta header to let the API handle refusal fallbacks, or omit the `fallbacks:` param if you'd like `BetaRefusalFallbackMiddleware` to handle fallbacks on the client side\.",
        ):
            create_message(client, fallbacks=[{"model": "server-fallback"}])
        # the error is raised before any request is sent
        assert len(respx_mock.calls) == 0

    @pytest.mark.respx(base_url=base_url)
    def test_an_empty_chain_disables_the_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[refusal("primary-model", "credit-token")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([])])

        result = create_message(client)

        assert result.stop_reason == "refusal"
        assert len(respx_mock.calls) == 1
        assert beta_headers(respx_mock) == [None]

    @pytest.mark.respx(base_url=base_url)
    def test_the_non_beta_messages_surface_passes_through(self, respx_mock: MockRouter) -> None:
        # only `client.beta.messages` requests are handled; the first-party
        # surface mints no credit tokens, so its refusals surface as-is
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                message(
                    "primary-model",
                    stop_reason="refusal",
                    stop_details={"type": "refusal", "category": None, "explanation": None},
                )
            ]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        result = client.messages.create(
            model="primary-model",
            max_tokens=1024,
            messages=[{"role": "user", "content": "hi"}],
        )

        assert result.stop_reason == "refusal"
        assert len(respx_mock.calls) == 1
        assert beta_headers(respx_mock) == [None]


class TestBetaHeader:
    @pytest.mark.respx(base_url=base_url)
    def test_sends_the_fallback_credit_beta_on_the_original_and_fallback_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model", "credit-token"), message("fallback-model")]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        create_message(client)

        assert beta_headers(respx_mock) == ["fallback-credit-2026-06-01", "fallback-credit-2026-06-01"]

    @pytest.mark.respx(base_url=base_url)
    def test_the_betas_option_replaces_the_default(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(
            middleware=[
                BetaRefusalFallbackMiddleware(
                    [{"model": "fallback-model"}],
                    betas=["fallback-credit-2027-01-01", "interleaved-thinking-2025-05-14"],
                )
            ]
        )

        create_message(client)

        assert beta_headers(respx_mock) == ["fallback-credit-2027-01-01, interleaved-thinking-2025-05-14"]

    @pytest.mark.respx(base_url=base_url)
    def test_empty_betas_sends_no_beta_header(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}], betas=[])])

        create_message(client)

        assert beta_headers(respx_mock) == [None]

    @pytest.mark.respx(base_url=base_url)
    def test_does_not_duplicate_a_beta_already_on_the_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        create_message(client, betas=["fallback-credit-2026-06-01"])

        assert beta_headers(respx_mock) == ["fallback-credit-2026-06-01"]

    @pytest.mark.respx(base_url=base_url)
    def test_appends_to_betas_already_on_the_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        create_message(client, betas=["interleaved-thinking-2025-05-14"])

        assert beta_headers(respx_mock) == ["interleaved-thinking-2025-05-14, fallback-credit-2026-06-01"]


def helper_headers(respx_mock: MockRouter) -> list[list[str]]:
    calls = cast("list[MockRequestCall]", respx_mock.calls)
    return [call.request.headers.get_list("x-stainless-helper") for call in calls]


class TestHelperTelemetry:
    @pytest.mark.respx(base_url=base_url)
    def test_tags_the_original_and_fallback_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model", "credit-token"), message("fallback-model")]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])
        create_message(client)
        assert helper_headers(respx_mock) == [
            ["fallback-refusal-middleware"],
            ["fallback-refusal-middleware"],
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_appends_to_a_helper_tag_already_on_the_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])
        client.beta.messages.create(
            model="primary-model",
            max_tokens=1024,
            messages=[{"role": "user", "content": "hi"}],
            extra_headers={"X-Stainless-Helper": "BetaToolRunner"},
        )
        assert helper_headers(respx_mock) == [["BetaToolRunner, fallback-refusal-middleware"]]

    @pytest.mark.respx(base_url=base_url)
    def test_does_not_tag_requests_it_passes_through(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[message("primary-model")])
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])
        # the GA surface is not applicable to this middleware
        client.messages.create(
            model="primary-model",
            max_tokens=1024,
            messages=[{"role": "user", "content": "hi"}],
        )
        assert helper_headers(respx_mock) == [[]]

    @pytest.mark.respx(base_url=base_url)
    async def test_async_tags_the_original_and_fallback_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model", "credit-token"), message("fallback-model")]
        )
        client = make_async_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])
        await create_message_async(client)
        assert helper_headers(respx_mock) == [
            ["fallback-refusal-middleware"],
            ["fallback-refusal-middleware"],
        ]


class TestAsyncRefusalFallback:
    @pytest.mark.respx(base_url=base_url)
    async def test_retries_a_refusal_with_the_fallback_params_and_credit_token(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model", "credit-token"), message("fallback-model")]
        )
        client = make_async_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        result = await create_message_async(client)

        assert result.model == "fallback-model"
        assert [block.to_dict() for block in result.content] == [
            {"type": "fallback", "from": {"model": "primary-model"}, "to": {"model": "fallback-model"}, "trigger": {"type": "refusal", "category": None}}
        ]
        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["primary-model", "fallback-model"]
        assert bodies[1]["fallback_credit_token"] == "credit-token"

    @pytest.mark.respx(base_url=base_url)
    async def test_pins_the_conversation_to_the_accepted_fallback_via_state(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model"), message("fallback-model"), message("fallback-model")]
        )
        client = make_async_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        state = BetaFallbackState()
        with state:
            await create_message_async(client)
        assert state.index == 0

        with state:
            await create_message_async(client)

        bodies = request_bodies(respx_mock)
        assert [body["model"] for body in bodies] == ["primary-model", "fallback-model", "fallback-model"]

    @pytest.mark.respx(base_url=base_url)
    async def test_walks_each_hop_through_the_chain_until_a_model_accepts(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model"), refusal("mid-model"), message("last-model")]
        )
        client = make_async_client(
            middleware=[BetaRefusalFallbackMiddleware([{"model": "mid-model"}, {"model": "last-model"}])]
        )

        state = BetaFallbackState()
        with state:
            result = await create_message_async(client)

        assert result.model == "last-model"
        assert state.index == 1


class TestBetaFallbackState:
    def test_reentering_the_same_state_nests(self) -> None:
        state = BetaFallbackState()
        with state:
            with state:
                assert _fallback_state.get() is state
            assert _fallback_state.get() is state
        assert _fallback_state.get() is None

    def test_nesting_different_states_restores_the_outer_pin(self) -> None:
        outer, inner = BetaFallbackState(), BetaFallbackState()
        with outer:
            with inner:
                assert _fallback_state.get() is inner
            assert _fallback_state.get() is outer
        assert _fallback_state.get() is None

    def test_one_state_shared_across_threads(self) -> None:
        # Each thread runs in its own context, so a state shared between them —
        # the documented usage — must enter and exit with that context's own
        # tokens; an instance-level token stack would interleave them and
        # `ContextVar.reset` raises on a foreign context's token.
        state = BetaFallbackState()
        a_entered, b_entered, a_exited = threading.Event(), threading.Event(), threading.Event()
        errors: list[Exception] = []

        def thread_a() -> None:
            try:
                with state:
                    a_entered.set()
                    assert b_entered.wait(timeout=5)
            except Exception as err:
                errors.append(err)
            finally:
                a_entered.set()
                a_exited.set()

        def thread_b() -> None:
            try:
                assert a_entered.wait(timeout=5)
                with state:
                    b_entered.set()
                    assert a_exited.wait(timeout=5)
                assert _fallback_state.get() is None
            except Exception as err:
                errors.append(err)
            finally:
                b_entered.set()

        threads = [threading.Thread(target=thread_a), threading.Thread(target=thread_b)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        assert errors == []


class TestErrorLogging:
    @pytest.mark.respx(base_url=base_url)
    def test_nothing_is_logged_for_non_streaming_retries(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[refusal("primary-model", "credit-token"), message("fallback-model")]
        )
        client = make_sync_client(middleware=[BetaRefusalFallbackMiddleware([{"model": "fallback-model"}])])

        create_message(client)

        assert not [
            record for record in caplog.records if record.name == LOGGER_NAME and record.levelno >= logging.ERROR
        ]
