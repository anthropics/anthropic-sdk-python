# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.skills import (
    VersionListResponse,
    VersionCreateResponse,
    VersionDeleteResponse,
    VersionRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.create(
            skill_id="skill_id",
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.create(
            skill_id="skill_id",
            files=[b"raw file contents"],
            betas=["string"],
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.skills.versions.with_raw_response.create(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.skills.versions.with_streaming_response.create(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(VersionCreateResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.beta.skills.versions.with_raw_response.create(
                skill_id="",
            )

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.retrieve(
            version="version",
            skill_id="skill_id",
        )
        assert_matches_type(VersionRetrieveResponse, version, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.retrieve(
            version="version",
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(VersionRetrieveResponse, version, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.skills.versions.with_raw_response.retrieve(
            version="version",
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionRetrieveResponse, version, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.skills.versions.with_streaming_response.retrieve(
            version="version",
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(VersionRetrieveResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.beta.skills.versions.with_raw_response.retrieve(
                version="version",
                skill_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            client.beta.skills.versions.with_raw_response.retrieve(
                version="",
                skill_id="skill_id",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.list(
            skill_id="skill_id",
        )
        assert_matches_type(SyncPageCursor[VersionListResponse], version, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.list(
            skill_id="skill_id",
            limit=0,
            page="page",
            betas=["string"],
        )
        assert_matches_type(SyncPageCursor[VersionListResponse], version, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.skills.versions.with_raw_response.list(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(SyncPageCursor[VersionListResponse], version, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.skills.versions.with_streaming_response.list(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(SyncPageCursor[VersionListResponse], version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.beta.skills.versions.with_raw_response.list(
                skill_id="",
            )

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.delete(
            version="version",
            skill_id="skill_id",
        )
        assert_matches_type(VersionDeleteResponse, version, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        version = client.beta.skills.versions.delete(
            version="version",
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(VersionDeleteResponse, version, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.skills.versions.with_raw_response.delete(
            version="version",
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionDeleteResponse, version, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.skills.versions.with_streaming_response.delete(
            version="version",
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(VersionDeleteResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.beta.skills.versions.with_raw_response.delete(
                version="version",
                skill_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            client.beta.skills.versions.with_raw_response.delete(
                version="",
                skill_id="skill_id",
            )


class TestAsyncVersions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.create(
            skill_id="skill_id",
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.create(
            skill_id="skill_id",
            files=[b"raw file contents"],
            betas=["string"],
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.versions.with_raw_response.create(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.versions.with_streaming_response.create(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(VersionCreateResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism binary unsupported")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.beta.skills.versions.with_raw_response.create(
                skill_id="",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.retrieve(
            version="version",
            skill_id="skill_id",
        )
        assert_matches_type(VersionRetrieveResponse, version, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.retrieve(
            version="version",
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(VersionRetrieveResponse, version, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.versions.with_raw_response.retrieve(
            version="version",
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionRetrieveResponse, version, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.versions.with_streaming_response.retrieve(
            version="version",
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(VersionRetrieveResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.beta.skills.versions.with_raw_response.retrieve(
                version="version",
                skill_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            await async_client.beta.skills.versions.with_raw_response.retrieve(
                version="",
                skill_id="skill_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.list(
            skill_id="skill_id",
        )
        assert_matches_type(AsyncPageCursor[VersionListResponse], version, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.list(
            skill_id="skill_id",
            limit=0,
            page="page",
            betas=["string"],
        )
        assert_matches_type(AsyncPageCursor[VersionListResponse], version, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.versions.with_raw_response.list(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(AsyncPageCursor[VersionListResponse], version, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.versions.with_streaming_response.list(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(AsyncPageCursor[VersionListResponse], version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.beta.skills.versions.with_raw_response.list(
                skill_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.delete(
            version="version",
            skill_id="skill_id",
        )
        assert_matches_type(VersionDeleteResponse, version, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        version = await async_client.beta.skills.versions.delete(
            version="version",
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(VersionDeleteResponse, version, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.versions.with_raw_response.delete(
            version="version",
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionDeleteResponse, version, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.versions.with_streaming_response.delete(
            version="version",
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(VersionDeleteResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.beta.skills.versions.with_raw_response.delete(
                version="version",
                skill_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version` but received ''"):
            await async_client.beta.skills.versions.with_raw_response.delete(
                version="",
                skill_id="skill_id",
            )
