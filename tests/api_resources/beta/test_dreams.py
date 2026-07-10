# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import BetaDream

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDreams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        dream = client.beta.dreams.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        dream = client.beta.dreams.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
            instructions="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.dreams.with_raw_response.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.dreams.with_streaming_response.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        dream = client.beta.dreams.retrieve(
            dream_id="dream_id",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        dream = client.beta.dreams.retrieve(
            dream_id="dream_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.dreams.with_raw_response.retrieve(
            dream_id="dream_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.dreams.with_streaming_response.retrieve(
            dream_id="dream_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dream_id` but received ''"):
            client.beta.dreams.with_raw_response.retrieve(
                dream_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        dream = client.beta.dreams.list()
        assert_matches_type(SyncPageCursor[BetaDream], dream, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        dream = client.beta.dreams.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            statuses=["pending"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaDream], dream, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.dreams.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(SyncPageCursor[BetaDream], dream, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.dreams.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = response.parse()
            assert_matches_type(SyncPageCursor[BetaDream], dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        dream = client.beta.dreams.archive(
            dream_id="dream_id",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        dream = client.beta.dreams.archive(
            dream_id="dream_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.dreams.with_raw_response.archive(
            dream_id="dream_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.dreams.with_streaming_response.archive(
            dream_id="dream_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dream_id` but received ''"):
            client.beta.dreams.with_raw_response.archive(
                dream_id="",
            )

    @parametrize
    def test_method_cancel(self, client: Anthropic) -> None:
        dream = client.beta.dreams.cancel(
            dream_id="dream_id",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_method_cancel_with_all_params(self, client: Anthropic) -> None:
        dream = client.beta.dreams.cancel(
            dream_id="dream_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_raw_response_cancel(self, client: Anthropic) -> None:
        response = client.beta.dreams.with_raw_response.cancel(
            dream_id="dream_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    def test_streaming_response_cancel(self, client: Anthropic) -> None:
        with client.beta.dreams.with_streaming_response.cancel(
            dream_id="dream_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cancel(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dream_id` but received ''"):
            client.beta.dreams.with_raw_response.cancel(
                dream_id="",
            )


class TestAsyncDreams:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
            instructions="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.dreams.with_raw_response.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.dreams.with_streaming_response.create(
            inputs=[
                {
                    "memory_store_id": "x",
                    "type": "memory_store",
                }
            ],
            model="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = await response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.retrieve(
            dream_id="dream_id",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.retrieve(
            dream_id="dream_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.dreams.with_raw_response.retrieve(
            dream_id="dream_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.dreams.with_streaming_response.retrieve(
            dream_id="dream_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = await response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dream_id` but received ''"):
            await async_client.beta.dreams.with_raw_response.retrieve(
                dream_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.list()
        assert_matches_type(AsyncPageCursor[BetaDream], dream, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            statuses=["pending"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaDream], dream, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.dreams.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(AsyncPageCursor[BetaDream], dream, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.dreams.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaDream], dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.archive(
            dream_id="dream_id",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.archive(
            dream_id="dream_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.dreams.with_raw_response.archive(
            dream_id="dream_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.dreams.with_streaming_response.archive(
            dream_id="dream_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = await response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dream_id` but received ''"):
            await async_client.beta.dreams.with_raw_response.archive(
                dream_id="",
            )

    @parametrize
    async def test_method_cancel(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.cancel(
            dream_id="dream_id",
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_method_cancel_with_all_params(self, async_client: AsyncAnthropic) -> None:
        dream = await async_client.beta.dreams.cancel(
            dream_id="dream_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.dreams.with_raw_response.cancel(
            dream_id="dream_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dream = response.parse()
        assert_matches_type(BetaDream, dream, path=["response"])

    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.dreams.with_streaming_response.cancel(
            dream_id="dream_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dream = await response.parse()
            assert_matches_type(BetaDream, dream, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dream_id` but received ''"):
            await async_client.beta.dreams.with_raw_response.cancel(
                dream_id="",
            )
