# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.tunnels import BetaTunnelCertificate

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCertificates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.tunnels.certificates.with_raw_response.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.tunnels.certificates.with_streaming_response.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = response.parse()
            assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.certificates.with_raw_response.create(
                tunnel_id="",
                ca_certificate_pem="ca_certificate_pem",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.tunnels.certificates.with_raw_response.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.tunnels.certificates.with_streaming_response.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = response.parse()
            assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.certificates.with_raw_response.retrieve(
                certificate_id="certificate_id",
                tunnel_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `certificate_id` but received ''"):
            client.beta.tunnels.certificates.with_raw_response.retrieve(
                certificate_id="",
                tunnel_id="tunnel_id",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.list(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(SyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.list(
            tunnel_id="tunnel_id",
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.tunnels.certificates.with_raw_response.list(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(SyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.tunnels.certificates.with_streaming_response.list(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = response.parse()
            assert_matches_type(SyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.certificates.with_raw_response.list(
                tunnel_id="",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        certificate = client.beta.tunnels.certificates.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.tunnels.certificates.with_raw_response.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.tunnels.certificates.with_streaming_response.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = response.parse()
            assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            client.beta.tunnels.certificates.with_raw_response.archive(
                certificate_id="certificate_id",
                tunnel_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `certificate_id` but received ''"):
            client.beta.tunnels.certificates.with_raw_response.archive(
                certificate_id="",
                tunnel_id="tunnel_id",
            )


class TestAsyncCertificates:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.certificates.with_raw_response.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.certificates.with_streaming_response.create(
            tunnel_id="tunnel_id",
            ca_certificate_pem="ca_certificate_pem",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = await response.parse()
            assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.certificates.with_raw_response.create(
                tunnel_id="",
                ca_certificate_pem="ca_certificate_pem",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.certificates.with_raw_response.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.certificates.with_streaming_response.retrieve(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = await response.parse()
            assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.certificates.with_raw_response.retrieve(
                certificate_id="certificate_id",
                tunnel_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `certificate_id` but received ''"):
            await async_client.beta.tunnels.certificates.with_raw_response.retrieve(
                certificate_id="",
                tunnel_id="tunnel_id",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.list(
            tunnel_id="tunnel_id",
        )
        assert_matches_type(AsyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.list(
            tunnel_id="tunnel_id",
            include_archived=True,
            limit=0,
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.certificates.with_raw_response.list(
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(AsyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.certificates.with_streaming_response.list(
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaTunnelCertificate], certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.certificates.with_raw_response.list(
                tunnel_id="",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        certificate = await async_client.beta.tunnels.certificates.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.tunnels.certificates.with_raw_response.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        certificate = response.parse()
        assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.tunnels.certificates.with_streaming_response.archive(
            certificate_id="certificate_id",
            tunnel_id="tunnel_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            certificate = await response.parse()
            assert_matches_type(BetaTunnelCertificate, certificate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tunnel_id` but received ''"):
            await async_client.beta.tunnels.certificates.with_raw_response.archive(
                certificate_id="certificate_id",
                tunnel_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `certificate_id` but received ''"):
            await async_client.beta.tunnels.certificates.with_raw_response.archive(
                certificate_id="",
                tunnel_id="tunnel_id",
            )
