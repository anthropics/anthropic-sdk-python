# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaEnvironment,
    BetaEnvironmentDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnvironments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        environment = client.beta.environments.create(
            name="python-data-analysis",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        environment = client.beta.environments.create(
            name="python-data-analysis",
            config={
                "type": "cloud",
                "networking": {
                    "type": "limited",
                    "allow_mcp_servers": True,
                    "allow_package_managers": True,
                    "allowed_hosts": ["api.example.com"],
                },
                "packages": {
                    "apt": ["string"],
                    "cargo": ["string"],
                    "gem": ["string"],
                    "go": ["string"],
                    "npm": ["string"],
                    "pip": ["pandas", "numpy"],
                    "type": "packages",
                },
            },
            description="Python environment with data-analysis packages.",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.environments.with_raw_response.create(
            name="python-data-analysis",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.environments.with_streaming_response.create(
            name="python-data-analysis",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        environment = client.beta.environments.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        environment = client.beta.environments.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.environments.with_raw_response.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.environments.with_streaming_response.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.with_raw_response.retrieve(
                environment_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        environment = client.beta.environments.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        environment = client.beta.environments.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            config={
                "type": "cloud",
                "networking": {
                    "type": "limited",
                    "allow_mcp_servers": True,
                    "allow_package_managers": True,
                    "allowed_hosts": ["api.example.com"],
                },
                "packages": {
                    "apt": ["string"],
                    "cargo": ["string"],
                    "gem": ["string"],
                    "go": ["string"],
                    "npm": ["string"],
                    "pip": ["pandas", "numpy"],
                    "type": "packages",
                },
            },
            description="Python environment with data-analysis packages.",
            metadata={"foo": "string"},
            name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.environments.with_raw_response.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.environments.with_streaming_response.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.with_raw_response.update(
                environment_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        environment = client.beta.environments.list()
        assert_matches_type(SyncPageCursor[BetaEnvironment], environment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        environment = client.beta.environments.list(
            include_archived=True,
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaEnvironment], environment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.environments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(SyncPageCursor[BetaEnvironment], environment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.environments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(SyncPageCursor[BetaEnvironment], environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        environment = client.beta.environments.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        environment = client.beta.environments.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.environments.with_raw_response.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.environments.with_streaming_response.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.with_raw_response.delete(
                environment_id="",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        environment = client.beta.environments.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        environment = client.beta.environments.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.environments.with_raw_response.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.environments.with_streaming_response.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            client.beta.environments.with_raw_response.archive(
                environment_id="",
            )


class TestAsyncEnvironments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.create(
            name="python-data-analysis",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.create(
            name="python-data-analysis",
            config={
                "type": "cloud",
                "networking": {
                    "type": "limited",
                    "allow_mcp_servers": True,
                    "allow_package_managers": True,
                    "allowed_hosts": ["api.example.com"],
                },
                "packages": {
                    "apt": ["string"],
                    "cargo": ["string"],
                    "gem": ["string"],
                    "go": ["string"],
                    "npm": ["string"],
                    "pip": ["pandas", "numpy"],
                    "type": "packages",
                },
            },
            description="Python environment with data-analysis packages.",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.with_raw_response.create(
            name="python-data-analysis",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.with_streaming_response.create(
            name="python-data-analysis",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.with_raw_response.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.with_streaming_response.retrieve(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.with_raw_response.retrieve(
                environment_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            config={
                "type": "cloud",
                "networking": {
                    "type": "limited",
                    "allow_mcp_servers": True,
                    "allow_package_managers": True,
                    "allowed_hosts": ["api.example.com"],
                },
                "packages": {
                    "apt": ["string"],
                    "cargo": ["string"],
                    "gem": ["string"],
                    "go": ["string"],
                    "npm": ["string"],
                    "pip": ["pandas", "numpy"],
                    "type": "packages",
                },
            },
            description="Python environment with data-analysis packages.",
            metadata={"foo": "string"},
            name="x",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.with_raw_response.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.with_streaming_response.update(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.with_raw_response.update(
                environment_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.list()
        assert_matches_type(AsyncPageCursor[BetaEnvironment], environment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.list(
            include_archived=True,
            limit=1,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaEnvironment], environment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(AsyncPageCursor[BetaEnvironment], environment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaEnvironment], environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.with_raw_response.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.with_streaming_response.delete(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(BetaEnvironmentDeleteResponse, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.with_raw_response.delete(
                environment_id="",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        environment = await async_client.beta.environments.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.environments.with_raw_response.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        environment = response.parse()
        assert_matches_type(BetaEnvironment, environment, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.environments.with_streaming_response.archive(
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            environment = await response.parse()
            assert_matches_type(BetaEnvironment, environment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `environment_id` but received ''"):
            await async_client.beta.environments.with_raw_response.archive(
                environment_id="",
            )
