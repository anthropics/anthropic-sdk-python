#pragma once

#include <chrono>
#include <random>
#include <functional>
#include <optional>

namespace anthropic {
namespace utils {

struct RetryConfig {
    int max_retries = 2;
    std::chrono::milliseconds initial_delay{500};
    std::chrono::milliseconds max_delay{8000};
    double backoff_factor = 2.0;
    double jitter_factor = 0.25;  // ±25% jitter
};

class RetryPolicy {
public:
    explicit RetryPolicy(const RetryConfig& config = RetryConfig());

    // Determine if a status code should be retried
    bool should_retry(int status_code, int attempt) const;

    // Calculate delay for next retry with exponential backoff and jitter
    std::chrono::milliseconds calculate_delay(int attempt) const;

    // Parse Retry-After header (returns delay in milliseconds, or nullopt if not present/invalid)
    static std::optional<std::chrono::milliseconds> parse_retry_after(const std::string& retry_after_value);

private:
    RetryConfig config_;
    mutable std::mt19937 rng_;
};

// Helper function to execute a request with retry logic
template<typename Func>
auto execute_with_retry(const RetryPolicy& policy, Func&& func) -> decltype(func()) {
    int attempt = 0;

    while (true) {
        try {
            auto result = func();
            return result;
        } catch (const std::exception&) {
            // Check if we should retry
            if (attempt >= policy.max_retries) {
                throw;  // Re-throw the exception
            }

            // Calculate delay
            auto delay = policy.calculate_delay(attempt);
            std::this_thread::sleep_for(delay);

            attempt++;
        }
    }
}

} // namespace utils
} // namespace anthropic
