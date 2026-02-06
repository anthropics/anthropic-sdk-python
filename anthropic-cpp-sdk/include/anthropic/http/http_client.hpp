#pragma once

#include <string>
#include <map>
#include <vector>
#include <memory>
#include <functional>

namespace anthropic {
namespace http {

struct Request {
    std::string method;  // GET, POST, PUT, DELETE, etc.
    std::string url;
    std::map<std::string, std::string> headers;
    std::string body;
    int timeout_ms = 600000;  // 10 minutes default
};

struct Response {
    int status_code = 0;
    std::map<std::string, std::string> headers;
    std::string body;
    bool success = false;
};

// Callback for streaming responses (returns true to continue, false to stop)
using StreamCallback = std::function<bool(const std::string& chunk)>;

// Abstract HTTP client interface
class HttpClient {
public:
    virtual ~HttpClient() = default;

    // Synchronous request
    virtual Response execute(const Request& request) = 0;

    // Streaming request (calls callback for each chunk)
    virtual Response execute_stream(const Request& request, StreamCallback callback) = 0;

    // Set default headers for all requests
    virtual void set_default_headers(const std::map<std::string, std::string>& headers) = 0;
};

// Factory function to create platform-specific HTTP client
std::unique_ptr<HttpClient> create_http_client();

} // namespace http
} // namespace anthropic
