#pragma once

#include <string>
#include <vector>
#include <variant>
#include <optional>
#include <rapidjson/document.h>

namespace anthropic {
namespace types {

// Text block
struct TextBlock {
    std::string type = "text";
    std::string text;
    // TODO: citations support
};

// Thinking block (extended thinking/reasoning)
struct ThinkingBlock {
    std::string type = "thinking";
    std::string thinking;
    std::string signature;
};

// Redacted thinking block
struct RedactedThinkingBlock {
    std::string type = "redacted_thinking";
    std::string redacted_thinking;
};

// Tool use block
struct ToolUseBlock {
    std::string type = "tool_use";
    std::string id;
    std::string name;
    rapidjson::Document input;  // Tool input as JSON
};

// Server tool use block
struct ServerToolUseBlock {
    std::string type = "server_tool_use";
    std::string id;
    std::string name;
    rapidjson::Document input;
};

// Web search tool result block
struct WebSearchToolResultBlock {
    std::string type = "web_search_tool_result";
    std::string query;
    std::vector<std::string> results;  // Simplified - full structure has more fields
};

// Discriminated union of all content block types
using ContentBlock = std::variant<
    TextBlock,
    ThinkingBlock,
    RedactedThinkingBlock,
    ToolUseBlock,
    ServerToolUseBlock,
    WebSearchToolResultBlock
>;

// Helper to get the type string from a content block
std::string get_content_block_type(const ContentBlock& block);

} // namespace types
} // namespace anthropic
