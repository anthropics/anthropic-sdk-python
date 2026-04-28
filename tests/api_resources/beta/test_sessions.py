# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from tests.utils import assert_matches_type
from anthropic._utils import parse_datetime
from anthropic.pagination import SyncPageCursor, AsyncPageCursor
from anthropic.types.beta import (
    BetaManagedAgentsSession,
    BetaManagedAgentsDeletedSession,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Anthropic) -> None:
        session = client.beta.sessions.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Anthropic) -> None:
        session = client.beta.sessions.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
            resources=[
                {
                    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
                    "type": "file",
                    "mount_path": "/uploads/receipt.pdf",
                }
            ],
            title="Order #1234 inquiry",
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Anthropic) -> None:
        response = client.beta.sessions.with_raw_response.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Anthropic) -> None:
        with client.beta.sessions.with_streaming_response.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Anthropic) -> None:
        session = client.beta.sessions.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Anthropic) -> None:
        session = client.beta.sessions.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Anthropic) -> None:
        response = client.beta.sessions.with_raw_response.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Anthropic) -> None:
        with client.beta.sessions.with_streaming_response.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.with_raw_response.retrieve(
                session_id="",
            )

    @parametrize
    def test_method_update(self, client: Anthropic) -> None:
        session = client.beta.sessions.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Anthropic) -> None:
        session = client.beta.sessions.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            metadata={"foo": "string"},
            title="Order #1234 inquiry",
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Anthropic) -> None:
        response = client.beta.sessions.with_raw_response.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Anthropic) -> None:
        with client.beta.sessions.with_streaming_response.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.with_raw_response.update(
                session_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list(self, client: Anthropic) -> None:
        session = client.beta.sessions.list()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_method_list_with_all_params(self, client: Anthropic) -> None:
        session = client.beta.sessions.list(
            agent_id="agent_id",
            agent_version=0,
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            memory_store_id="memory_store_id",
            order="asc",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_raw_response_list(self, client: Anthropic) -> None:
        response = client.beta.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    def test_streaming_response_list(self, client: Anthropic) -> None:
        with client.beta.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Anthropic) -> None:
        session = client.beta.sessions.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Anthropic) -> None:
        session = client.beta.sessions.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Anthropic) -> None:
        response = client.beta.sessions.with_raw_response.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Anthropic) -> None:
        with client.beta.sessions.with_streaming_response.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.with_raw_response.delete(
                session_id="",
            )

    @parametrize
    def test_method_archive(self, client: Anthropic) -> None:
        session = client.beta.sessions.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_method_archive_with_all_params(self, client: Anthropic) -> None:
        session = client.beta.sessions.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: Anthropic) -> None:
        response = client.beta.sessions.with_raw_response.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: Anthropic) -> None:
        with client.beta.sessions.with_streaming_response.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: Anthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.beta.sessions.with_raw_response.archive(
                session_id="",
            )


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
            metadata={"foo": "string"},
            resources=[
                {
                    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w",
                    "type": "file",
                    "mount_path": "/uploads/receipt.pdf",
                }
            ],
            title="Order #1234 inquiry",
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.with_raw_response.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.with_streaming_response.create(
            agent="agent_011CZkYpogX7uDKUyvBTophP",
            environment_id="env_011CZkZ9X2dpNyB7HsEFoRfW",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.with_raw_response.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.with_streaming_response.retrieve(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.with_raw_response.retrieve(
                session_id="",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            metadata={"foo": "string"},
            title="Order #1234 inquiry",
            vault_ids=["string"],
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.with_raw_response.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.with_streaming_response.update(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.with_raw_response.update(
                session_id="",
            )

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.list()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.list(
            agent_id="agent_id",
            agent_version=0,
            created_at_gt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_gte=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lt=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_at_lte=parse_datetime("2019-12-27T18:11:19.117Z"),
            include_archived=True,
            limit=0,
            memory_store_id="memory_store_id",
            order="asc",
            page="page",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(AsyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

    @pytest.mark.skip(reason="buildURL drops path-level query params (SDK-4349)")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(AsyncPageCursor[BetaManagedAgentsSession], session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.with_raw_response.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.with_streaming_response.delete(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(BetaManagedAgentsDeletedSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.with_raw_response.delete(
                session_id="",
            )

    @parametrize
    async def test_method_archive(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_method_archive_with_all_params(self, async_client: AsyncAnthropic) -> None:
        session = await async_client.beta.sessions.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
            betas=["message-batches-2024-09-24"],
        )
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncAnthropic) -> None:
        response = await async_client.beta.sessions.with_raw_response.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncAnthropic) -> None:
        async with async_client.beta.sessions.with_streaming_response.archive(
            session_id="sesn_011CZkZAtmR3yMPDzynEDxu7",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(BetaManagedAgentsSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncAnthropic) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.beta.sessions.with_raw_response.archive(
                session_id="",
            )
