# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaManagedAgentsDeploymentRun,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeploymentRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        deployment_run = client.beta.deployment_runs.retrieve(
            deployment_run_id="deployment_run_id",
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        deployment_run = client.beta.deployment_runs.retrieve(
            deployment_run_id="deployment_run_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.deployment_runs.with_raw_response.retrieve(
            deployment_run_id="deployment_run_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_run = response.parse()
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.deployment_runs.with_streaming_response.retrieve(
            deployment_run_id="deployment_run_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_run = response.parse()
            assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_run_id` but received ''"):
            client.beta.deployment_runs.with_raw_response.retrieve(
                deployment_run_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        deployment_run = client.beta.deployment_runs.list()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        deployment_run = client.beta.deployment_runs.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            deployment_id="deployment_id",
            has_error=True,
            limit=0,
            page="page",
            trigger_type="schedule",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.deployment_runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_run = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.deployment_runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_run = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDeploymentRuns:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        deployment_run = await async_client.beta.deployment_runs.retrieve(
            deployment_run_id="deployment_run_id",
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment_run = await async_client.beta.deployment_runs.retrieve(
            deployment_run_id="deployment_run_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployment_runs.with_raw_response.retrieve(
            deployment_run_id="deployment_run_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_run = response.parse()
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployment_runs.with_streaming_response.retrieve(
            deployment_run_id="deployment_run_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_run = await response.parse()
            assert_matches_type(BetaManagedAgentsDeploymentRun, deployment_run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_run_id` but received ''"):
            await async_client.beta.deployment_runs.with_raw_response.retrieve(
                deployment_run_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        deployment_run = await async_client.beta.deployment_runs.list()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment_run = await async_client.beta.deployment_runs.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            deployment_id="deployment_id",
            has_error=True,
            limit=0,
            page="page",
            trigger_type="schedule",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployment_runs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment_run = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployment_runs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment_run = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeploymentRun], deployment_run, path=["response"])

        assert cast(Any, response.is_closed) is True
