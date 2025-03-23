from __future__ import annotations

import json
import httpx
import typing
from typing import Any, Dict, List, Union, Callable, Optional, Sequence, cast
from dataclasses import dataclass, field

from ...._base_client import BaseClient, AsyncAPIClient, SyncAPIClient


class MockResponse:
    """A simple response object for mocking API responses."""
    def __init__(
        self,
        *,
        status_code: int = 200,
        content: bytes | str | dict | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.status_code = status_code
        self.headers = headers or {}
        
        if content is None:
            self._content = b''
        elif isinstance(content, bytes):
            self._content = content
        elif isinstance(content, str):
            self._content = content.encode("utf-8")
        elif isinstance(content, dict):
            self._content = json.dumps(content).encode("utf-8")
            self.headers.setdefault("Content-Type", "application/json")
        else:
            raise TypeError(f"Unsupported content type: {type(content)}")

    @property
    def content(self) -> bytes:
        return self._content

    def json(self) -> Any:
        return json.loads(self.content)

    def text(self) -> str:
        return self.content.decode("utf-8")

    def read(self) -> bytes:
        return self.content


@dataclass
class MockResponseBuilder:
    """Builds mock responses for offline mode."""
    
    responses: Dict[str, List[MockResponse]] = field(default_factory=dict)
    default_response: Optional[MockResponse] = None

    def add(
        self,
        method: str,
        path: str,
        response: MockResponse,
    ) -> None:
        """Add a mock response for a specific method and path."""
        key = f"{method.upper()}:{path}"
        if key not in self.responses:
            self.responses[key] = []
        self.responses[key].append(response)

    def set_default_response(self, response: MockResponse) -> None:
        """Set a default response for any unmatched requests."""
        self.default_response = response

    def get(self, method: str, path: str) -> MockResponse:
        """Get a mock response for a method and path."""
        key = f"{method.upper()}:{path}"
        if key in self.responses and self.responses[key]:
            # Pop the first response in the queue
            return self.responses[key].pop(0)
        
        if self.default_response:
            return self.default_response
            
        # Default fallback response
        return MockResponse(
            status_code=404,
            content={"error": {"message": f"No mock response found for {method} {path}"}},
        )


_response_builder = MockResponseBuilder()


def get_mock_response(method: str, path: str) -> MockResponse:
    """Get a mock response for a given request."""
    return _response_builder.get(method, path)


def mock_request(
    self: SyncAPIClient,
    cast_to: Any,
    options: Any,
    stream: bool = False,
    stream_cls: Optional[Any] = None,
) -> Any:
    """Mock synchronous request method that returns predefined responses."""
    mock_response = get_mock_response(options.method, options.url)
    
    # Convert to httpx.Response
    response = httpx.Response(
        status_code=mock_response.status_code,
        headers=mock_response.headers,
        content=mock_response.content,
    )
    
    # Process via the standard client pipeline
    return self._process_response(
        cast_to=cast_to,
        options=options,
        response=response,
        stream=stream,
        stream_cls=stream_cls,
        retries_taken=0
    )


async def mock_async_request(
    self: AsyncAPIClient,
    cast_to: Any,
    options: Any,
    stream: bool = False,
    stream_cls: Optional[Any] = None,
) -> Any:
    """Mock asynchronous request method that returns predefined responses."""
    mock_response = get_mock_response(options.method, options.url)
    
    # Convert to httpx.Response
    response = httpx.Response(
        status_code=mock_response.status_code,
        headers=mock_response.headers,
        content=mock_response.content,
    )
    
    # Process via the standard client pipeline
    return await self._process_response(
        cast_to=cast_to,
        options=options,
        response=response,
        stream=stream,
        stream_cls=stream_cls,
        retries_taken=0
    )


def patch_client_for_offline_mode(client: Union[SyncAPIClient, AsyncAPIClient]) -> None:
    """
    Patch an instance of the client to use mock responses instead of real HTTP requests.
    """
    if isinstance(client, SyncAPIClient):
        # Save original method
        if not hasattr(client, "_original_request"):
            client._original_request = client.request
        
        # Replace request method
        client.request = mock_request.__get__(client)
    elif isinstance(client, AsyncAPIClient):
        # Save original method
        if not hasattr(client, "_original_request"):
            client._original_request = client.request
        
        # Replace request method
        client.request = mock_async_request.__get__(client)
    else:
        raise TypeError(f"Unsupported client type: {type(client)}")


def setup_offline_mode() -> MockResponseBuilder:
    """
    Get the mock response builder to configure offline mode responses.
    
    Example:
        >>> from anthropic.lib.mock import setup_offline_mode
        >>> mock_responses = setup_offline_mode()
        >>> mock_responses.add(
        ...     "POST", 
        ...     "messages", 
        ...     MockResponse(content={"content": [{"text": "Hello, world!"}]})
        ... )
        >>> client = Anthropic(offline_mode=True)
        >>> response = client.messages.create(...)
    """
    # Reset the response builder
    global _response_builder
    _response_builder = MockResponseBuilder()
    
    # Add a default response
    _response_builder.set_default_response(
        MockResponse(
            status_code=200,
            content={
                "id": "msg_mock_response",
                "type": "message",
                "role": "assistant",
                "content": [{"type": "text", "text": "This is a mock response from offline mode."}],
                "model": "claude-3-opus-20240229",
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 10
                }
            }
        )
    )
    
    return _response_builder