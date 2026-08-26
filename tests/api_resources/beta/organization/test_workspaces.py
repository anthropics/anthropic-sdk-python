# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types.beta.organization import (
    BetaWorkspace,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkspaces:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.create(
            name="x",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.create(
            name="x",
            data_residency={
                "allowed_inference_geos": "unrestricted",
                "default_inference_geo": "global",
                "workspace_geo": "us",
            },
            display_color="#6C5BB9",
            external_key_id="ekey_01SDCCSbTxrXDpWc1phhtcfK",
            tags={
                "env": "prod",
                "team": "platform",
            },
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.retrieve(
            "workspace_id",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.with_raw_response.retrieve(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.with_streaming_response.retrieve(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.update(
            workspace_id="workspace_id",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.update(
            workspace_id="workspace_id",
            data_residency={
                "allowed_inference_geos": "unrestricted",
                "default_inference_geo": "global",
            },
            display_color="#6C5BB9",
            external_key_id="ekey_01SDCCSbTxrXDpWc1phhtcfK",
            name="x",
            tags={
                "env": "prod",
                "team": "platform",
            },
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.with_raw_response.update(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.with_streaming_response.update(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.with_raw_response.update(
                workspace_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.list()
        assert_matches_type(SyncPage[BetaWorkspace], workspace, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.list(
            after_id="after_id",
            before_id="before_id",
            include_archived=True,
            limit=1,
        )
        assert_matches_type(SyncPage[BetaWorkspace], workspace, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(SyncPage[BetaWorkspace], workspace, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(SyncPage[BetaWorkspace], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        workspace = client.beta.organization.workspaces.archive(
            "workspace_id",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.organization.workspaces.with_raw_response.archive(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.organization.workspaces.with_streaming_response.archive(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            client.beta.organization.workspaces.with_raw_response.archive(
                "",
            )


class TestAsyncWorkspaces:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.create(
            name="x",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.create(
            name="x",
            data_residency={
                "allowed_inference_geos": "unrestricted",
                "default_inference_geo": "global",
                "workspace_geo": "us",
            },
            display_color="#6C5BB9",
            external_key_id="ekey_01SDCCSbTxrXDpWc1phhtcfK",
            tags={
                "env": "prod",
                "team": "platform",
            },
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.with_raw_response.create(
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.with_streaming_response.create(
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.retrieve(
            "workspace_id",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.with_raw_response.retrieve(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.with_streaming_response.retrieve(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.update(
            workspace_id="workspace_id",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.update(
            workspace_id="workspace_id",
            data_residency={
                "allowed_inference_geos": "unrestricted",
                "default_inference_geo": "global",
            },
            display_color="#6C5BB9",
            external_key_id="ekey_01SDCCSbTxrXDpWc1phhtcfK",
            name="x",
            tags={
                "env": "prod",
                "team": "platform",
            },
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.with_raw_response.update(
            workspace_id="workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.with_streaming_response.update(
            workspace_id="workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.with_raw_response.update(
                workspace_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.list()
        assert_matches_type(AsyncPage[BetaWorkspace], workspace, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.list(
            after_id="after_id",
            before_id="before_id",
            include_archived=True,
            limit=1,
        )
        assert_matches_type(AsyncPage[BetaWorkspace], workspace, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(AsyncPage[BetaWorkspace], workspace, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(AsyncPage[BetaWorkspace], workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        workspace = await async_client.beta.organization.workspaces.archive(
            "workspace_id",
        )
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.workspaces.with_raw_response.archive(
            "workspace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workspace = await response.parse()
        assert_matches_type(BetaWorkspace, workspace, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.workspaces.with_streaming_response.archive(
            "workspace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workspace = await response.parse()
            assert_matches_type(BetaWorkspace, workspace, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workspace_id` but received ''"):
            await async_client.beta.organization.workspaces.with_raw_response.archive(
                "",
            )
