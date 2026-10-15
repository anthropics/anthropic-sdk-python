from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaPlugin,
    BetaDeletedPlugin,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPlugins:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.create(
            files=[b"Example data"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.create(
            files=[b"Example data"],
            marketplace_id="marketplace_id",
            release_notes="release_notes",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.with_raw_response.create(
            files=[b"Example data"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = response.parse()
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.with_streaming_response.create(
            files=[b"Example data"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = response.parse()
            assert_matches_type(BetaPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.retrieve(
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.retrieve(
            plugin_id="plugin_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.with_raw_response.retrieve(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = response.parse()
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.with_streaming_response.retrieve(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = response.parse()
            assert_matches_type(BetaPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.with_raw_response.retrieve(
                plugin_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.with_raw_response.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = response.parse()
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.with_streaming_response.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = response.parse()
            assert_matches_type(BetaPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.with_raw_response.update(
                plugin_id="",
                served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.list()
        assert_matches_type(SyncPageCursor[BetaPlugin], plugin, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            marketplace_id="marketplace_id",
            organization_id="organization_id",
            owner_type="organization",
            owner_user_id="owner_user_id",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaPlugin], plugin, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = response.parse()
        assert_matches_type(SyncPageCursor[BetaPlugin], plugin, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = response.parse()
            assert_matches_type(SyncPageCursor[BetaPlugin], plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.delete(
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        plugin = client.beta.organization.plugins.delete(
            plugin_id="plugin_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.with_raw_response.delete(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = response.parse()
        assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.with_streaming_response.delete(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = response.parse()
            assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.with_raw_response.delete(
                plugin_id="",
            )


class TestAsyncPlugins:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.create(
            files=[b"Example data"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.create(
            files=[b"Example data"],
            marketplace_id="marketplace_id",
            release_notes="release_notes",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.with_raw_response.create(
            files=[b"Example data"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = await response.parse()
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.with_streaming_response.create(
            files=[b"Example data"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = await response.parse()
            assert_matches_type(BetaPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.retrieve(
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.retrieve(
            plugin_id="plugin_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.with_raw_response.retrieve(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = await response.parse()
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.with_streaming_response.retrieve(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = await response.parse()
            assert_matches_type(BetaPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.with_raw_response.retrieve(
                plugin_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.with_raw_response.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = await response.parse()
        assert_matches_type(BetaPlugin, plugin, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.with_streaming_response.update(
            plugin_id="plugin_id",
            served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = await response.parse()
            assert_matches_type(BetaPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.with_raw_response.update(
                plugin_id="",
                served_version_id="pluginver_01KaZmQpRsTuVwXyZ2b4c6d8",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.list()
        assert_matches_type(AsyncPageCursor[BetaPlugin], plugin, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.list(
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=1,
            marketplace_id="marketplace_id",
            organization_id="organization_id",
            owner_type="organization",
            owner_user_id="owner_user_id",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaPlugin], plugin, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaPlugin], plugin, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaPlugin], plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.delete(
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        plugin = await async_client.beta.organization.plugins.delete(
            plugin_id="plugin_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.with_raw_response.delete(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        plugin = await response.parse()
        assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.with_streaming_response.delete(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            plugin = await response.parse()
            assert_matches_type(BetaDeletedPlugin, plugin, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.with_raw_response.delete(
                plugin_id="",
            )
