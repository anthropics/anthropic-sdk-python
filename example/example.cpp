#include <anthropic/client.hpp>
#include <anthropic/resources/messages.hpp>
#include <anthropic/types/errors.hpp>
#include <iostream>
#include <string>

int main() {
    try {
        // Create client (will auto-load ANTHROPIC_API_KEY from environment)
        anthropic::Client client;

        // Build message request
        anthropic::resources::MessageCreateParams params;
        params.model = "claude-sonnet-4-5-20250929";
        params.max_tokens = 1024;

        // Add user message
        anthropic::resources::types::MessageParam user_msg;
        user_msg.role = "user";
        user_msg.content = "Hello! What can you tell me about C++ programming?";
        params.messages.push_back(user_msg);

        // Optional parameters
        params.temperature = 0.7;

        std::cout << "Sending message to Claude..." << std::endl;

        // Create message
        anthropic::types::Message response = client.messages().create(params);

        // Print response
        std::cout << "\nResponse from Claude:" << std::endl;
        std::cout << "Model: " << response.model << std::endl;
        std::cout << "Stop Reason: " << anthropic::types::stop_reason_to_string(*response.stop_reason) << std::endl;
        std::cout << "\nContent:" << std::endl;

        for (const auto& block : response.content) {
            if (std::holds_alternative<anthropic::types::TextBlock>(block)) {
                const auto& text_block = std::get<anthropic::types::TextBlock>(block);
                std::cout << text_block.text << std::endl;
            }
        }

        std::cout << "\nUsage:" << std::endl;
        std::cout << "  Input tokens: " << response.usage.input_tokens << std::endl;
        std::cout << "  Output tokens: " << response.usage.output_tokens << std::endl;

        return 0;

    }
    catch (const anthropic::AuthenticationError& e) {
        std::cerr << "Authentication error: " << e.what() << std::endl;
        std::cerr << "Make sure ANTHROPIC_API_KEY environment variable is set." << std::endl;
        return 1;
    }
    catch (const anthropic::APIError& e) {
        std::cerr << "API error (status " << e.status_code() << "): " << e.what() << std::endl;
        return 1;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
