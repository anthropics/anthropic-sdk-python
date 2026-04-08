# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta.sessions import (
    ResourceUpdateResponse,
    ResourceRetrieveResponse,
    BetaManagedAgentsFileResource,
    BetaManagedAgentsSessionResource,
    BetaManagedAgentsDeleteSessionResource,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["string"],
        )
        assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.sessions.resources.with_raw_response.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.sessions.resources.with_streaming_response.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = response.parse()
            assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.retrieve(
                resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.retrieve(
                resource_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
        )
        assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
            betas=["string"],
        )
        assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.sessions.resources.with_raw_response.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.sessions.resources.with_streaming_response.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = response.parse()
            assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.update(
                resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
                session_id="",
                authorization_token="ghp_exampletoken",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.update(
                resource_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
                authorization_token="ghp_exampletoken",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            limit=0,
            page="page",
            betas=["string"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.sessions.resources.with_raw_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.sessions.resources.with_streaming_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_path_params_list(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.list(
                session_id="",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["string"],
        )
        assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.sessions.resources.with_raw_response.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.sessions.resources.with_streaming_response.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = response.parse()
            assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.delete(
                resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.delete(
                resource_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_add(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
        )
        assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_method_add_with_all_params(self, client: Anthropic) -> None:
        resource = client.beta.sessions.resources.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
            mount_path="/uploads/receipt.pdf",
            betas=["string"],
        )
        assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_raw_response_add(self, client: Anthropic) -> None:
        response = client.beta.sessions.resources.with_raw_response.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_streaming_response_add(self, client: Anthropic) -> None:
        with client.beta.sessions.resources.with_streaming_response.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = response.parse()
            assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    def test_path_params_add(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.resources.with_raw_response.add(
                session_id="",
                file_id="file_011CNha8iCJcU1wXNR6q4V8w",
                type="file",
            )


class TestAsyncResources:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["string"],
        )
        assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.resources.with_raw_response.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.resources.with_streaming_response.retrieve(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = await response.parse()
            assert_matches_type(ResourceRetrieveResponse, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.retrieve(
                resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.retrieve(
                resource_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
        )
        assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
            betas=["string"],
        )
        assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.resources.with_raw_response.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.resources.with_streaming_response.update(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            authorization_token="ghp_exampletoken",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = await response.parse()
            assert_matches_type(ResourceUpdateResponse, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.update(
                resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
                session_id="",
                authorization_token="ghp_exampletoken",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.update(
                resource_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
                authorization_token="ghp_exampletoken",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            limit=0,
            page="page",
            betas=["string"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.resources.with_raw_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.resources.with_streaming_response.list(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsSessionResource], resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.list(
                session_id="",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["string"],
        )
        assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.resources.with_raw_response.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.resources.with_streaming_response.delete(
            resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = await response.parse()
            assert_matches_type(BetaManagedAgentsDeleteSessionResource, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.delete(
                resource_id="sesrsc_011CZkZBJq5dWxk9fVLNcPht",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `resource_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.delete(
                resource_id="",
                session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            )

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_add(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
        )
        assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncAnthropic) -> None:
        resource = await async_client.beta.sessions.resources.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
            mount_path="/uploads/receipt.pdf",
            betas=["string"],
        )
        assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.resources.with_raw_response.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resource = response.parse()
        assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.resources.with_streaming_response.add(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            file_id="file_011CNha8iCJcU1wXNR6q4V8w",
            type="file",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resource = await response.parse()
            assert_matches_type(BetaManagedAgentsFileResource, resource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prism can't find endpoint with beta only tag")
    @parametrize
    async def test_path_params_add(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.resources.with_raw_response.add(
                session_id="",
                file_id="file_011CNha8iCJcU1wXNR6q4V8w",
                type="file",
            )
