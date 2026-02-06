#pragma once

#include <string>
#include <functional>
#include <optional>

namespace anthropic {
namespace http {

struct SSEEvent {
    std::string event_type;  // Empty means "message"
    std::string data;
    std::optional<std::string> id;
    std::optional<int> retry;
};

// Callback for parsed SSE events (returns true to continue, false to stop)
using SSECallback = std::function<bool(const SSEEvent& event)>;

// Server-Sent Events parser
// Reference: https://html.spec.whatwg.org/multipage/server-sent-events.html
class SSEParser {
public:
    SSEParser();

    // Parse a chunk of SSE data and call callback for each complete event
    void parse(const std::string& chunk, SSECallback callback);

    // Reset parser state
    void reset();

private:
    void process_line(const std::string& line, SSECallback& callback);
    void dispatch_event(SSECallback& callback);

    std::string buffer_;           // Accumulated data
    std::string current_event_;    // Current event type
    std::string current_data_;     // Current data (may be multiline)
    std::optional<std::string> current_id_;
    std::optional<int> current_retry_;
};

} // namespace http
} // namespace anthropic
