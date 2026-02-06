#include "anthropic/utils/retry_logic.hpp"
#include <thread>
#include <ctime>
#include <regex>
#include <cmath>
#include <string>

namespace anthropic {
namespace utils {

RetryPolicy::RetryPolicy(const RetryConfig& config)
    : config_(config)
    , rng_(static_cast<unsigned int>(std::time(nullptr))) {
}

bool RetryPolicy::should_retry(int status_code, int attempt) const {
    if (attempt >= config_.max_retries) {
        return false;
    }

    // Retry on these status codes
    return status_code == 408 ||  // Request Timeout
           status_code == 409 ||  // Conflict
           status_code == 429 ||  // Too Many Requests
           status_code >= 500;    // Server errors
}

std::chrono::milliseconds RetryPolicy::calculate_delay(int attempt) const {
    // Exponential backoff: initial_delay * (backoff_factor ^ attempt)
    double delay_ms = config_.initial_delay.count() * std::pow(config_.backoff_factor, attempt);

    // Cap at max_delay
    delay_ms = std::min(delay_ms, static_cast<double>(config_.max_delay.count()));

    // Add jitter (±jitter_factor)
    std::uniform_real_distribution<double> dist(1.0 - config_.jitter_factor, 1.0 + config_.jitter_factor);
    delay_ms *= dist(rng_);

    return std::chrono::milliseconds(static_cast<long long>(delay_ms));
}

std::optional<std::chrono::milliseconds> RetryPolicy::parse_retry_after(const std::string& retry_after_value) {
    if (retry_after_value.empty()) {
        return std::nullopt;
    }

    // Try to parse as integer (seconds)
    try {
        int seconds = std::stoi(retry_after_value);
        if (seconds > 0) {
            return std::chrono::milliseconds(seconds * 1000);
        }
    } catch (...) {
        // Not an integer, might be HTTP-date format
        // For simplicity, we'll just ignore date format and use exponential backoff
    }

    return std::nullopt;
}

} // namespace utils
} // namespace anthropic
