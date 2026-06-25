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
    BetaManagedAgentsDeployment,
    BetaManagedAgentsDeploymentRun,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
            description="description",
            metadata={"foo": "string"},
            resources=[
                {
                    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
                    "type": "file",
                    "mount_path": "/uploads/receipt.pdf",
                }
            ],
            schedule={
                "expression": "0 9 * * 1-5",
                "timezone": "America/Los_Angeles",
                "type": "cron",
            },
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.beta.deployments.with_raw_response.retrieve(
                deployment_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            agent="string",
            description="description",
            environment_id="environment_id",
            initial_events=[
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
            metadata={"foo": "string"},
            name="name",
            resources=[
                {
                    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
                    "type": "file",
                    "mount_path": "/uploads/receipt.pdf",
                }
            ],
            schedule={
                "expression": "0 9 * * 1-5",
                "timezone": "America/Los_Angeles",
                "type": "cron",
            },
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.beta.deployments.with_raw_response.update(
                deployment_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.list()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.list(
            agent_id="agent_id",
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            status="active",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.beta.deployments.with_raw_response.archive(
                deployment_id="",
            )

    @parametrize
    def test_method_pause(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_method_pause_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_pause(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_pause(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_pause(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.beta.deployments.with_raw_response.pause(
                deployment_id="",
            )

    @parametrize
    def test_method_run(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

    @parametrize
    def test_method_run_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

    @parametrize
    def test_raw_response_run(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

    @parametrize
    def test_streaming_response_run(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_run(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.beta.deployments.with_raw_response.run(
                deployment_id="",
            )

    @parametrize
    def test_method_unpause(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_method_unpause_with_all_params(self, client: Anthropic) -> None:
        deployment = client.beta.deployments.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_raw_response_unpause(self, client: Anthropic) -> None:
        response = client.beta.deployments.with_raw_response.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    def test_streaming_response_unpause(self, client: Anthropic) -> None:
        with client.beta.deployments.with_streaming_response.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_unpause(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.beta.deployments.with_raw_response.unpause(
                deployment_id="",
            )


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
            description="description",
            metadata={"foo": "string"},
            resources=[
                {
                    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
                    "type": "file",
                    "mount_path": "/uploads/receipt.pdf",
                }
            ],
            schedule={
                "expression": "0 9 * * 1-5",
                "timezone": "America/Los_Angeles",
                "type": "cron",
            },
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.create(
            agent="string",
            environment_id="x",
            initial_events=[
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
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.retrieve(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.beta.deployments.with_raw_response.retrieve(
                deployment_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            agent="string",
            description="description",
            environment_id="environment_id",
            initial_events=[
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
            metadata={"foo": "string"},
            name="name",
            resources=[
                {
                    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
                    "type": "file",
                    "mount_path": "/uploads/receipt.pdf",
                }
            ],
            schedule={
                "expression": "0 9 * * 1-5",
                "timezone": "America/Los_Angeles",
                "type": "cron",
            },
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.update(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.beta.deployments.with_raw_response.update(
                deployment_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.list()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.list(
            agent_id="agent_id",
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            page="page",
            status="active",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsDeployment], deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.archive(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.beta.deployments.with_raw_response.archive(
                deployment_id="",
            )

    @parametrize
    async def test_method_pause(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_pause_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_pause(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_pause(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.pause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_pause(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.beta.deployments.with_raw_response.pause(
                deployment_id="",
            )

    @parametrize
    async def test_method_run(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

    @parametrize
    async def test_method_run_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

    @parametrize
    async def test_raw_response_run(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_run(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.run(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeploymentRun, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_run(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.beta.deployments.with_raw_response.run(
                deployment_id="",
            )

    @parametrize
    async def test_method_unpause(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_method_unpause_with_all_params(self, async_client: AsyncAnthropic) -> None:
        deployment = await async_client.beta.deployments.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_raw_response_unpause(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.deployments.with_raw_response.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

    @parametrize
    async def test_streaming_response_unpause(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.deployments.with_streaming_response.unpause(
            deployment_id="depl_011CZkZcDH3vPqd7xnEfwTai",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(BetaManagedAgentsDeployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_unpause(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.beta.deployments.with_raw_response.unpause(
                deployment_id="",
            )
