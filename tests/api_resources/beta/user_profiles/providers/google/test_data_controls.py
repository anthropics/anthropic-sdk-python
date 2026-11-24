from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta.user_profiles.providers.google import (
    BetaGoogleManagedDataControls,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDataControls:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        data_control = client.beta.user_profiles.providers.google.data_controls.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        data_control = client.beta.user_profiles.providers.google.data_controls.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            betas=["computer-use-2024-10-22"],
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.providers.google.data_controls.with_raw_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_control = response.parse()
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.user_profiles.providers.google.data_controls.with_streaming_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_control = response.parse()
            assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.beta.user_profiles.providers.google.data_controls.with_raw_response.retrieve(
                user_profile_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        data_control = client.beta.user_profiles.providers.google.data_controls.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        data_control = client.beta.user_profiles.providers.google.data_controls.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            cmek={
                "type": "enabled",
                "external_key_ids": {"us": "ekey_01SDCCSbTxrXDpWc1phhtcfK"},
            },
            storage={"type": "disabled"},
            betas=["computer-use-2024-10-22"],
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.user_profiles.providers.google.data_controls.with_raw_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_control = response.parse()
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.user_profiles.providers.google.data_controls.with_streaming_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_control = response.parse()
            assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            client.beta.user_profiles.providers.google.data_controls.with_raw_response.update(
                user_profile_id="",
            )


class TestAsyncDataControls:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        data_control = await async_client.beta.user_profiles.providers.google.data_controls.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        data_control = await async_client.beta.user_profiles.providers.google.data_controls.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            betas=["computer-use-2024-10-22"],
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.providers.google.data_controls.with_raw_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_control = await response.parse()
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.providers.google.data_controls.with_streaming_response.retrieve(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_control = await response.parse()
            assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.beta.user_profiles.providers.google.data_controls.with_raw_response.retrieve(
                user_profile_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        data_control = await async_client.beta.user_profiles.providers.google.data_controls.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        data_control = await async_client.beta.user_profiles.providers.google.data_controls.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            cmek={
                "type": "enabled",
                "external_key_ids": {"us": "ekey_01SDCCSbTxrXDpWc1phhtcfK"},
            },
            storage={"type": "disabled"},
            betas=["computer-use-2024-10-22"],
            workspace_id="wrkspc_011CZkZaBF1tNoB5wlCeusgy",
            extra_query={"beta": "true"},
        )
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.user_profiles.providers.google.data_controls.with_raw_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_control = await response.parse()
        assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.user_profiles.providers.google.data_controls.with_streaming_response.update(
            user_profile_id="uprof_011CZkZCu8hGbp5mYRQgUmz9",
            extra_query={"beta": "true"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_control = await response.parse()
            assert_matches_type(BetaGoogleManagedDataControls, data_control, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_profile_id` but received ''"):
            await async_client.beta.user_profiles.providers.google.data_controls.with_raw_response.update(
                user_profile_id="",
            )
