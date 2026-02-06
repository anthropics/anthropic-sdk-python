#include "anthropic/utils/env.hpp"
#include <cstdlib>

namespace anthropic {
namespace utils {

std::optional<std::string> get_env(const std::string& name) {
    const char* value = std::getenv(name.c_str());
    if (value == nullptr) {
        return std::nullopt;
    }
    return std::string(value);
}

} // namespace utils
} // namespace anthropic
