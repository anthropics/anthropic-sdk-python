# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.types.beta.organization import (
    BetaComplianceSettings,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestComplianceSettings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        compliance_setting = client.beta.organization.compliance_settings.retrieve()
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.compliance_settings.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compliance_setting = response.parse()
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.compliance_settings.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compliance_setting = response.parse()
            assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        compliance_setting = client.beta.organization.compliance_settings.update(
            state={"type": "enabled"},
        )
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.compliance_settings.with_raw_response.update(
            state={"type": "enabled"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compliance_setting = response.parse()
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.compliance_settings.with_streaming_response.update(
            state={"type": "enabled"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compliance_setting = response.parse()
            assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncComplianceSettings:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        compliance_setting = await async_client.beta.organization.compliance_settings.retrieve()
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.compliance_settings.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compliance_setting = await response.parse()
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.compliance_settings.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compliance_setting = await response.parse()
            assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        compliance_setting = await async_client.beta.organization.compliance_settings.update(
            state={"type": "enabled"},
        )
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.compliance_settings.with_raw_response.update(
            state={"type": "enabled"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        compliance_setting = await response.parse()
        assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.compliance_settings.with_streaming_response.update(
            state={"type": "enabled"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            compliance_setting = await response.parse()
            assert_matches_type(BetaComplianceSettings, compliance_setting, path=["response"])

        assert cast(Any, response.is_closed) is True
