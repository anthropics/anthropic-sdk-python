from __future__ import annotations

import os
from typing import cast
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

from anthropic import AnthropicVertex, AsyncAnthropicVertex

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class MockRequestCall(Protocol):
    request: httpx.Request


class TestAnthropicVertex:
    client = AnthropicVertex(region="region", project_id="project", access_token="my-access-token")

    @pytest.mark.respx()
    def test_messages_retries(self, respx_mock: MockRouter) -> None:
        request_url = "https://region-aiplatform.googleapis.com/v1/projects/project/locations/region/publishers/anthropic/models/claude-3-sonnet@20240229:rawPredict"
        respx_mock.post(request_url).mock(
            side_effect=[
                httpx.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
                httpx.Response(200, json={"foo": "bar"}),
            ]
        )

        self.client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-sonnet@20240229",
        )

        calls = cast("list[MockRequestCall]", respx_mock.calls)

        assert len(calls) == 2

        assert calls[0].request.url == request_url
        assert calls[1].request.url == request_url

    def test_copy(self) -> None:
        copied = self.client.copy()
        assert id(copied) != id(self.client)

        copied = self.client.copy(region="another-region", project_id="another-project")
        assert copied.region == "another-region"
        assert self.client.region == "region"
        assert copied.project_id == "another-project"
        assert self.client.project_id == "project"

    def test_with_options(self) -> None:
        copied = self.client.with_options(region="another-region", project_id="another-project")
        assert copied.region == "another-region"
        assert self.client.region == "region"
        assert copied.project_id == "another-project"
        assert self.client.project_id == "project"

    def test_copy_default_options(self) -> None:
        # options that have a default are overridden correctly
        copied = self.client.copy(max_retries=7)
        assert copied.max_retries == 7
        assert self.client.max_retries == 2

        copied2 = copied.copy(max_retries=6)
        assert copied2.max_retries == 6
        assert copied.max_retries == 7

        # timeout
        assert isinstance(self.client.timeout, httpx.Timeout)
        copied = self.client.copy(timeout=None)
        assert copied.timeout is None
        assert isinstance(self.client.timeout, httpx.Timeout)

    def test_copy_default_headers(self) -> None:
        client = AnthropicVertex(
            base_url=base_url,
            region="region",
            project_id="project",
            _strict_response_validation=True,
            default_headers={"X-Foo": "bar"},
        )
        assert client.default_headers["X-Foo"] == "bar"

        # does not override the already given value when not specified
        copied = client.copy()
        assert copied.default_headers["X-Foo"] == "bar"

        # merges already given headers
        copied = client.copy(default_headers={"X-Bar": "stainless"})
        assert copied.default_headers["X-Foo"] == "bar"
        assert copied.default_headers["X-Bar"] == "stainless"

        # uses new values for any already given headers
        copied = client.copy(default_headers={"X-Foo": "stainless"})
        assert copied.default_headers["X-Foo"] == "stainless"

        # set_default_headers

        # completely overrides already set values
        copied = client.copy(set_default_headers={})
        assert copied.default_headers.get("X-Foo") is None

        copied = client.copy(set_default_headers={"X-Bar": "Robert"})
        assert copied.default_headers["X-Bar"] == "Robert"

        with pytest.raises(
            ValueError,
            match="`default_headers` and `set_default_headers` arguments are mutually exclusive",
        ):
            client.copy(set_default_headers={}, default_headers={"X-Foo": "Bar"})


class TestAsyncAnthropicVertex:
    client = AsyncAnthropicVertex(region="region", project_id="project", access_token="my-access-token")

    @pytest.mark.respx()
    @pytest.mark.asyncio()
    async def test_messages_retries(self, respx_mock: MockRouter) -> None:
        request_url = "https://region-aiplatform.googleapis.com/v1/projects/project/locations/region/publishers/anthropic/models/claude-3-sonnet@20240229:rawPredict"
        respx_mock.post(request_url).mock(
            side_effect=[
                httpx.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
                httpx.Response(200, json={"foo": "bar"}),
            ]
        )

        await self.client.with_options(timeout=0.2).messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-sonnet@20240229",
        )

        calls = cast("list[MockRequestCall]", respx_mock.calls)

        assert len(calls) == 2

        assert calls[0].request.url == request_url
        assert calls[1].request.url == request_url

    def test_copy(self) -> None:
        copied = self.client.copy()
        assert id(copied) != id(self.client)

        copied = self.client.copy(region="another-region", project_id="another-project")
        assert copied.region == "another-region"
        assert self.client.region == "region"
        assert copied.project_id == "another-project"
        assert self.client.project_id == "project"

    def test_with_options(self) -> None:
        copied = self.client.with_options(region="another-region", project_id="another-project")
        assert copied.region == "another-region"
        assert self.client.region == "region"
        assert copied.project_id == "another-project"
        assert self.client.project_id == "project"

    def test_copy_default_options(self) -> None:
        # options that have a default are overridden correctly
        copied = self.client.copy(max_retries=7)
        assert copied.max_retries == 7
        assert self.client.max_retries == 2

        copied2 = copied.copy(max_retries=6)
        assert copied2.max_retries == 6
        assert copied.max_retries == 7

        # timeout
        assert isinstance(self.client.timeout, httpx.Timeout)
        copied = self.client.copy(timeout=None)
        assert copied.timeout is None
        assert isinstance(self.client.timeout, httpx.Timeout)

    def test_copy_default_headers(self) -> None:
        client = AsyncAnthropicVertex(
            base_url=base_url,
            region="region",
            project_id="project",
            _strict_response_validation=True,
            default_headers={"X-Foo": "bar"},
        )
        assert client.default_headers["X-Foo"] == "bar"

        # does not override the already given value when not specified
        copied = client.copy()
        assert copied.default_headers["X-Foo"] == "bar"

        # merges already given headers
        copied = client.copy(default_headers={"X-Bar": "stainless"})
        assert copied.default_headers["X-Foo"] == "bar"
        assert copied.default_headers["X-Bar"] == "stainless"

        # uses new values for any already given headers
        copied = client.copy(default_headers={"X-Foo": "stainless"})
        assert copied.default_headers["X-Foo"] == "stainless"

        # set_default_headers

        # completely overrides already set values
        copied = client.copy(set_default_headers={})
        assert copied.default_headers.get("X-Foo") is None

        copied = client.copy(set_default_headers={"X-Bar": "Robert"})
        assert copied.default_headers["X-Bar"] == "Robert"

        with pytest.raises(
            ValueError,
            match="`default_headers` and `set_default_headers` arguments are mutually exclusive",
        ):
            client.copy(set_default_headers={}, default_headers={"X-Foo": "Bar"})
