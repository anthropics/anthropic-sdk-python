"""Tests for output_format to output_config.format conversion."""

import json
import warnings

import httpx2
import pytest
from respx import MockRouter
from pydantic import BaseModel

from anthropic import Anthropic, AnthropicError, AsyncAnthropic, _compat


class TestOutputFormatConversion:
    """Test that output_format is properly converted to output_config.format."""

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_converts_pydantic_to_output_config(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() converts Pydantic models to output_config.format."""

        class User(BaseModel):
            name: str
            age: int

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx2.Response(
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

    def test_stream_rejects_schema_dict(self, client: Anthropic) -> None:
        """A raw schema dict is no longer accepted by `.stream()`; it belongs in `output_config.format`."""
        with pytest.raises(TypeError, match="output_config"):
            client.beta.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format={"type": "json_schema", "schema": {"type": "string"}},  # type: ignore[arg-type]
            )


class TestOutputFormatNoDeprecationWarning:
    """The typed `output_format=` of the helpers is the supported form and must not warn."""

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_does_not_warn_for_type(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """`.parse(output_format=Model)` is silent."""

        class SimpleModel(BaseModel):
            value: str

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx2.Response(
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

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            client.beta.messages.parse(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=SimpleModel,
            )

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_stream_does_not_warn_for_type(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """`.stream(output_format=Model)` is silent."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx2.Response(
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

        class Answer(BaseModel):
            text: str

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            with client.beta.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Test"}],
                model="claude-sonnet-4-5",
                output_format=Answer,
            ):
                pass

        body = json.loads(respx_mock.calls.last.request.content)
        assert body["output_config"]["format"]["type"] == "json_schema"
        assert "output_format" not in body

    def test_no_warning_when_output_format_not_provided(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify no deprecation warning when output_format is not used."""
        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx2.Response(
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
            return_value=httpx2.Response(
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


class TestStructuredOutputsBetaHeader:
    """Test that structured-outputs-2025-12-15 beta header is added for .parse()."""

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    def test_parse_adds_structured_outputs_beta_header(self, client: Anthropic, respx_mock: MockRouter) -> None:
        """Verify .parse() auto-adds structured-outputs-2025-12-15 beta header."""

        class DataModel(BaseModel):
            value: int

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx2.Response(
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
            return_value=httpx2.Response(
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
            return_value=httpx2.Response(
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

    @pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
    async def test_async_parse_converts_pydantic(self, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        """Verify async .parse() converts Pydantic models to output_config.format."""

        class User(BaseModel):
            name: str

        respx_mock.post("/v1/messages?beta=true").mock(
            return_value=httpx2.Response(
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
