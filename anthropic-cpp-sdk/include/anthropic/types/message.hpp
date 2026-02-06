#pragma once

#include "content_block.hpp"
#include "stop_reason.hpp"
#include "usage.hpp"
#include <string>
#include <vector>
#include <optional>

namespace anthropic {
namespace types {

struct Message {
    std::string id;
    std::string type = "message";
    std::string role = "assistant";
    std::string model;
    std::vector<ContentBlock> content;
    std::optional<StopReason> stop_reason;
    std::optional<std::string> stop_sequence;
    Usage usage;
};

} // namespace types
} // namespace anthropic
