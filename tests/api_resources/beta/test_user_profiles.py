# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaUserProfile,
    BetaUserProfileEnrollmentURL,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUserProfiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.create()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.create(
            external_id="user_12345",
            metadata={},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.user_profiles.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(BetaUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.with_raw_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.user_profiles.with_streaming_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(BetaUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.beta.user_profiles.with_raw_response.retrieve(
                user_profile_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            external_id="user_12345",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.with_raw_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.user_profiles.with_streaming_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(BetaUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.beta.user_profiles.with_raw_response.update(
                user_profile_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.list()
        assert_matches_type(SyncPageCursor[BetaUserProfile], user_profile, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.list(
            limit=0,
            order="asc",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaUserProfile], user_profile, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(SyncPageCursor[BetaUserProfile], user_profile, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.user_profiles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(SyncPageCursor[BetaUserProfile], user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_enrollment_url(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

    @parametrize
    def test_method_create_enrollment_url_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.beta.user_profiles.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

    @parametrize
    def test_raw_response_create_enrollment_url(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.with_raw_response.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_create_enrollment_url(self, client: Anthropic) -> None:
        with client.beta.user_profiles.with_streaming_response.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create_enrollment_url(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.beta.user_profiles.with_raw_response.create_enrollment_url(
                user_profile_id="",
            )


class TestAsyncUserProfiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.create()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.create(
            external_id="user_12345",
            metadata={},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(BetaUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.with_raw_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.with_streaming_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(BetaUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.beta.user_profiles.with_raw_response.retrieve(
                user_profile_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            external_id="user_12345",
            metadata={"foo": "string"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.with_raw_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.with_streaming_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(BetaUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.beta.user_profiles.with_raw_response.update(
                user_profile_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.list()
        assert_matches_type(AsyncPageCursor[BetaUserProfile], user_profile, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.list(
            limit=0,
            order="asc",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaUserProfile], user_profile, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(AsyncPageCursor[BetaUserProfile], user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaUserProfile], user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_enrollment_url(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

    @parametrize
    async def test_method_create_enrollment_url_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.beta.user_profiles.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_create_enrollment_url(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.with_raw_response.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_create_enrollment_url(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.with_streaming_response.create_enrollment_url(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(BetaUserProfileEnrollmentURL, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create_enrollment_url(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.beta.user_profiles.with_raw_response.create_enrollment_url(
                user_profile_id="",
            )
