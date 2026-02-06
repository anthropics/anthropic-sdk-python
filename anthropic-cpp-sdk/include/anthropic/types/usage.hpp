#pragma once

#include <optional>
#include <string>

namespace anthropic {
namespace types {

struct Usage {
    int input_tokens = 0;
    int output_tokens = 0;
    std::optional<int> cache_creation_input_tokens;
    std::optional<int> cache_read_input_tokens;
    std::optional<std::string> inference_geo;
    std::optional<std::string> service_tier;  // "standard", "priority", "batch"
};

} // namespace types
} // namespace anthropic
