# Test for issue #1118: Batch + Structured Outputs - betas parameter bug
# Tests that betas in MessageCreateParamsNonStreaming are stripped when used in batch requests

from __future__ import annotations

import json
from unittest.mock import Mock, patch

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic.types.beta.messages import BetaMessageBatch


class TestBatchBetasStripping:
    """Test that betas parameter is stripped from individual request params in batch processing."""

    @pytest.mark.respx
    def test_betas_stripped_from_request_params(self, respx_mock: MockRouter) -> None:
        """Test that betas in request params are stripped before sending to API."""
        client = Anthropic(api_key="test-key", base_url="http://127.0.0.1:4010")

        # Mock the API response
        respx_mock.post("/v1/messages/batches?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "batch_123",
                    "type": "message_batch",
                    "processing_status": "in_progress",
                    "request_counts": {
                        "processing": 1,
                        "succeeded": 0,
                        "errored": 0,
                        "canceled": 0,
                        "expired": 0,
                    },
                    "ended_at": None,
                    "created_at": "2024-01-01T00:00:00Z",
                    "expires_at": "2024-01-02T00:00:00Z",
                    "cancel_initiated_at": None,
                    "results_url": None,
                },
            )
        )

        # Create a batch with betas in both batch-level and request params
        batch = client.beta.messages.batches.create(
            betas=["structured-outputs-2025-11-13"],
            requests=[
                {
                    "custom_id": "test-1",
                    "params": {
                        "model": "claude-sonnet-4-5",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": "Hello"}],
                        # This should be stripped
                        "betas": ["structured-outputs-2025-11-13"],
                        "output_format": {
                            "type": "json_schema",
                            "schema": {"type": "object", "properties": {"name": {"type": "string"}}},
                        },
                    },
                }
            ],
        )

        assert batch.id == "batch_123"

        # Verify the request body doesn't contain betas in params
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls[0].request
        body = json.loads(request.content.decode())

        # Check that the request params don't have betas
        assert "requests" in body
        assert len(body["requests"]) == 1
        assert "params" in body["requests"][0]
        assert "betas" not in body["requests"][0]["params"], "betas should be stripped from request params"
        assert "output_format" in body["requests"][0]["params"], "output_format should still be present"

        # Check that the header has the beta
        assert "anthropic-beta" in request.headers
        assert "structured-outputs-2025-11-13" in request.headers["anthropic-beta"]
        assert "message-batches-2024-09-24" in request.headers["anthropic-beta"]

    @pytest.mark.respx
    async def test_async_betas_stripped_from_request_params(self, respx_mock: MockRouter) -> None:
        """Test that betas in request params are stripped in async client."""
        client = AsyncAnthropic(api_key="test-key", base_url="http://127.0.0.1:4010")

        # Mock the API response
        respx_mock.post("/v1/messages/batches?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "batch_456",
                    "type": "message_batch",
                    "processing_status": "in_progress",
                    "request_counts": {
                        "processing": 1,
                        "succeeded": 0,
                        "errored": 0,
                        "canceled": 0,
                        "expired": 0,
                    },
                    "ended_at": None,
                    "created_at": "2024-01-01T00:00:00Z",
                    "expires_at": "2024-01-02T00:00:00Z",
                    "cancel_initiated_at": None,
                    "results_url": None,
                },
            )
        )

        # Create a batch with betas in request params
        batch = await client.beta.messages.batches.create(
            betas=["structured-outputs-2025-11-13"],
            requests=[
                {
                    "custom_id": "test-2",
                    "params": {
                        "model": "claude-sonnet-4-5",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": "Hello async"}],
                        # This should be stripped
                        "betas": ["structured-outputs-2025-11-13"],
                        "output_format": {
                            "type": "json_schema",
                            "schema": {"type": "object", "properties": {"email": {"type": "string"}}},
                        },
                    },
                }
            ],
        )

        assert batch.id == "batch_456"

        # Verify the request body doesn't contain betas in params
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls[0].request
        body = json.loads(request.content.decode())

        # Check that the request params don't have betas
        assert "betas" not in body["requests"][0]["params"], "betas should be stripped from request params"

    @pytest.mark.respx
    def test_multiple_requests_with_betas_all_stripped(self, respx_mock: MockRouter) -> None:
        """Test that betas are stripped from all requests in a batch."""
        client = Anthropic(api_key="test-key", base_url="http://127.0.0.1:4010")

        respx_mock.post("/v1/messages/batches?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "batch_789",
                    "type": "message_batch",
                    "processing_status": "in_progress",
                    "request_counts": {
                        "processing": 2,
                        "succeeded": 0,
                        "errored": 0,
                        "canceled": 0,
                        "expired": 0,
                    },
                    "ended_at": None,
                    "created_at": "2024-01-01T00:00:00Z",
                    "expires_at": "2024-01-02T00:00:00Z",
                    "cancel_initiated_at": None,
                    "results_url": None,
                },
            )
        )

        # Create a batch with multiple requests, each with betas
        batch = client.beta.messages.batches.create(
            betas=["structured-outputs-2025-11-13"],
            requests=[
                {
                    "custom_id": "test-3",
                    "params": {
                        "model": "claude-sonnet-4-5",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": "First"}],
                        "betas": ["structured-outputs-2025-11-13"],
                    },
                },
                {
                    "custom_id": "test-4",
                    "params": {
                        "model": "claude-sonnet-4-5",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": "Second"}],
                        "betas": ["structured-outputs-2025-11-13"],
                    },
                },
            ],
        )

        assert batch.id == "batch_789"

        # Verify both requests have betas stripped
        request = respx_mock.calls[0].request
        body = json.loads(request.content.decode())

        assert len(body["requests"]) == 2
        for req in body["requests"]:
            assert "betas" not in req["params"], "betas should be stripped from all request params"

    @pytest.mark.respx
    def test_request_without_betas_unchanged(self, respx_mock: MockRouter) -> None:
        """Test that requests without betas field are not affected."""
        client = Anthropic(api_key="test-key", base_url="http://127.0.0.1:4010")

        respx_mock.post("/v1/messages/batches?beta=true").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "batch_abc",
                    "type": "message_batch",
                    "processing_status": "in_progress",
                    "request_counts": {
                        "processing": 1,
                        "succeeded": 0,
                        "errored": 0,
                        "canceled": 0,
                        "expired": 0,
                    },
                    "ended_at": None,
                    "created_at": "2024-01-01T00:00:00Z",
                    "expires_at": "2024-01-02T00:00:00Z",
                    "cancel_initiated_at": None,
                    "results_url": None,
                },
            )
        )

        # Create a batch without betas in request params
        batch = client.beta.messages.batches.create(
            betas=["structured-outputs-2025-11-13"],
            requests=[
                {
                    "custom_id": "test-5",
                    "params": {
                        "model": "claude-sonnet-4-5",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": "No betas here"}],
                    },
                }
            ],
        )

        assert batch.id == "batch_abc"

        # Verify the request is processed normally
        request = respx_mock.calls[0].request
        body = json.loads(request.content.decode())

        assert "model" in body["requests"][0]["params"]
        assert "max_tokens" in body["requests"][0]["params"]
