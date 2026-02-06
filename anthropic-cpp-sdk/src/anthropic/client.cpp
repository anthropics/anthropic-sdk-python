#include "anthropic/client.hpp"
#include "anthropic/resources/messages.hpp"
#include "anthropic/types/errors.hpp"
#include "anthropic/utils/env.hpp"

namespace anthropic {

Client::Client(const Config& config)
    : config_(config)
    , http_client_(http::create_http_client())
    , retry_policy_(std::make_unique<utils::RetryPolicy>()) {

    initialize_auth();
    setup_default_headers();
}

Client::~Client() = default;

void Client::initialize_auth() {
    // Auto-load from environment if not provided
    if (!config_.api_key.has_value()) {
        config_.api_key = utils::get_env("ANTHROPIC_API_KEY");
    }

    if (!config_.auth_token.has_value()) {
        config_.auth_token = utils::get_env("ANTHROPIC_AUTH_TOKEN");
    }

    // Validate that at least one auth method is provided
    if (!config_.api_key.has_value() && !config_.auth_token.has_value()) {
        throw AuthenticationError(
            "Could not resolve authentication method. "
            "Expected either api_key or auth_token to be set, "
            "or ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN environment variable."
        );
    }
}

void Client::setup_default_headers() {
    // Standard headers
    default_headers_["Accept"] = "application/json";
    default_headers_["Content-Type"] = "application/json";
    default_headers_["User-Agent"] = "Anthropic-CPP-SDK/1.0";
    default_headers_["anthropic-version"] = "2023-06-01";

    // Authentication headers
    if (config_.api_key.has_value()) {
        default_headers_["X-Api-Key"] = *config_.api_key;
    }

    if (config_.auth_token.has_value()) {
        default_headers_["Authorization"] = "Bearer " + *config_.auth_token;
    }

    // Custom headers (override defaults)
    for (const auto& [key, value] : config_.custom_headers) {
        default_headers_[key] = value;
    }

    http_client_->set_default_headers(default_headers_);
}

resources::Messages& Client::messages() {
    if (!messages_) {
        messages_ = std::make_unique<resources::Messages>(*this);
    }
    return *messages_;
}

resources::Completions& Client::completions() {
    if (!completions_) {
        completions_ = std::make_unique<resources::Completions>(*this);
    }
    return *completions_;
}

resources::Models& Client::models() {
    if (!models_) {
        models_ = std::make_unique<resources::Models>(*this);
    }
    return *models_;
}

http::HttpClient& Client::http_client() {
    return *http_client_;
}

const utils::RetryPolicy& Client::retry_policy() const {
    return *retry_policy_;
}

const std::string& Client::base_url() const {
    return config_.base_url;
}

} // namespace anthropic
