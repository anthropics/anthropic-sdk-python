from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.plugins import (
    BetaPluginInstallationSetting,
    BetaDeletedPluginInstallationSetting,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInstallationSettings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        installation_setting = client.beta.organization.plugins.installation_settings.list(
            plugin_id="plugin_id",
        )
        assert_matches_type(SyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        installation_setting = client.beta.organization.plugins.installation_settings.list(
            plugin_id="plugin_id",
            limit=1,
            organization_id="organization_id",
            page="page",
            target_type="organization",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.installation_settings.with_raw_response.list(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        installation_setting = response.parse()
        assert_matches_type(SyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.installation_settings.with_streaming_response.list(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            installation_setting = response.parse()
            assert_matches_type(SyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.installation_settings.with_raw_response.list(
                plugin_id="",
            )

    @parametrize
    def test_method_remove(self, client: Anthropic) -> None:
        installation_setting = client.beta.organization.plugins.installation_settings.remove(
            target="target",
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    def test_method_remove_with_all_params(self, client: Anthropic) -> None:
        installation_setting = client.beta.organization.plugins.installation_settings.remove(
            target="target",
            plugin_id="plugin_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    def test_raw_response_remove(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.installation_settings.with_raw_response.remove(
            target="target",
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        installation_setting = response.parse()
        assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    def test_streaming_response_remove(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.installation_settings.with_streaming_response.remove(
            target="target",
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            installation_setting = response.parse()
            assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.installation_settings.with_raw_response.remove(
                target="target",
                plugin_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target` but received ''"):
            client.beta.organization.plugins.installation_settings.with_raw_response.remove(
                target="",
                plugin_id="plugin_id",
            )

    @parametrize
    def test_method_set(self, client: Anthropic) -> None:
        installation_setting = client.beta.organization.plugins.installation_settings.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
        )
        assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    def test_method_set_with_all_params(self, client: Anthropic) -> None:
        installation_setting = client.beta.organization.plugins.installation_settings.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    def test_raw_response_set(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.installation_settings.with_raw_response.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        installation_setting = response.parse()
        assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    def test_streaming_response_set(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.installation_settings.with_streaming_response.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            installation_setting = response.parse()
            assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_set(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.installation_settings.with_raw_response.set(
                target="target",
                plugin_id="",
                installation_preference="required",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target` but received ''"):
            client.beta.organization.plugins.installation_settings.with_raw_response.set(
                target="",
                plugin_id="plugin_id",
                installation_preference="required",
            )


class TestAsyncInstallationSettings:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        installation_setting = await async_client.beta.organization.plugins.installation_settings.list(
            plugin_id="plugin_id",
        )
        assert_matches_type(AsyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        installation_setting = await async_client.beta.organization.plugins.installation_settings.list(
            plugin_id="plugin_id",
            limit=1,
            organization_id="organization_id",
            page="page",
            target_type="organization",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.installation_settings.with_raw_response.list(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        installation_setting = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.installation_settings.with_streaming_response.list(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            installation_setting = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaPluginInstallationSetting], installation_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.installation_settings.with_raw_response.list(
                plugin_id="",
            )

    @parametrize
    async def test_method_remove(self, async_client: AsyncAnthropic) -> None:
        installation_setting = await async_client.beta.organization.plugins.installation_settings.remove(
            target="target",
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    async def test_method_remove_with_all_params(self, async_client: AsyncAnthropic) -> None:
        installation_setting = await async_client.beta.organization.plugins.installation_settings.remove(
            target="target",
            plugin_id="plugin_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.installation_settings.with_raw_response.remove(
            target="target",
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        installation_setting = await response.parse()
        assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.installation_settings.with_streaming_response.remove(
            target="target",
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            installation_setting = await response.parse()
            assert_matches_type(BetaDeletedPluginInstallationSetting, installation_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.installation_settings.with_raw_response.remove(
                target="target",
                plugin_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target` but received ''"):
            await async_client.beta.organization.plugins.installation_settings.with_raw_response.remove(
                target="",
                plugin_id="plugin_id",
            )

    @parametrize
    async def test_method_set(self, async_client: AsyncAnthropic) -> None:
        installation_setting = await async_client.beta.organization.plugins.installation_settings.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
        )
        assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    async def test_method_set_with_all_params(self, async_client: AsyncAnthropic) -> None:
        installation_setting = await async_client.beta.organization.plugins.installation_settings.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    async def test_raw_response_set(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.installation_settings.with_raw_response.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        installation_setting = await response.parse()
        assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

    @parametrize
    async def test_streaming_response_set(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.installation_settings.with_streaming_response.set(
            target="target",
            plugin_id="plugin_id",
            installation_preference="required",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            installation_setting = await response.parse()
            assert_matches_type(BetaPluginInstallationSetting, installation_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_set(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.installation_settings.with_raw_response.set(
                target="target",
                plugin_id="",
                installation_preference="required",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `target` but received ''"):
            await async_client.beta.organization.plugins.installation_settings.with_raw_response.set(
                target="",
                plugin_id="plugin_id",
                installation_preference="required",
            )
