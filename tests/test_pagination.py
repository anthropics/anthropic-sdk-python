"""Comprehensive tests for pagination functionality."""

from __future__ import annotations

import os
from typing import List, Optional

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic.pagination import SyncPage, AsyncPage
from anthropic.types import Model

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSyncPage:
    """Test SyncPage pagination functionality."""

    client = Anthropic(base_url=base_url, api_key="test-api-key")

    @pytest.mark.respx(base_url=base_url)
    def test_iteration_over_page_items(self, respx_mock: MockRouter) -> None:
        """Test iterating over items in a page."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        },
                        {
                            "id": "claude-3-sonnet-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Sonnet",
                            "created_at": "2024-02-29T00:00:00Z",
                        },
                    ],
                    "has_more": False,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-sonnet-20240229",
                },
            )
        )

        page = self.client.models.list()
        items = list(page)

        assert len(items) == 2
        assert items[0].id == "claude-3-opus-20240229"
        assert items[1].id == "claude-3-sonnet-20240229"

    @pytest.mark.respx(base_url=base_url)
    def test_has_next_page_true(self, respx_mock: MockRouter) -> None:
        """Test has_next_page returns True when more pages exist."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-opus-20240229",
                },
            )
        )

        page = self.client.models.list()
        assert page.has_next_page() is True

    @pytest.mark.respx(base_url=base_url)
    def test_has_next_page_false_with_has_more_false(self, respx_mock: MockRouter) -> None:
        """Test has_next_page returns False when has_more is False."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": False,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-opus-20240229",
                },
            )
        )

        page = self.client.models.list()
        assert page.has_next_page() is False

    @pytest.mark.respx(base_url=base_url)
    def test_has_next_page_false_with_empty_data(self, respx_mock: MockRouter) -> None:
        """Test has_next_page returns False when data is empty."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [],
                    "has_more": False,
                    "first_id": None,
                    "last_id": None,
                },
            )
        )

        page = self.client.models.list()
        assert page.has_next_page() is False

    @pytest.mark.respx(base_url=base_url)
    def test_next_page_info_with_after_id(self, respx_mock: MockRouter) -> None:
        """Test next_page_info returns correct params for forward pagination."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-opus-20240229",
                },
            )
        )

        page = self.client.models.list()
        next_info = page.next_page_info()

        assert next_info is not None
        assert next_info.params.get("after_id") == "claude-3-opus-20240229"

    @pytest.mark.respx(base_url=base_url)
    def test_next_page_info_with_before_id(self, respx_mock: MockRouter) -> None:
        """Test next_page_info returns correct params for backward pagination."""
        # First request with before_id
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-sonnet-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Sonnet",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "claude-3-sonnet-20240229",
                    "last_id": "claude-3-sonnet-20240229",
                },
            )
        )

        page = self.client.models.list(before_id="some-id")
        next_info = page.next_page_info()

        assert next_info is not None
        assert next_info.params.get("before_id") == "claude-3-sonnet-20240229"

    @pytest.mark.respx(base_url=base_url)
    def test_next_page_info_returns_none_without_last_id(self, respx_mock: MockRouter) -> None:
        """Test next_page_info returns None when last_id is missing."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": None,
                },
            )
        )

        page = self.client.models.list()
        next_info = page.next_page_info()

        assert next_info is None

    @pytest.mark.respx(base_url=base_url)
    def test_next_page_info_returns_none_without_first_id_for_before(
        self, respx_mock: MockRouter
    ) -> None:
        """Test next_page_info returns None when first_id is missing for backward pagination."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": None,
                    "last_id": "claude-3-opus-20240229",
                },
            )
        )

        page = self.client.models.list(before_id="some-id")
        next_info = page.next_page_info()

        assert next_info is None

    @pytest.mark.respx(base_url=base_url)
    def test_get_next_page(self, respx_mock: MockRouter) -> None:
        """Test fetching the next page."""
        # First page
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "model-1",
                            "type": "model",
                            "display_name": "Model 1",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "model-1",
                    "last_id": "model-1",
                },
            )
        )

        # Second page
        respx_mock.get("/v1/models", params={"after_id": "model-1"}).mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "model-2",
                            "type": "model",
                            "display_name": "Model 2",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": False,
                    "first_id": "model-2",
                    "last_id": "model-2",
                },
            )
        )

        page1 = self.client.models.list()
        assert page1.has_next_page() is True

        page2 = page1.get_next_page()
        items = list(page2)
        assert len(items) == 1
        assert items[0].id == "model-2"
        assert page2.has_next_page() is False


class TestAsyncPage:
    """Test AsyncPage pagination functionality."""

    client = AsyncAnthropic(base_url=base_url, api_key="test-api-key")

    @pytest.mark.respx(base_url=base_url)
    async def test_async_iteration_over_page_items(self, respx_mock: MockRouter) -> None:
        """Test async iteration over items in a page."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        },
                        {
                            "id": "claude-3-sonnet-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Sonnet",
                            "created_at": "2024-02-29T00:00:00Z",
                        },
                    ],
                    "has_more": False,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-sonnet-20240229",
                },
            )
        )

        page = await self.client.models.list()
        items = []
        async for item in page:
            items.append(item)

        assert len(items) == 2
        assert items[0].id == "claude-3-opus-20240229"
        assert items[1].id == "claude-3-sonnet-20240229"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_has_next_page_true(self, respx_mock: MockRouter) -> None:
        """Test has_next_page returns True for async pages when more pages exist."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-opus-20240229",
                },
            )
        )

        page = await self.client.models.list()
        assert page.has_next_page() is True

    @pytest.mark.respx(base_url=base_url)
    async def test_async_has_next_page_false(self, respx_mock: MockRouter) -> None:
        """Test has_next_page returns False for async pages when no more pages exist."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "claude-3-opus-20240229",
                            "type": "model",
                            "display_name": "Claude 3 Opus",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": False,
                    "first_id": "claude-3-opus-20240229",
                    "last_id": "claude-3-opus-20240229",
                },
            )
        )

        page = await self.client.models.list()
        assert page.has_next_page() is False

    @pytest.mark.respx(base_url=base_url)
    async def test_async_get_next_page(self, respx_mock: MockRouter) -> None:
        """Test fetching the next page asynchronously."""
        # First page
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "model-1",
                            "type": "model",
                            "display_name": "Model 1",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": True,
                    "first_id": "model-1",
                    "last_id": "model-1",
                },
            )
        )

        # Second page
        respx_mock.get("/v1/models", params={"after_id": "model-1"}).mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [
                        {
                            "id": "model-2",
                            "type": "model",
                            "display_name": "Model 2",
                            "created_at": "2024-02-29T00:00:00Z",
                        }
                    ],
                    "has_more": False,
                    "first_id": "model-2",
                    "last_id": "model-2",
                },
            )
        )

        page1 = await self.client.models.list()
        assert page1.has_next_page() is True

        page2 = await page1.get_next_page()
        items = []
        async for item in page2:
            items.append(item)

        assert len(items) == 1
        assert items[0].id == "model-2"
        assert page2.has_next_page() is False

    @pytest.mark.respx(base_url=base_url)
    async def test_async_empty_page(self, respx_mock: MockRouter) -> None:
        """Test handling of empty pages in async pagination."""
        respx_mock.get("/v1/models").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": [],
                    "has_more": False,
                    "first_id": None,
                    "last_id": None,
                },
            )
        )

        page = await self.client.models.list()
        items = []
        async for item in page:
            items.append(item)

        assert len(items) == 0
        assert page.has_next_page() is False
