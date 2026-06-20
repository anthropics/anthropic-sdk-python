# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.environments import (
    BetaSelfHostedWork,
    BetaSelfHostedWorkQueueStats,
    BetaSelfHostedWorkHeartbeatResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWork:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        work = client.beta.environments.work.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.retrieve(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            client.beta.environments.work.with_raw_response.retrieve(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        work = client.beta.environments.work.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.update(
                work_id="work_id",
                environment_id="",
                metadata={"foo": "string"},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            client.beta.environments.work.with_raw_response.update(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
                metadata={"foo": "string"},
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        work = client.beta.environments.work.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(SyncPageCursor[BetaSelfHostedWork], work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaSelfHostedWork], work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(SyncPageCursor[BetaSelfHostedWork], work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(SyncPageCursor[BetaSelfHostedWork], work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.list(
                environment_id="",
            )

    @parametrize
    def test_method_ack(self, client: Anthropic) -> None:
        work = client.beta.environments.work.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_method_ack_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_raw_response_ack(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_streaming_response_ack(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_ack(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.ack(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            client.beta.environments.work.with_raw_response.ack(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )

    @parametrize
    def test_method_heartbeat(self, client: Anthropic) -> None:
        work = client.beta.environments.work.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

    @parametrize
    def test_method_heartbeat_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            desired_ttl_seconds=0,
            expected_last_heartbeat="expected_last_heartbeat",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

    @parametrize
    def test_raw_response_heartbeat(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

    @parametrize
    def test_streaming_response_heartbeat(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_heartbeat(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.heartbeat(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            client.beta.environments.work.with_raw_response.heartbeat(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )

    @parametrize
    def test_method_poll(self, client: Anthropic) -> None:
        work = client.beta.environments.work.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

    @parametrize
    def test_method_poll_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            block_ms=1,
            reclaim_older_than_ms=1,
            betas=["message-batches-2024-09-24"],
            anthropic_worker_id="Anthropic-Worker-ID",
        )
        assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

    @parametrize
    def test_raw_response_poll(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

    @parametrize
    def test_streaming_response_poll(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_poll(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.poll(
                environment_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_stats(self, client: Anthropic) -> None:
        work = client.beta.environments.work.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_stats_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_stats(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_stats(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_stats(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.stats(
                environment_id="",
            )

    @parametrize
    def test_method_stop(self, client: Anthropic) -> None:
        work = client.beta.environments.work.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_method_stop_with_all_params(self, client: Anthropic) -> None:
        work = client.beta.environments.work.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            force=True,
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_raw_response_stop(self, client: Anthropic) -> None:
        response = client.beta.environments.work.with_raw_response.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    def test_streaming_response_stop(self, client: Anthropic) -> None:
        with client.beta.environments.work.with_streaming_response.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_stop(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.work.with_raw_response.stop(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            client.beta.environments.work.with_raw_response.stop(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )


class TestAsyncWork:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.retrieve(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.retrieve(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.retrieve(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.update(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.update(
                work_id="work_id",
                environment_id="",
                metadata={"foo": "string"},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.update(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
                metadata={"foo": "string"},
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(AsyncPageCursor[BetaSelfHostedWork], work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaSelfHostedWork], work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(AsyncPageCursor[BetaSelfHostedWork], work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.list(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaSelfHostedWork], work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.list(
                environment_id="",
            )

    @parametrize
    async def test_method_ack(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_method_ack_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_raw_response_ack(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_streaming_response_ack(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.ack(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_ack(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.ack(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.ack(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )

    @parametrize
    async def test_method_heartbeat(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

    @parametrize
    async def test_method_heartbeat_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            desired_ttl_seconds=0,
            expected_last_heartbeat="expected_last_heartbeat",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

    @parametrize
    async def test_raw_response_heartbeat(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

    @parametrize
    async def test_streaming_response_heartbeat(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.heartbeat(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(BetaSelfHostedWorkHeartbeatResponse, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_heartbeat(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.heartbeat(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.heartbeat(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )

    @parametrize
    async def test_method_poll(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

    @parametrize
    async def test_method_poll_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            block_ms=1,
            reclaim_older_than_ms=1,
            betas=["message-batches-2024-09-24"],
            anthropic_worker_id="Anthropic-Worker-ID",
        )
        assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

    @parametrize
    async def test_raw_response_poll(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

    @parametrize
    async def test_streaming_response_poll(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.poll(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(Optional[BetaSelfHostedWork], work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_poll(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.poll(
                environment_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_stats(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_stats_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_stats(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_stats(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.stats(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(BetaSelfHostedWorkQueueStats, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_stats(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.stats(
                environment_id="",
            )

    @parametrize
    async def test_method_stop(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_method_stop_with_all_params(self, async_client: AsyncAnthropic) -> None:
        work = await async_client.beta.environments.work.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            force=True,
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_raw_response_stop(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.work.with_raw_response.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        work = response.parse()
        assert_matches_type(BetaSelfHostedWork, work, path=["response"])

    @parametrize
    async def test_streaming_response_stop(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.work.with_streaming_response.stop(
            work_id="work_id",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            work = await response.parse()
            assert_matches_type(BetaSelfHostedWork, work, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_stop(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.stop(
                work_id="work_id",
                environment_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `work_id` but received ''"):
            await async_client.beta.environments.work.with_raw_response.stop(
                work_id="",
                environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            )
