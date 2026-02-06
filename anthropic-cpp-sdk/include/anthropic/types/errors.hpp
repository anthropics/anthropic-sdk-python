#pragma once

#include <stdexcept>
#include <string>
#include <optional>

namespace anthropic {

// Base class for all Anthropic SDK errors
class AnthropicError : public std::runtime_error {
public:
    explicit AnthropicError(const std::string& message)
        : std::runtime_error(message) {}
};

// Base class for API-related errors with HTTP status code
class APIError : public AnthropicError {
public:
    APIError(int status_code, const std::string& message, const std::string& response_body = "")
        : AnthropicError(message)
        , status_code_(status_code)
        , response_body_(response_body) {}

    int status_code() const { return status_code_; }
    const std::string& response_body() const { return response_body_; }

private:
    int status_code_;
    std::string response_body_;
};

// 400 Bad Request
class BadRequestError : public APIError {
public:
    BadRequestError(const std::string& message, const std::string& response_body = "")
        : APIError(400, message, response_body) {}
};

// 401 Unauthorized
class AuthenticationError : public APIError {
public:
    AuthenticationError(const std::string& message, const std::string& response_body = "")
        : APIError(401, message, response_body) {}
};

// 403 Forbidden
class PermissionDeniedError : public APIError {
public:
    PermissionDeniedError(const std::string& message, const std::string& response_body = "")
        : APIError(403, message, response_body) {}
};

// 404 Not Found
class NotFoundError : public APIError {
public:
    NotFoundError(const std::string& message, const std::string& response_body = "")
        : APIError(404, message, response_body) {}
};

// 409 Conflict
class ConflictError : public APIError {
public:
    ConflictError(const std::string& message, const std::string& response_body = "")
        : APIError(409, message, response_body) {}
};

// 422 Unprocessable Entity
class UnprocessableEntityError : public APIError {
public:
    UnprocessableEntityError(const std::string& message, const std::string& response_body = "")
        : APIError(422, message, response_body) {}
};

// 429 Too Many Requests
class RateLimitError : public APIError {
public:
    RateLimitError(const std::string& message, const std::string& response_body = "")
        : APIError(429, message, response_body) {}
};

// 500+ Internal Server Error
class InternalServerError : public APIError {
public:
    InternalServerError(int status_code, const std::string& message, const std::string& response_body = "")
        : APIError(status_code, message, response_body) {}
};

// Network-related errors
class ConnectionError : public AnthropicError {
public:
    explicit ConnectionError(const std::string& message)
        : AnthropicError(message) {}
};

class TimeoutError : public AnthropicError {
public:
    explicit TimeoutError(const std::string& message)
        : AnthropicError(message) {}
};

// Helper function to create appropriate error from HTTP status code
inline std::unique_ptr<APIError> create_api_error(int status_code, const std::string& message, const std::string& response_body = "") {
    switch (status_code) {
        case 400:
            return std::make_unique<BadRequestError>(message, response_body);
        case 401:
            return std::make_unique<AuthenticationError>(message, response_body);
        case 403:
            return std::make_unique<PermissionDeniedError>(message, response_body);
        case 404:
            return std::make_unique<NotFoundError>(message, response_body);
        case 409:
            return std::make_unique<ConflictError>(message, response_body);
        case 422:
            return std::make_unique<UnprocessableEntityError>(message, response_body);
        case 429:
            return std::make_unique<RateLimitError>(message, response_body);
        default:
            if (status_code >= 500) {
                return std::make_unique<InternalServerError>(status_code, message, response_body);
            }
            return std::make_unique<APIError>(status_code, message, response_body);
    }
}

} // namespace anthropic
