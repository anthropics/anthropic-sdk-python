from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.organization import (
    BetaTelemetryDestination,
    BetaDeletedTelemetryDestination,
    BetaTelemetryDestinationTestResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTelemetryDestinations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.create(
            endpoint_url="x",
            workspaces={"type": "all"},
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.create(
            endpoint_url="x",
            workspaces={"type": "all"},
            display_name="display_name",
            headers={"foo": "string"},
            traces={
                "content_mode": "metadata_only",
                "enabled": True,
                "endpoint_url": "endpoint_url",
                "max_content_bytes": 0,
            },
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.organization.telemetry_destinations.with_raw_response.create(
            endpoint_url="x",
            workspaces={"type": "all"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = response.parse()
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.organization.telemetry_destinations.with_streaming_response.create(
            endpoint_url="x",
            workspaces={"type": "all"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = response.parse()
            assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.retrieve(
            destination_id="destination_id",
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.retrieve(
            destination_id="destination_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.organization.telemetry_destinations.with_raw_response.retrieve(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = response.parse()
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.organization.telemetry_destinations.with_streaming_response.retrieve(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = response.parse()
            assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            client.beta.organization.telemetry_destinations.with_raw_response.retrieve(
                destination_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.update(
            destination_id="destination_id",
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.update(
            destination_id="destination_id",
            display_name="display_name",
            endpoint_url="endpoint_url",
            headers={"foo": "string"},
            state={"type": "enabled"},
            traces={
                "content_mode": "metadata_only",
                "enabled": True,
                "endpoint_url": "endpoint_url",
                "max_content_bytes": 0,
            },
            workspaces={"type": "all"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.organization.telemetry_destinations.with_raw_response.update(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = response.parse()
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.organization.telemetry_destinations.with_streaming_response.update(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = response.parse()
            assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            client.beta.organization.telemetry_destinations.with_raw_response.update(
                destination_id="",
            )

    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.list()
        assert_matches_type(SyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.list(
            limit=0,
            page="page",
            workspace_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.organization.telemetry_destinations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = response.parse()
        assert_matches_type(SyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.organization.telemetry_destinations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = response.parse()
            assert_matches_type(SyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.delete(
            destination_id="destination_id",
        )
        assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.delete(
            destination_id="destination_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.organization.telemetry_destinations.with_raw_response.delete(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = response.parse()
        assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.organization.telemetry_destinations.with_streaming_response.delete(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = response.parse()
            assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            client.beta.organization.telemetry_destinations.with_raw_response.delete(
                destination_id="",
            )

    @parametrize
    def test_method_test(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.test(
            destination_id="destination_id",
        )
        assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

    @parametrize
    def test_method_test_with_all_params(self, client: Anthropic) -> None:
        telemetry_destination = client.beta.organization.telemetry_destinations.test(
            destination_id="destination_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

    @parametrize
    def test_raw_response_test(self, client: Anthropic) -> None:
        response = client.beta.organization.telemetry_destinations.with_raw_response.test(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = response.parse()
        assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

    @parametrize
    def test_streaming_response_test(self, client: Anthropic) -> None:
        with client.beta.organization.telemetry_destinations.with_streaming_response.test(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = response.parse()
            assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_test(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            client.beta.organization.telemetry_destinations.with_raw_response.test(
                destination_id="",
            )


class TestAsyncTelemetryDestinations:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.create(
            endpoint_url="x",
            workspaces={"type": "all"},
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.create(
            endpoint_url="x",
            workspaces={"type": "all"},
            display_name="display_name",
            headers={"foo": "string"},
            traces={
                "content_mode": "metadata_only",
                "enabled": True,
                "endpoint_url": "endpoint_url",
                "max_content_bytes": 0,
            },
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.telemetry_destinations.with_raw_response.create(
            endpoint_url="x",
            workspaces={"type": "all"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = await response.parse()
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.telemetry_destinations.with_streaming_response.create(
            endpoint_url="x",
            workspaces={"type": "all"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = await response.parse()
            assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.retrieve(
            destination_id="destination_id",
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.retrieve(
            destination_id="destination_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.telemetry_destinations.with_raw_response.retrieve(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = await response.parse()
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.telemetry_destinations.with_streaming_response.retrieve(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = await response.parse()
            assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            await async_client.beta.organization.telemetry_destinations.with_raw_response.retrieve(
                destination_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.update(
            destination_id="destination_id",
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.update(
            destination_id="destination_id",
            display_name="display_name",
            endpoint_url="endpoint_url",
            headers={"foo": "string"},
            state={"type": "enabled"},
            traces={
                "content_mode": "metadata_only",
                "enabled": True,
                "endpoint_url": "endpoint_url",
                "max_content_bytes": 0,
            },
            workspaces={"type": "all"},
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.telemetry_destinations.with_raw_response.update(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = await response.parse()
        assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.telemetry_destinations.with_streaming_response.update(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = await response.parse()
            assert_matches_type(BetaTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            await async_client.beta.organization.telemetry_destinations.with_raw_response.update(
                destination_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.list()
        assert_matches_type(AsyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.list(
            limit=0,
            page="page",
            workspace_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.telemetry_destinations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = await response.parse()
        assert_matches_type(AsyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.telemetry_destinations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaTelemetryDestination], telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.delete(
            destination_id="destination_id",
        )
        assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.delete(
            destination_id="destination_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.telemetry_destinations.with_raw_response.delete(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = await response.parse()
        assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.telemetry_destinations.with_streaming_response.delete(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = await response.parse()
            assert_matches_type(BetaDeletedTelemetryDestination, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            await async_client.beta.organization.telemetry_destinations.with_raw_response.delete(
                destination_id="",
            )

    @parametrize
    async def test_method_test(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.test(
            destination_id="destination_id",
        )
        assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

    @parametrize
    async def test_method_test_with_all_params(self, async_client: AsyncAnthropic) -> None:
        telemetry_destination = await async_client.beta.organization.telemetry_destinations.test(
            destination_id="destination_id",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

    @parametrize
    async def test_raw_response_test(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.organization.telemetry_destinations.with_raw_response.test(
            destination_id="destination_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        telemetry_destination = await response.parse()
        assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

    @parametrize
    async def test_streaming_response_test(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.organization.telemetry_destinations.with_streaming_response.test(
            destination_id="destination_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            telemetry_destination = await response.parse()
            assert_matches_type(BetaTelemetryDestinationTestResponse, telemetry_destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_test(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `destination_id` but received ''"):
            await async_client.beta.organization.telemetry_destinations.with_raw_response.test(
                destination_id="",
            )
