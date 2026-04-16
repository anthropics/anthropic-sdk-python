# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types.beta import (
    SkillListResponse,
    SkillCreateResponse,
    SkillDeleteResponse,
    SkillRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSkills:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        skill = client.beta.skills.create()
        assert_matches_type(SkillCreateResponse, skill, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        skill = client.beta.skills.create(
            display_title="display_title",
            files=[b"Example data"],
            betas=["string"],
        )
        assert_matches_type(SkillCreateResponse, skill, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.skills.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SkillCreateResponse, skill, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.skills.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = response.parse()
            assert_matches_type(SkillCreateResponse, skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        skill = client.beta.skills.retrieve(
            skill_id="skill_id",
        )
        assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        skill = client.beta.skills.retrieve(
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.skills.with_raw_response.retrieve(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.skills.with_streaming_response.retrieve(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = response.parse()
            assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.beta.skills.with_raw_response.retrieve(
                skill_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        skill = client.beta.skills.list()
        assert_matches_type(SyncPage[SkillListResponse], skill, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        skill = client.beta.skills.list(
            limit=0,
            after_id="after_id",
            before_id="before_id",
            source="source",
            betas=["string"],
        )
        assert_matches_type(SyncPage[SkillListResponse], skill, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.skills.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SyncPage[SkillListResponse], skill, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.skills.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = response.parse()
            assert_matches_type(SyncPage[SkillListResponse], skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        skill = client.beta.skills.delete(
            skill_id="skill_id",
        )
        assert_matches_type(SkillDeleteResponse, skill, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        skill = client.beta.skills.delete(
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(SkillDeleteResponse, skill, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.skills.with_raw_response.delete(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SkillDeleteResponse, skill, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.skills.with_streaming_response.delete(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = response.parse()
            assert_matches_type(SkillDeleteResponse, skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            client.beta.skills.with_raw_response.delete(
                skill_id="",
            )


class TestAsyncSkills:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.create()
        assert_matches_type(SkillCreateResponse, skill, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.create(
            display_title="display_title",
            files=[b"Example data"],
            betas=["string"],
        )
        assert_matches_type(SkillCreateResponse, skill, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SkillCreateResponse, skill, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = await response.parse()
            assert_matches_type(SkillCreateResponse, skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.retrieve(
            skill_id="skill_id",
        )
        assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.retrieve(
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.with_raw_response.retrieve(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.with_streaming_response.retrieve(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = await response.parse()
            assert_matches_type(SkillRetrieveResponse, skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.beta.skills.with_raw_response.retrieve(
                skill_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.list()
        assert_matches_type(AsyncPage[SkillListResponse], skill, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.list(
            limit=0,
            after_id="after_id",
            before_id="before_id",
            source="source",
            betas=["string"],
        )
        assert_matches_type(AsyncPage[SkillListResponse], skill, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(AsyncPage[SkillListResponse], skill, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = await response.parse()
            assert_matches_type(AsyncPage[SkillListResponse], skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.delete(
            skill_id="skill_id",
        )
        assert_matches_type(SkillDeleteResponse, skill, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        skill = await async_client.beta.skills.delete(
            skill_id="skill_id",
            betas=["string"],
        )
        assert_matches_type(SkillDeleteResponse, skill, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.skills.with_raw_response.delete(
            skill_id="skill_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        skill = response.parse()
        assert_matches_type(SkillDeleteResponse, skill, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.skills.with_streaming_response.delete(
            skill_id="skill_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            skill = await response.parse()
            assert_matches_type(SkillDeleteResponse, skill, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `skill_id` but received ''"):
            await async_client.beta.skills.with_raw_response.delete(
                skill_id="",
            )
