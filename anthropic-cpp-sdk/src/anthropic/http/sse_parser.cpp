#include "anthropic/http/sse_parser.hpp"
#include <sstream>

namespace anthropic {
namespace http {

SSEParser::SSEParser() {
    reset();
}

void SSEParser::reset() {
    buffer_.clear();
    current_event_.clear();
    current_data_.clear();
    current_id_.reset();
    current_retry_.reset();
}

void SSEParser::parse(const std::string& chunk, SSECallback callback) {
    buffer_ += chunk;

    // Process complete lines
    size_t pos = 0;
    while ((pos = buffer_.find('\n')) != std::string::npos) {
        std::string line = buffer_.substr(0, pos);
        buffer_ = buffer_.substr(pos + 1);

        // Remove trailing \r if present
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }

        process_line(line, callback);
    }
}

void SSEParser::process_line(const std::string& line, SSECallback& callback) {
    // Empty line dispatches the event
    if (line.empty()) {
        dispatch_event(callback);
        return;
    }

    // Lines starting with : are comments
    if (line[0] == ':') {
        return;
    }

    // Parse field
    size_t colon = line.find(':');
    std::string field;
    std::string value;

    if (colon == std::string::npos) {
        field = line;
        value = "";
    } else {
        field = line.substr(0, colon);
        value = line.substr(colon + 1);

        // Remove leading space from value if present
        if (!value.empty() && value[0] == ' ') {
            value = value.substr(1);
        }
    }

    // Process field
    if (field == "event") {
        current_event_ = value;
    } else if (field == "data") {
        // Accumulate data (may be multiline)
        if (!current_data_.empty()) {
            current_data_ += '\n';
        }
        current_data_ += value;
    } else if (field == "id") {
        // ID field must not contain null bytes
        if (value.find('\0') == std::string::npos) {
            current_id_ = value;
        }
    } else if (field == "retry") {
        // Retry field must be integer
        try {
            current_retry_ = std::stoi(value);
        } catch (...) {
            // Ignore invalid retry values
        }
    }
    // Unknown fields are ignored
}

void SSEParser::dispatch_event(SSECallback& callback) {
    // Don't dispatch if no data
    if (current_data_.empty()) {
        current_event_.clear();
        current_id_.reset();
        current_retry_.reset();
        return;
    }

    SSEEvent event;
    event.event_type = current_event_.empty() ? "message" : current_event_;
    event.data = current_data_;
    event.id = current_id_;
    event.retry = current_retry_;

    // Reset state for next event
    current_event_.clear();
    current_data_.clear();
    // Note: id and retry persist across events until changed

    // Call callback
    callback(event);
}

} // namespace http
} // namespace anthropic
