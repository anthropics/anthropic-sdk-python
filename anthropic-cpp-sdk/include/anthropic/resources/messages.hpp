#pragma once

#include "../types/message.hpp"
#include <string>
#include <vector>
#include <optional>
#include <memory>

namespace anthropic {

class Client;

namespace resources {

// Message creation request parameters
struct MessageCreateParams {
    std::string model;
    int max_tokens;
    std::vector<types::MessageParam> messages;

    // Optional parameters
    std::optional<std::string> system;
    std::optional<double> temperature;
    std::optional<double> top_p;
    std::optional<int> top_k;
    std::optional<std::vector<std::string>> stop_sequences;
    bool stream = false;

    // TODO: Add tools, tool_choice, thinking, output_config, metadata, etc.
};

// Simplified message param for input
namespace types {
struct MessageParam {
    std::string role;  // "user" or "assistant"
    std::string content;  // Simplified - full version supports content blocks
};
}

class Messages {
public:
    explicit Messages(Client& client);

    // Create a message (synchronous, non-streaming)
    anthropic::types::Message create(const MessageCreateParams& params);

    // Create a streaming message
    // MessageStream stream(const MessageCreateParams& params);

    // Count tokens for a message
    // MessageTokensCount count_tokens(const MessageCountTokensParams& params);

private:
    Client& client_;

    std::string build_request_body(const MessageCreateParams& params);
    anthropic::types::Message parse_response(const std::string& response_body);
};

// Stub classes for completeness
class Completions {
public:
    explicit Completions(Client& client) : client_(client) {}
private:
    Client& client_;
};

class Models {
public:
    explicit Models(Client& client) : client_(client) {}
private:
    Client& client_;
};

} // namespace resources
} // namespace anthropic
