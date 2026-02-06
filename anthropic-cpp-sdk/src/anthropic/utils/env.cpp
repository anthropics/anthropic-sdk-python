#include "anthropic/utils/env.hpp"
#include <cstdlib>
#include <memory>

namespace anthropic {
namespace utils {

std::optional<std::string> get_env(const std::string& name) {
    char* value = nullptr;
    size_t size = 0;
    if (_dupenv_s(&value, &size, name.c_str()) == 0 && value != nullptr) {
        std::string result(value);
        free(value);
        return result;
    }
    return std::nullopt;
}

} // namespace utils
} // namespace anthropic
