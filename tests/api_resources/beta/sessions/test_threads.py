# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.sessions import BetaManagedAgentsSessionThread

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        thread = client.beta.sessions.threads.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        thread = client.beta.sessions.threads.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.sessions.threads.with_raw_response.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.sessions.threads.with_streaming_response.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.threads.with_raw_response.retrieve(
                thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.beta.sessions.threads.with_raw_response.retrieve(
                thread_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        thread = client.beta.sessions.threads.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        thread = client.beta.sessions.threads.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.sessions.threads.with_raw_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.sessions.threads.with_streaming_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.threads.with_raw_response.list(
                session_id="",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        thread = client.beta.sessions.threads.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        thread = client.beta.sessions.threads.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.sessions.threads.with_raw_response.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.sessions.threads.with_streaming_response.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.threads.with_raw_response.archive(
                thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.beta.sessions.threads.with_raw_response.archive(
                thread_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        thread = await async_client.beta.sessions.threads.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        thread = await async_client.beta.sessions.threads.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.threads.with_raw_response.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.threads.with_streaming_response.retrieve(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.threads.with_raw_response.retrieve(
                thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.beta.sessions.threads.with_raw_response.retrieve(
                thread_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        thread = await async_client.beta.sessions.threads.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        thread = await async_client.beta.sessions.threads.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.threads.with_raw_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.threads.with_streaming_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionThread], thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.threads.with_raw_response.list(
                session_id="",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        thread = await async_client.beta.sessions.threads.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        thread = await async_client.beta.sessions.threads.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.threads.with_raw_response.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.threads.with_streaming_response.archive(
            thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(BetaManagedAgentsSessionThread, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.threads.with_raw_response.archive(
                thread_id="sthr_011CZkZVWa6oIjw0rgXZpnBt",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.beta.sessions.threads.with_raw_response.archive(
                thread_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )
