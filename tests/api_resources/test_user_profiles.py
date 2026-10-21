from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types import (
    UserProfile,
    DeletedUserProfile,
)
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUserProfiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.create()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.create(
            access_type="application",
            external_user_details={
                "account_status": "active",
                "country": "US",
                "email_hash": "x",
                "entity_type": "business",
                "name_hash": "x",
                "onboarded_at": parse_datetime("2024-11-02T08:15:00Z"),
                "reference_id": "user_12345",
            },
            metadata={},
            name="Example User",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.user_profiles.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.user_profiles.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(UserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.user_profiles.with_raw_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.user_profiles.with_streaming_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(UserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.user_profiles.with_raw_response.retrieve(
                user_profile_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            access_type="application",
            external_user_details={
                "account_status": "suspended",
                "country": "country",
                "email_hash": "x",
                "entity_type": "individual",
                "name_hash": "x",
                "onboarded_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                "reference_id": "x",
            },
            metadata={"foo": "string"},
            name="x",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.user_profiles.with_raw_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.user_profiles.with_streaming_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(UserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.user_profiles.with_raw_response.update(
                user_profile_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.list()
        assert_matches_type(SyncPageCursor[UserProfile], user_profile, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.list(
            enforcement_status=["unrestricted"],
            limit=0,
            order="asc",
            order_by="created_at",
            page="page",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(SyncPageCursor[UserProfile], user_profile, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.user_profiles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(SyncPageCursor[UserProfile], user_profile, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.user_profiles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(SyncPageCursor[UserProfile], user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        user_profile = client.user_profiles.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.user_profiles.with_raw_response.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = response.parse()
        assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.user_profiles.with_streaming_response.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = response.parse()
            assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.user_profiles.with_raw_response.delete(
                user_profile_id="",
            )


class TestAsyncUserProfiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.create()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.create(
            access_type="application",
            external_user_details={
                "account_status": "active",
                "country": "US",
                "email_hash": "x",
                "entity_type": "business",
                "name_hash": "x",
                "onboarded_at": parse_datetime("2024-11-02T08:15:00Z"),
                "reference_id": "user_12345",
            },
            metadata={},
            name="Example User",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.user_profiles.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = await response.parse()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.user_profiles.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(UserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.user_profiles.with_raw_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = await response.parse()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.user_profiles.with_streaming_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(UserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.user_profiles.with_raw_response.retrieve(
                user_profile_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            access_type="application",
            external_user_details={
                "account_status": "suspended",
                "country": "country",
                "email_hash": "x",
                "entity_type": "individual",
                "name_hash": "x",
                "onboarded_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                "reference_id": "x",
            },
            metadata={"foo": "string"},
            name="x",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.user_profiles.with_raw_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = await response.parse()
        assert_matches_type(UserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.user_profiles.with_streaming_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(UserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.user_profiles.with_raw_response.update(
                user_profile_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.list()
        assert_matches_type(AsyncPageCursor[UserProfile], user_profile, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.list(
            enforcement_status=["unrestricted"],
            limit=0,
            order="asc",
            order_by="created_at",
            page="page",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(AsyncPageCursor[UserProfile], user_profile, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.user_profiles.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = await response.parse()
        assert_matches_type(AsyncPageCursor[UserProfile], user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.user_profiles.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(AsyncPageCursor[UserProfile], user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )
        assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        user_profile = await async_client.user_profiles.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
        )
        assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.user_profiles.with_raw_response.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user_profile = await response.parse()
        assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.user_profiles.with_streaming_response.delete(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user_profile = await response.parse()
            assert_matches_type(DeletedUserProfile, user_profile, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.user_profiles.with_raw_response.delete(
                user_profile_id="",
            )
