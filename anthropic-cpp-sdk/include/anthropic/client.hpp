#pragma once

#include "http/http_client.hpp"
#include "utils/retry_logic.hpp"
#include <string>
#include <memory>
#include <map>
#include <optional>

namespace anthropic {

// Forward declarations
namespace resources {
    class Messages;
    class Completions;
    class Models;
}

class Client {
public:
    // Configuration struct
    struct Config {
        std::optional<std::string> api_key;       // From ANTHROPIC_API_KEY env var if not set
        std::optional<std::string> auth_token;    // From ANTHROPIC_AUTH_TOKEN env var if not set
        std::string base_url = "https://api.anthropic.com";
        int timeout_ms = 600000;                  // 10 minutes
        int max_retries = 2;
        std::map<std::string, std::string> custom_headers;
    };

    explicit Client(const Config& config = Config());
    ~Client();

    // Resource accessors
    resources::Messages& messages();
    resources::Completions& completions();
    resources::Models& models();

    // Internal use - get configured HTTP client
    http::HttpClient& http_client();
    const utils::RetryPolicy& retry_policy() const;
    const std::string& base_url() const;

private:
    void initialize_auth();
    void setup_default_headers();

    Config config_;
    std::unique_ptr<http::HttpClient> http_client_;
    std::unique_ptr<utils::RetryPolicy> retry_policy_;
    std::map<std::string, std::string> default_headers_;

    // Resources (lazy initialized)
    std::unique_ptr<resources::Messages> messages_;
    std::unique_ptr<resources::Completions> completions_;
    std::unique_ptr<resources::Models> models_;
};

} // namespace anthropic
