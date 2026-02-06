#include "anthropic/types/content_block.hpp"

namespace anthropic {
namespace types {

std::string get_content_block_type(const ContentBlock& block) {
    return std::visit([](const auto& b) { return b.type; }, block);
}

} // namespace types
} // namespace anthropic
