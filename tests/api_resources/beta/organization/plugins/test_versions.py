from __future__ import annotations

import os
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization.plugins import (
    BetaPluginVersion,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        version = client.beta.organization.plugins.versions.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.organization.plugins.versions.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
            release_notes="release_notes",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.versions.with_raw_response.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.versions.with_streaming_response.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(BetaPluginVersion, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.versions.with_raw_response.create(
                plugin_id="",
                files=[b"Example data"],
            )

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        version = client.beta.organization.plugins.versions.retrieve(
            version="version",
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.organization.plugins.versions.retrieve(
            version="version",
            plugin_id="plugin_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.versions.with_raw_response.retrieve(
            version="version",
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.versions.with_streaming_response.retrieve(
            version="version",
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(BetaPluginVersion, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.versions.with_raw_response.retrieve(
                version="version",
                plugin_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            client.beta.organization.plugins.versions.with_raw_response.retrieve(
                version="",
                plugin_id="plugin_id",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        version = client.beta.organization.plugins.versions.list(
            plugin_id="plugin_id",
        )
        assert_matches_type(SyncPageCursor[BetaPluginVersion], version, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.organization.plugins.versions.list(
            plugin_id="plugin_id",
            limit=1,
            organization_id="organization_id",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaPluginVersion], version, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.plugins.versions.with_raw_response.list(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(SyncPageCursor[BetaPluginVersion], version, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.plugins.versions.with_streaming_response.list(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(SyncPageCursor[BetaPluginVersion], version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.versions.with_raw_response.list(
                plugin_id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))
        version = client.beta.organization.plugins.versions.download(
            version="version",
            plugin_id="plugin_id",
        )
        assert version.is_closed
        assert version.json() == {"foo": "bar"}
        assert cast(Any, version.is_closed) is True
        assert isinstance(version, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download_with_all_params(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))
        version = client.beta.organization.plugins.versions.download(
            version="version",
            plugin_id="plugin_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert version.is_closed
        assert version.json() == {"foo": "bar"}
        assert cast(Any, version.is_closed) is True
        assert isinstance(version, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))

        version = client.beta.organization.plugins.versions.with_raw_response.download(
            version="version",
            plugin_id="plugin_id",
        )

        assert version.is_closed is True
        assert version.http_request.headers.get("X-Stainless-Lang") == "python"
        assert version.json() == {"foo": "bar"}
        assert isinstance(version, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download(self, client: Anthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))
        with client.beta.organization.plugins.versions.with_streaming_response.download(
            version="version",
            plugin_id="plugin_id",
        ) as version:
            assert not version.is_closed
            assert version.http_request.headers.get("X-Stainless-Lang") == "python"

            assert version.json() == {"foo": "bar"}
            assert cast(Any, version.is_closed) is True
            assert isinstance(version, StreamedBinaryAPIResponse)

        assert cast(Any, version.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            client.beta.organization.plugins.versions.with_raw_response.download(
                version="version",
                plugin_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            client.beta.organization.plugins.versions.with_raw_response.download(
                version="",
                plugin_id="plugin_id",
            )


class TestAsyncVersions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.organization.plugins.versions.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.organization.plugins.versions.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
            release_notes="release_notes",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.versions.with_raw_response.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.versions.with_streaming_response.create(
            plugin_id="plugin_id",
            files=[b"Example data"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(BetaPluginVersion, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.versions.with_raw_response.create(
                plugin_id="",
                files=[b"Example data"],
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.organization.plugins.versions.retrieve(
            version="version",
            plugin_id="plugin_id",
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.organization.plugins.versions.retrieve(
            version="version",
            plugin_id="plugin_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.versions.with_raw_response.retrieve(
            version="version",
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert_matches_type(BetaPluginVersion, version, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.versions.with_streaming_response.retrieve(
            version="version",
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(BetaPluginVersion, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.versions.with_raw_response.retrieve(
                version="version",
                plugin_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            await async_client.beta.organization.plugins.versions.with_raw_response.retrieve(
                version="",
                plugin_id="plugin_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.organization.plugins.versions.list(
            plugin_id="plugin_id",
        )
        assert_matches_type(AsyncPageCursor[BetaPluginVersion], version, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.organization.plugins.versions.list(
            plugin_id="plugin_id",
            limit=1,
            organization_id="organization_id",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaPluginVersion], version, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.plugins.versions.with_raw_response.list(
            plugin_id="plugin_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaPluginVersion], version, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.plugins.versions.with_streaming_response.list(
            plugin_id="plugin_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaPluginVersion], version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.versions.with_raw_response.list(
                plugin_id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))
        version = await async_client.beta.organization.plugins.versions.download(
            version="version",
            plugin_id="plugin_id",
        )
        assert version.is_closed
        assert await version.json() == {"foo": "bar"}
        assert cast(Any, version.is_closed) is True
        assert isinstance(version, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download_with_all_params(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))
        version = await async_client.beta.organization.plugins.versions.download(
            version="version",
            plugin_id="plugin_id",
            organization_id="organization_id",
            betas=["message-batches-2024-09-24"],
        )
        assert version.is_closed
        assert await version.json() == {"foo": "bar"}
        assert cast(Any, version.is_closed) is True
        assert isinstance(version, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))

        version = await async_client.beta.organization.plugins.versions.with_raw_response.download(
            version="version",
            plugin_id="plugin_id",
        )

        assert version.is_closed is True
        assert version.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await version.json() == {"foo": "bar"}
        assert isinstance(version, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        respx_mock.get(
            "/v1/organizations/plugins/plugin_id/versions/version/content", params__contains={"beta": "true"}
        ).mock(return_value=httpx2.Response(200, json={"foo": "bar"}))
        async with async_client.beta.organization.plugins.versions.with_streaming_response.download(
            version="version",
            plugin_id="plugin_id",
        ) as version:
            assert not version.is_closed
            assert version.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await version.json() == {"foo": "bar"}
            assert cast(Any, version.is_closed) is True
            assert isinstance(version, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, version.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `plugin_id` but received ''"):
            await async_client.beta.organization.plugins.versions.with_raw_response.download(
                version="version",
                plugin_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            await async_client.beta.organization.plugins.versions.with_raw_response.download(
                version="",
                plugin_id="plugin_id",
            )
