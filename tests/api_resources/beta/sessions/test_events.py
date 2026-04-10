# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.sessions import (
    BetaManagedAgentsSessionEvent,
    BetaManagedAgentsSendSessionEvents,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        event = client.beta.sessions.events.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        event = client.beta.sessions.events.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            limit=0,
            order="asc",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.sessions.events.with_raw_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.sessions.events.with_streaming_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.events.with_raw_response.list(
                session_id="",
            )

    @parametrize
    def test_method_send(self, client: Anthropic) -> None:
        event = client.beta.sessions.events.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
        )
        assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

    @parametrize
    def test_method_send_with_all_params(self, client: Anthropic) -> None:
        event = client.beta.sessions.events.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

    @parametrize
    def test_raw_response_send(self, client: Anthropic) -> None:
        response = client.beta.sessions.events.with_raw_response.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

    @parametrize
    def test_streaming_response_send(self, client: Anthropic) -> None:
        with client.beta.sessions.events.with_streaming_response.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_send(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.events.with_raw_response.send(
                session_id="",
                events=[
                    {
                        "content": [
                            {
                                "text": "Where is my order #1234?",
                                "type": "text",
                            }
                        ],
                        "type": "user.message",
                    }
                ],
            )

    @parametrize
    def test_method_stream(self, client: Anthropic) -> None:
        event_stream = client.beta.sessions.events.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        event_stream.response.close()

    @parametrize
    def test_method_stream_with_all_params(self, client: Anthropic) -> None:
        event_stream = client.beta.sessions.events.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        event_stream.response.close()

    @parametrize
    def test_raw_response_stream(self, client: Anthropic) -> None:
        response = client.beta.sessions.events.with_raw_response.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_stream(self, client: Anthropic) -> None:
        with client.beta.sessions.events.with_streaming_response.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_stream(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.events.with_raw_response.stream(
                session_id="",
            )


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        event = await async_client.beta.sessions.events.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        event = await async_client.beta.sessions.events.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            limit=0,
            order="asc",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.events.with_raw_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.events.with_streaming_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionEvent], event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.events.with_raw_response.list(
                session_id="",
            )

    @parametrize
    async def test_method_send(self, async_client: AsyncAnthropic) -> None:
        event = await async_client.beta.sessions.events.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
        )
        assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

    @parametrize
    async def test_method_send_with_all_params(self, async_client: AsyncAnthropic) -> None:
        event = await async_client.beta.sessions.events.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

    @parametrize
    async def test_raw_response_send(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.events.with_raw_response.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

    @parametrize
    async def test_streaming_response_send(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.events.with_streaming_response.send(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            events=[
                {
                    "content": [
                        {
                            "text": "Where is my order #1234?",
                            "type": "text",
                        }
                    ],
                    "type": "user.message",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(BetaManagedAgentsSendSessionEvents, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_send(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.events.with_raw_response.send(
                session_id="",
                events=[
                    {
                        "content": [
                            {
                                "text": "Where is my order #1234?",
                                "type": "text",
                            }
                        ],
                        "type": "user.message",
                    }
                ],
            )

    @parametrize
    async def test_method_stream(self, async_client: AsyncAnthropic) -> None:
        event_stream = await async_client.beta.sessions.events.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        await event_stream.response.aclose()

    @parametrize
    async def test_method_stream_with_all_params(self, async_client: AsyncAnthropic) -> None:
        event_stream = await async_client.beta.sessions.events.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        await event_stream.response.aclose()

    @parametrize
    async def test_raw_response_stream(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.events.with_raw_response.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_stream(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.events.with_streaming_response.stream(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_stream(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.events.with_raw_response.stream(
                session_id="",
            )
