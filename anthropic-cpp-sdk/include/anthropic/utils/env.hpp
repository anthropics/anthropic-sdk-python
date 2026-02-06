#pragma once

#include <string>
#include <optional>

namespace anthropic {
namespace utils {

// Get environment variable value
std::optional<std::string> get_env(const std::string& name);

} // namespace utils
} // namespace anthropic
