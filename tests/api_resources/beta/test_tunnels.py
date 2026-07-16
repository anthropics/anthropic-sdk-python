# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaTunnel,
    BetaTunnelToken,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTunnels:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.create()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.create(
            display_name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.tunnels.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.tunnels.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = response.parse()
            assert_matches_type(BetaTunnel, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.retrieve(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.retrieve(
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.tunnels.with_raw_response.retrieve(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.tunnels.with_streaming_response.retrieve(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = response.parse()
            assert_matches_type(BetaTunnel, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.with_raw_response.retrieve(
                tunnel_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.list()
        assert_matches_type(SyncPageCursor[BetaTunnel], tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.list(
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaTunnel], tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.tunnels.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(SyncPageCursor[BetaTunnel], tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.tunnels.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = response.parse()
            assert_matches_type(SyncPageCursor[BetaTunnel], tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.archive(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.archive(
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.tunnels.with_raw_response.archive(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.tunnels.with_streaming_response.archive(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = response.parse()
            assert_matches_type(BetaTunnel, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.with_raw_response.archive(
                tunnel_id="",
            )

    @parametrize
    def test_method_reveal_token(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.reveal_token(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    def test_method_reveal_token_with_all_params(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.reveal_token(
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    def test_raw_response_reveal_token(self, client: Anthropic) -> None:
        response = client.beta.tunnels.with_raw_response.reveal_token(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    def test_streaming_response_reveal_token(self, client: Anthropic) -> None:
        with client.beta.tunnels.with_streaming_response.reveal_token(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = response.parse()
            assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_reveal_token(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.with_raw_response.reveal_token(
                tunnel_id="",
            )

    @parametrize
    def test_method_rotate_token(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.rotate_token(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    def test_method_rotate_token_with_all_params(self, client: Anthropic) -> None:
        tunnel = client.beta.tunnels.rotate_token(
            tunnel_id="tunnel_id",
            reason="reason",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    def test_raw_response_rotate_token(self, client: Anthropic) -> None:
        response = client.beta.tunnels.with_raw_response.rotate_token(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    def test_streaming_response_rotate_token(self, client: Anthropic) -> None:
        with client.beta.tunnels.with_streaming_response.rotate_token(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = response.parse()
            assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_rotate_token(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.with_raw_response.rotate_token(
                tunnel_id="",
            )


class TestAsyncTunnels:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.create()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.create(
            display_name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = await response.parse()
            assert_matches_type(BetaTunnel, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.retrieve(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.retrieve(
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.with_raw_response.retrieve(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.with_streaming_response.retrieve(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = await response.parse()
            assert_matches_type(BetaTunnel, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.with_raw_response.retrieve(
                tunnel_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.list()
        assert_matches_type(AsyncPageCursor[BetaTunnel], tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.list(
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaTunnel], tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(AsyncPageCursor[BetaTunnel], tunnel, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaTunnel], tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.archive(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.archive(
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.with_raw_response.archive(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnel, tunnel, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.with_streaming_response.archive(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = await response.parse()
            assert_matches_type(BetaTunnel, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.with_raw_response.archive(
                tunnel_id="",
            )

    @parametrize
    async def test_method_reveal_token(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.reveal_token(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    async def test_method_reveal_token_with_all_params(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.reveal_token(
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    async def test_raw_response_reveal_token(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.with_raw_response.reveal_token(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    async def test_streaming_response_reveal_token(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.with_streaming_response.reveal_token(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = await response.parse()
            assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_reveal_token(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.with_raw_response.reveal_token(
                tunnel_id="",
            )

    @parametrize
    async def test_method_rotate_token(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.rotate_token(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    async def test_method_rotate_token_with_all_params(self, async_client: AsyncAnthropic) -> None:
        tunnel = await async_client.beta.tunnels.rotate_token(
            tunnel_id="tunnel_id",
            reason="reason",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    async def test_raw_response_rotate_token(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.with_raw_response.rotate_token(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tunnel = response.parse()
        assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

    @parametrize
    async def test_streaming_response_rotate_token(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.with_streaming_response.rotate_token(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tunnel = await response.parse()
            assert_matches_type(BetaTunnelToken, tunnel, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_rotate_token(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.with_raw_response.rotate_token(
                tunnel_id="",
            )
