"""Tests for output_format to output_config.format conversion and deprecation."""

import json
import warnings

import httpx
import pytest
from respx import MockRouter
from pydantic import BaseModel

from anthropic import Anthropic, AnthropicError, AsyncAnthropic, _compat


class TestOutputFormatConversion:
    """Test that output_format is properly converted to output_config.format."""

    def test_create_converts_output_format_to_output_config(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .create() converts output_format to output_config.format in request body."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"result": "test"}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
            )

        request = respx_mock.calls.last.request
        body = json.loads(request.content)

        # Should have output_config with format
        assert "output_config" in body
        assert "format" in body["output_config"]
        assert body["output_config"]["format"]["type"] == "json_schema"
        assert body["output_config"]["format"]["schema"]["type"] == "object"

        # Should NOT have output_format in request
        assert "output_format" not in body

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_converts_pydantic_to_output_config(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() converts Pydantic models to output_config.format."""

        class User(BaseModel):
            name: str
            age: int

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"name": "John", "age": 30}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=User,
            )

        request = respx_mock.calls.last.request
        body = json.loads(request.content)

        # Should have output_config with format containing the User schema
        assert "output_config" in body
        assert "format" in body["output_config"]
        assert body["output_config"]["format"]["type"] == "json_schema"
        assert "properties" in body["output_config"]["format"]["schema"]
        assert "name" in body["output_config"]["format"]["schema"]["properties"]
        assert "age" in body["output_config"]["format"]["schema"]["properties"]

        # Should NOT have output_format in request
        assert "output_format" not in body

    def test_stream_converts_output_format_to_output_config(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .stream() converts output_format to output_config.format."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            with client.beta.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "string"}},
            ) as stream: # type: ignore
                pass

        request = respx_mock.calls.last.request
        body = json.loads(request.content)

        assert "output_config" in body
        assert "format" in body["output_config"]
        assert body["output_config"]["format"]["type"] == "json_schema"
        assert "output_format" not in body

    def test_count_tokens_converts_output_format_to_output_config(
        self, client: Anthropic, respx_mock: MockRouter
    ) -> None:
        """Verify .count_tokens() converts output_format to output_config.format."""
        respx_mock.post("/v1/messages/count_tokens?beta=true").mock(
            return_value=httpx.Response(200, json={"input_tokens": 10})
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            client.beta.messages.count_tokens(
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "array"}},
            )

        request = respx_mock.calls.last.request
        body = json.loads(request.content)

        assert "output_config" in body
        assert "format" in body["output_config"]
        assert body["output_config"]["format"]["type"] == "json_schema"
        assert "output_format" not in body


class TestOutputFormatDeprecation:
    """Test that output_format parameter emits deprecation warnings."""

    def test_create_emits_deprecation_warning(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .create() emits DeprecationWarning when output_format is used."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with pytest.warns(DeprecationWarning, match="output_format.*deprecated.*output_config.format"):
            client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
            )

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_emits_deprecation_warning(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() emits DeprecationWarning when output_format is used."""

        class SimpleModel(BaseModel):
            value: str

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"value": "test"}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with pytest.warns(DeprecationWarning, match="output_format.*deprecated.*output_config.format"):
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=SimpleModel,
            )

    def test_stream_emits_deprecation_warning(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .stream() emits DeprecationWarning when output_format is used."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with pytest.warns(DeprecationWarning, match="output_format.*deprecated.*output_config.format"):
            with client.beta.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "string"}},
            ) as stream: # type: ignore
                pass

    def test_count_tokens_emits_deprecation_warning(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .count_tokens() emits DeprecationWarning when output_format is used."""
        respx_mock.post("/v1/messages/count_tokens?beta=true").mock(
            return_value=httpx.Response(200, json={"input_tokens": 10})
        )

        with pytest.warns(DeprecationWarning, match="output_format.*deprecated.*output_config.format"):
            client.beta.messages.count_tokens(
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "array"}},
            )

    def test_no_warning_when_output_format_not_provided(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify no deprecation warning when output_format is not used."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            # Should not raise any warnings
            client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
            )

    def test_no_warning_when_using_output_config(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify no deprecation warning when using output_config.format directly."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            # Should not raise any warnings
            client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_config={"format": {"type": "json_schema", "schema": {"type": "object"}}},
            )


class TestOutputConfigConflict:
    """Test that providing both output_format and output_config.format raises an error."""

    def test_create_rejects_both_output_format_and_config(self, client: Anthropic) -> None:
        """Verify .create() raises error when both output_format and output_config.format are provided."""
        with pytest.raises(AnthropicError, match="Both output_format and output_config.format were provided"):
            client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
                output_config={"format": {"type": "json_schema", "schema": {"type": "string"}}},
            )

    def test_parse_rejects_both_output_format_and_config(self, client: Anthropic) -> None:
        """Verify .parse() raises error when both output_format and output_config.format are provided."""

        class TestModel(BaseModel):
            value: str

        with pytest.raises(AnthropicError, match="Both output_format and output_config.format were provided"):
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=TestModel,
                output_config={"format": {"type": "json_schema", "schema": {"type": "string"}}},
            )

    def test_count_tokens_rejects_both_output_format_and_config(self, client: Anthropic) -> None:
        """Verify .count_tokens() raises error when both are provided."""
        with pytest.raises(AnthropicError, match="Both output_format and output_config.format were provided"):
            client.beta.messages.count_tokens(
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
                output_config={"format": {"type": "json_schema", "schema": {"type": "string"}}},
            )

    def test_allows_output_config_without_format(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify output_config without format field can be used with output_format."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            # Should succeed - output_config.effort is fine with output_format
            client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
                output_config={"effort": "high"},  # No format field, so no conflict
            )


class TestStructuredOutputsBetaHeader:
    """Test that structured-outputs-2025-12-15 beta header is added for .parse()."""

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_adds_structured_outputs_beta_header(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() auto-adds structured-outputs-2025-12-15 beta header."""

        class DataModel(BaseModel):
            value: int

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"value": 42}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=DataModel,
            )

        request = respx_mock.calls.last.request
        assert "anthropic-beta" in request.headers
        assert "structured-outputs-2025-12-15" in request.headers["anthropic-beta"]

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_preserves_existing_betas(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() preserves other beta headers when adding structured-outputs."""

        class DataModel(BaseModel):
            value: int

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"value": 42}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=DataModel,
                betas=["some-other-beta-feature"],
            )

        request = respx_mock.calls.last.request
        beta_header = request.headers["anthropic-beta"]
        assert "structured-outputs-2025-12-15" in beta_header
        assert "some-other-beta-feature" in beta_header

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_does_not_duplicate_beta_header(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() doesn't duplicate structured-outputs beta if already present."""

        class DataModel(BaseModel):
            value: int

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"value": 42}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=DataModel,
                betas=["structured-outputs-2025-12-15"],
            )

        request = respx_mock.calls.last.request
        beta_header = request.headers["anthropic-beta"]
        # Should only appear once
        assert beta_header.count("structured-outputs-2025-12-15") == 1


class TestAsyncOutputFormatConversion:
    """Test async variants of output_format conversion."""

    async def test_async_create_converts_output_format(
        self, async_client: AsyncAnthropic, respx_mock: MockRouter
    ) -> None:
        """Verify async .create() converts output_format to output_config.format."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            await async_client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
            )

        request = respx_mock.calls.last.request
        body = json.loads(request.content)

        assert "output_config" in body
        assert "format" in body["output_config"]
        assert "output_format" not in body

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    async def test_async_parse_converts_pydantic(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        """Verify async .parse() converts Pydantic models to output_config.format."""

        class User(BaseModel):
            name: str

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": '{"name": "John"}', "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            await async_client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=User,
            )

        request = respx_mock.calls.last.request
        body = json.loads(request.content)

        assert "output_config" in body
        assert "format" in body["output_config"]
        assert "output_format" not in body

    async def test_async_methods_emit_deprecation_warnings(
        self, async_client: AsyncAnthropic, respx_mock: MockRouter
    ) -> None:
        """Verify async methods emit DeprecationWarning."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-sonnet-4-5",
                    "content": [{"text": "test", "type": "text"}],
                    "stop_reason": "end_turn",
                    "usage": {"input_tokens": 10, "output_tokens": 20},
                },
            )
        )

        with pytest.warns(DeprecationWarning, match="output_format.*deprecated"):
            await async_client.beta.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "object"}},
            )
