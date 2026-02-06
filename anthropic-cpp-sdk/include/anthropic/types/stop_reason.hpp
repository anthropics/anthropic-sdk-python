#pragma once

#include <string>

namespace anthropic {
namespace types {

enum class StopReason {
    EndTurn,        // "end_turn" - model reached natural stopping point
    MaxTokens,      // "max_tokens" - exceeded token limit
    StopSequence,   // "stop_sequence" - custom stop sequence generated
    ToolUse,        // "tool_use" - model invoked tools
    PauseTurn,      // "pause_turn" - long-running turn paused
    Refusal         // "refusal" - streaming classifiers intervened
};

// Convert StopReason to string
inline std::string stop_reason_to_string(StopReason reason) {
    switch (reason) {
        case StopReason::EndTurn: return "end_turn";
        case StopReason::MaxTokens: return "max_tokens";
        case StopReason::StopSequence: return "stop_sequence";
        case StopReason::ToolUse: return "tool_use";
        case StopReason::PauseTurn: return "pause_turn";
        case StopReason::Refusal: return "refusal";
    }
    return "unknown";
}

// Parse StopReason from string
inline StopReason stop_reason_from_string(const std::string& str) {
    if (str == "end_turn") return StopReason::EndTurn;
    if (str == "max_tokens") return StopReason::MaxTokens;
    if (str == "stop_sequence") return StopReason::StopSequence;
    if (str == "tool_use") return StopReason::ToolUse;
    if (str == "pause_turn") return StopReason::PauseTurn;
    if (str == "refusal") return StopReason::Refusal;
    return StopReason::EndTurn;  // Default fallback
}

} // namespace types
} // namespace anthropic
