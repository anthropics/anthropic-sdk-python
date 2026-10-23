from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta.user_profiles import (
    BetaUserProfileActionURL,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestActionURLs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        action_url = client.beta.user_profiles.action_urls.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        action_url = client.beta.user_profiles.action_urls.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            betas=["message-batches-2024-09-24"],
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.action_urls.with_raw_response.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action_url = response.parse()
        assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.user_profiles.action_urls.with_streaming_response.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action_url = response.parse()
            assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.beta.user_profiles.action_urls.with_raw_response.create(
                user_profile_id="",
                action={"type": "enroll_end_user"},
            )


class TestAsyncActionURLs:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        action_url = await async_client.beta.user_profiles.action_urls.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        action_url = await async_client.beta.user_profiles.action_urls.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            betas=["message-batches-2024-09-24"],
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.action_urls.with_raw_response.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action_url = await response.parse()
        assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.action_urls.with_streaming_response.create(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            action={"type": "enroll_end_user"},
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action_url = await response.parse()
            assert_matches_type(BetaUserProfileActionURL, action_url, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.beta.user_profiles.action_urls.with_raw_response.create(
                user_profile_id="",
                action={"type": "enroll_end_user"},
            )
