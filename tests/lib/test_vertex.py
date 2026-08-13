from __future__ import annotations

import os
import sys
import json
from typing import Any, Dict, List, cast
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

from anthropic import AnthropicVertex, AsyncAnthropicVertex, beta_tool, beta_async_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.vertex._auth import refresh_auth
from anthropic.lib._extras._common import MissingDependencyError

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class MockRequestCall(Protocol):
    request: httpx.Request


TOOL_RUNNER_URL = "https://region-aiplatform.googleapis.com/v1/projects/project/locations/region/publishers/anthropic/models/claude-haiku-4-5@20251001:rawPredict"


def _vertex_message(content: List[Dict[str, Any]], stop_reason: str) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "msg_01",
            "type": "message",
            "role": "assistant",
            "model": "claude",
            "content": content,
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 5},
        },
    )


def _tool_runner_responses() -> List[httpx.Response]:
    return [
        _vertex_message(
            [{"type": "tool_use", "id": "toolu_01", "name": "get_weather", "input": {"city": "Paris"}}],
            "tool_use",
        ),
        _vertex_message([{"type": "text", "text": "It is sunny in Paris."}], "end_turn"),
    ]


def _assert_tool_runner_calls(calls: List[MockRequestCall]) -> None:
    assert len(calls) == 2
    for call in calls:
        assert call.request.url == TOOL_RUNNER_URL
        assert call.request.headers["Authorization"] == "Bearer my-access-token"
        body = json.loads(call.request.content)
        assert "model" not in body and "stream" not in body and "output_format" not in body
        assert body["anthropic_version"] == "vertex-2023-10-16"
    second = json.loads(calls[1].request.content)
    assert [m["role"] for m in second["messages"]] == ["user", "assistant", "user"]
    assert second["messages"][1]["content"][0]["type"] == "tool_use"
    assert second["messages"][2]["content"][0] == {
        "type": "tool_result",
        "tool_use_id": "toolu_01",
        "content": "sunny in Paris",
    }


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

    def test_copy_x_stainless_helper_header_appends(self) -> None:
        # `x-stainless-helper` accumulates across copies instead of being clobbered
        client = AnthropicVertex(
            base_url=base_url,
            region="region",
            project_id="project",
            _strict_response_validation=True,
            default_headers={"x-stainless-helper": "parent"},
        )
        copied = client.copy(default_headers={"x-stainless-helper": "child"})
        assert copied.default_headers["x-stainless-helper"] == "parent, child"

    def test_global_region_base_url(self) -> None:
        """Test that global region uses the correct base URL."""
        client = AnthropicVertex(region="global", project_id="test-project", access_token="fake-token")
        assert str(client.base_url).rstrip("/") == "https://aiplatform.googleapis.com/v1"

    def test_us_region_base_url(self) -> None:
        """Test that us region uses the correct base URL."""
        client = AnthropicVertex(region="us", project_id="test-project", access_token="fake-token")
        assert str(client.base_url).rstrip("/") == "https://aiplatform.us.rep.googleapis.com/v1"

    def test_eu_region_base_url(self) -> None:
        """Test that us region uses the correct base URL."""
        client = AnthropicVertex(region="eu", project_id="test-project", access_token="fake-token")
        assert str(client.base_url).rstrip("/") == "https://aiplatform.eu.rep.googleapis.com/v1"

    @pytest.mark.parametrize("region", ["us-central1", "europe-west1", "asia-southeast1"])
    def test_regional_base_url(self, region: str) -> None:
        """Test that regional endpoints use the correct base URL format."""
        client = AnthropicVertex(region=region, project_id="test-project", access_token="fake-token")
        expected_url = f"https://{region}-aiplatform.googleapis.com/v1"
        assert str(client.base_url).rstrip("/") == expected_url

    def test_env_var_base_url_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that ANTHROPIC_VERTEX_BASE_URL environment variable does not override client arg."""
        test_url = "https://custom-endpoint.googleapis.com/v1"

        monkeypatch.setenv("ANTHROPIC_VERTEX_BASE_URL", test_url)

        client = AnthropicVertex(
            region="global",  # we expect this to get ignored since the user is providing a base_url
            project_id="test-project",
            access_token="fake-token",
            base_url="https://test.googleapis.com/v1",
        )
        assert str(client.base_url).rstrip("/") == "https://test.googleapis.com/v1"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
    @pytest.mark.respx()
    def test_beta_tool_runner_routes_through_raw_predict(self, respx_mock: MockRouter) -> None:
        @beta_tool
        def get_weather(city: str) -> str:
            """Get the weather.

            Args:
                city: city name
            """
            return f"sunny in {city}"

        respx_mock.post(url__startswith="https://region-aiplatform.googleapis.com/").mock(
            side_effect=_tool_runner_responses()
        )

        final = self.client.beta.messages.tool_runner(
            model="claude-haiku-4-5@20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": "weather in Paris?"}],
            tools=[get_weather],
        ).until_done()

        assert final.stop_reason == "end_turn"
        _assert_tool_runner_calls(cast("list[MockRequestCall]", respx_mock.calls))

    def test_beta_messages_helpers_are_bound(self) -> None:
        for name in ("create", "parse", "stream", "tool_runner", "count_tokens"):
            assert callable(getattr(self.client.beta.messages, name))


def test_refresh_without_google_auth_raises_actionable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    # `None` in sys.modules makes the import fail even when google-auth is installed.
    monkeypatch.setitem(sys.modules, "google.auth.transport.requests", cast(Any, None))

    class FakeCredentials:
        def refresh(self, _request: object) -> None:
            raise AssertionError("should not be reached: building the request needs google-auth")

    with pytest.raises(MissingDependencyError, match=r"anthropic\[vertex\]"):
        refresh_auth(cast(Any, FakeCredentials()))


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

    def test_copy_x_stainless_helper_header_appends(self) -> None:
        # `x-stainless-helper` accumulates across copies instead of being clobbered
        client = AsyncAnthropicVertex(
            base_url=base_url,
            region="region",
            project_id="project",
            _strict_response_validation=True,
            default_headers={"x-stainless-helper": "parent"},
        )
        copied = client.copy(default_headers={"x-stainless-helper": "child"})
        assert copied.default_headers["x-stainless-helper"] == "parent, child"

    def test_global_region_base_url(self) -> None:
        """Test that global region uses the correct base URL."""
        client = AsyncAnthropicVertex(region="global", project_id="test-project", access_token="fake-token")
        assert str(client.base_url).rstrip("/") == "https://aiplatform.googleapis.com/v1"

    def test_us_region_base_url(self) -> None:
        """Test that us region uses the correct base URL."""
        client = AsyncAnthropicVertex(region="us", project_id="test-project", access_token="fake-token")
        assert str(client.base_url).rstrip("/") == "https://aiplatform.us.rep.googleapis.com/v1"

    def test_eu_region_base_url(self) -> None:
        """Test that eu region uses the correct base URL."""
        client = AsyncAnthropicVertex(region="eu", project_id="test-project", access_token="fake-token")
        assert str(client.base_url).rstrip("/") == "https://aiplatform.eu.rep.googleapis.com/v1"

    def test_regional_base_url(self) -> None:
        """Test that regional endpoints use the correct base URL format."""
        test_regions = ["us-central1", "europe-west1", "asia-southeast1"]

        for region in test_regions:
            client = AsyncAnthropicVertex(region=region, project_id="test-project", access_token="fake-token")
            expected_url = f"https://{region}-aiplatform.googleapis.com/v1"
            assert str(client.base_url).rstrip("/") == expected_url

    def test_env_var_base_url_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that ANTHROPIC_VERTEX_BASE_URL environment variable does not override client arg."""
        test_url = "https://custom-endpoint.googleapis.com/v1"

        monkeypatch.setenv("ANTHROPIC_VERTEX_BASE_URL", test_url)

        client = AsyncAnthropicVertex(
            region="global",  # we expect this to get ignored since the user is providing a base_url
            project_id="test-project",
            access_token="fake-token",
            base_url="https://test.googleapis.com/v1",
        )
        assert str(client.base_url).rstrip("/") == "https://test.googleapis.com/v1"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
    @pytest.mark.respx()
    @pytest.mark.asyncio()
    async def test_beta_tool_runner_routes_through_raw_predict(self, respx_mock: MockRouter) -> None:
        @beta_async_tool
        async def get_weather(city: str) -> str:
            """Get the weather.

            Args:
                city: city name
            """
            return f"sunny in {city}"

        respx_mock.post(url__startswith="https://region-aiplatform.googleapis.com/").mock(
            side_effect=_tool_runner_responses()
        )

        final = await self.client.beta.messages.tool_runner(
            model="claude-haiku-4-5@20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": "weather in Paris?"}],
            tools=[get_weather],
        ).until_done()

        assert final.stop_reason == "end_turn"
        _assert_tool_runner_calls(cast("list[MockRequestCall]", respx_mock.calls))

    def test_beta_messages_helpers_are_bound(self) -> None:
        for name in ("create", "parse", "stream", "tool_runner", "count_tokens"):
            assert callable(getattr(self.client.beta.messages, name))
