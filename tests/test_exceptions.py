"""Comprehensive tests for anthropic exception classes."""

from __future__ import annotations

import httpx
import pytest

from anthropic._exceptions import (
    AnthropicError,
    APIError,
    APIResponseValidationError,
    APIStatusError,
    APIConnectionError,
    APITimeoutError,
    BadRequestError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ConflictError,
    RequestTooLargeError,
    UnprocessableEntityError,
    RateLimitError,
    ServiceUnavailableError,
    OverloadedError,
    DeadlineExceededError,
    InternalServerError,
)


class TestAnthropicError:
    """Test the base AnthropicError exception."""

    def test_can_be_raised(self) -> None:
        with pytest.raises(AnthropicError):
            raise AnthropicError("test error")

    def test_inherits_from_exception(self) -> None:
        assert issubclass(AnthropicError, Exception)


class TestAPIError:
    """Test the APIError exception."""

    def test_initialization(self) -> None:
        request = httpx.Request("GET", "https://api.anthropic.com/test")
        body = {"error": "test error"}
        error = APIError("Test message", request, body=body)

        assert error.message == "Test message"
        assert error.request == request
        assert error.body == body
        assert str(error) == "Test message"

    def test_with_none_body(self) -> None:
        request = httpx.Request("GET", "https://api.anthropic.com/test")
        error = APIError("Test message", request, body=None)

        assert error.message == "Test message"
        assert error.request == request
        assert error.body is None

    def test_inherits_from_anthropic_error(self) -> None:
        assert issubclass(APIError, AnthropicError)


class TestAPIResponseValidationError:
    """Test the APIResponseValidationError exception."""

    def test_initialization_with_custom_message(self) -> None:
        request = httpx.Request("GET", "https://api.anthropic.com/test")
        response = httpx.Response(200, json={"invalid": "data"}, request=request)
        body = {"invalid": "data"}
        error = APIResponseValidationError(response, body, message="Custom validation error")

        assert error.message == "Custom validation error"
        assert error.response == response
        assert error.status_code == 200
        assert error.body == body

    def test_initialization_with_default_message(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(422, json={"error": "validation failed"}, request=request)
        body = {"error": "validation failed"}
        error = APIResponseValidationError(response, body)

        assert error.message == "Data returned by API invalid for expected schema."
        assert error.status_code == 422

    def test_inherits_from_api_error(self) -> None:
        assert issubclass(APIResponseValidationError, APIError)


class TestAPIStatusError:
    """Test the APIStatusError exception."""

    def test_initialization(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/messages")
        response = httpx.Response(
            500,
            json={"error": "server error"},
            headers={"request-id": "req_123456"},
            request=request,
        )
        body = {"error": "server error"}
        error = APIStatusError("Server error occurred", response=response, body=body)

        assert error.message == "Server error occurred"
        assert error.response == response
        assert error.status_code == 500
        assert error.request_id == "req_123456"
        assert error.body == body

    def test_without_request_id_header(self) -> None:
        request = httpx.Request("GET", "https://api.anthropic.com/test")
        response = httpx.Response(404, json={"error": "not found"}, request=request)
        error = APIStatusError("Not found", response=response, body=None)

        assert error.status_code == 404
        assert error.request_id is None

    def test_inherits_from_api_error(self) -> None:
        assert issubclass(APIStatusError, APIError)


class TestAPIConnectionError:
    """Test the APIConnectionError exception."""

    def test_default_message(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/messages")
        error = APIConnectionError(request=request)

        assert error.message == "Connection error."
        assert error.request == request
        assert error.body is None

    def test_custom_message(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/messages")
        error = APIConnectionError(message="Network unreachable", request=request)

        assert error.message == "Network unreachable"

    def test_inherits_from_api_error(self) -> None:
        assert issubclass(APIConnectionError, APIError)


class TestAPITimeoutError:
    """Test the APITimeoutError exception."""

    def test_initialization(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/messages")
        error = APITimeoutError(request)

        assert error.message == "Request timed out."
        assert error.request == request
        assert error.body is None

    def test_inherits_from_connection_error(self) -> None:
        assert issubclass(APITimeoutError, APIConnectionError)


class TestBadRequestError:
    """Test the BadRequestError exception (400)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(400, json={"error": "bad request"}, request=request)
        error = BadRequestError("Bad request", response=response, body=None)

        assert error.status_code == 400

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(BadRequestError, APIStatusError)


class TestAuthenticationError:
    """Test the AuthenticationError exception (401)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(401, json={"error": "unauthorized"}, request=request)
        error = AuthenticationError("Invalid API key", response=response, body=None)

        assert error.status_code == 401

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(AuthenticationError, APIStatusError)


class TestPermissionDeniedError:
    """Test the PermissionDeniedError exception (403)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(403, json={"error": "forbidden"}, request=request)
        error = PermissionDeniedError("Access denied", response=response, body=None)

        assert error.status_code == 403

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(PermissionDeniedError, APIStatusError)


class TestNotFoundError:
    """Test the NotFoundError exception (404)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(404, json={"error": "not found"}, request=request)
        error = NotFoundError("Resource not found", response=response, body=None)

        assert error.status_code == 404

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(NotFoundError, APIStatusError)


class TestConflictError:
    """Test the ConflictError exception (409)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(409, json={"error": "conflict"}, request=request)
        error = ConflictError("Resource conflict", response=response, body=None)

        assert error.status_code == 409

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(ConflictError, APIStatusError)


class TestRequestTooLargeError:
    """Test the RequestTooLargeError exception (413)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(413, json={"error": "payload too large"}, request=request)
        error = RequestTooLargeError("Request too large", response=response, body=None)

        assert error.status_code == 413

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(RequestTooLargeError, APIStatusError)


class TestUnprocessableEntityError:
    """Test the UnprocessableEntityError exception (422)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(422, json={"error": "validation failed"}, request=request)
        error = UnprocessableEntityError("Unprocessable entity", response=response, body=None)

        assert error.status_code == 422

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(UnprocessableEntityError, APIStatusError)


class TestRateLimitError:
    """Test the RateLimitError exception (429)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(429, json={"error": "rate limit exceeded"}, request=request)
        error = RateLimitError("Rate limit exceeded", response=response, body=None)

        assert error.status_code == 429

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(RateLimitError, APIStatusError)


class TestServiceUnavailableError:
    """Test the ServiceUnavailableError exception (503)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(503, json={"error": "service unavailable"}, request=request)
        error = ServiceUnavailableError("Service unavailable", response=response, body=None)

        assert error.status_code == 503

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(ServiceUnavailableError, APIStatusError)


class TestOverloadedError:
    """Test the OverloadedError exception (529)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(529, json={"error": "overloaded"}, request=request)
        error = OverloadedError("Service overloaded", response=response, body=None)

        assert error.status_code == 529

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(OverloadedError, APIStatusError)


class TestDeadlineExceededError:
    """Test the DeadlineExceededError exception (504)."""

    def test_status_code(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(504, json={"error": "deadline exceeded"}, request=request)
        error = DeadlineExceededError("Deadline exceeded", response=response, body=None)

        assert error.status_code == 504

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(DeadlineExceededError, APIStatusError)


class TestInternalServerError:
    """Test the InternalServerError exception (5xx)."""

    def test_can_be_raised(self) -> None:
        request = httpx.Request("POST", "https://api.anthropic.com/test")
        response = httpx.Response(500, json={"error": "internal server error"}, request=request)
        error = InternalServerError("Internal server error", response=response, body=None)

        assert error.status_code == 500
        assert isinstance(error, APIStatusError)

    def test_inherits_from_status_error(self) -> None:
        assert issubclass(InternalServerError, APIStatusError)


class TestExceptionHierarchy:
    """Test the overall exception hierarchy."""

    def test_all_status_errors_inherit_from_api_status_error(self) -> None:
        status_errors = [
            BadRequestError,
            AuthenticationError,
            PermissionDeniedError,
            NotFoundError,
            ConflictError,
            RequestTooLargeError,
            UnprocessableEntityError,
            RateLimitError,
            ServiceUnavailableError,
            OverloadedError,
            DeadlineExceededError,
            InternalServerError,
        ]

        for error_class in status_errors:
            assert issubclass(error_class, APIStatusError)

    def test_all_api_errors_inherit_from_anthropic_error(self) -> None:
        api_errors = [
            APIError,
            APIResponseValidationError,
            APIStatusError,
            APIConnectionError,
            APITimeoutError,
        ]

        for error_class in api_errors:
            assert issubclass(error_class, AnthropicError)

    def test_all_errors_inherit_from_exception(self) -> None:
        all_errors = [
            AnthropicError,
            APIError,
            APIResponseValidationError,
            APIStatusError,
            APIConnectionError,
            APITimeoutError,
            BadRequestError,
            AuthenticationError,
            PermissionDeniedError,
            NotFoundError,
            ConflictError,
            RequestTooLargeError,
            UnprocessableEntityError,
            RateLimitError,
            ServiceUnavailableError,
            OverloadedError,
            DeadlineExceededError,
            InternalServerError,
        ]

        for error_class in all_errors:
            assert issubclass(error_class, Exception)
