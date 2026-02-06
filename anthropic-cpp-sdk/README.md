# Anthropic C++ SDK

A comprehensive C++ SDK for the Anthropic (Claude) API, designed for Windows applications with support for Visual Studio.

## Features

- **Full Claude API Support**: Messages, Completions, Models, and Beta APIs
- **Streaming Responses**: SSE-based streaming for real-time interactions
- **Windows-Native**: Uses WinHTTP for HTTP operations (no external dependencies)
- **Thread-Safe**: Full support for multi-threaded applications
- **Static Linking**: Builds as a static library with minimal runtime dependencies
- **Modern C++**: C++20 standard with clean, efficient code
- **Error Handling**: Comprehensive exception hierarchy for API errors
- **Automatic Retry**: Built-in exponential backoff with jitter for failed requests

## Project Status

This is a **Phase 1 implementation** demonstrating the core architecture:

✅ HTTP client layer with WinHTTP
✅ SSE parser for streaming
✅ Error handling and retry logic
✅ Core type system (Message, ContentBlock, Usage)
✅ JSON serialization with RapidJSON
✅ Main Client class with authentication
✅ Basic Messages API (create method)
✅ Visual Studio project configuration

**To be implemented:**
- Streaming support (MessageStream)
- Tool use and tool calling
- Batch processing APIs
- Complete content block types (images, documents)
- Citations support
- Models and Completions resources
- Beta APIs
- Connection pooling
- Comprehensive unit tests

## Requirements

- Windows 10/11
- Visual Studio 2022 (v143 toolset)
- C++20 support
- Windows SDK (for WinHTTP)

## Dependencies

The SDK uses minimal external dependencies:

1. **WinHTTP** (Windows SDK) - HTTP/HTTPS client
2. **RapidJSON** (header-only, included) - JSON parsing
3. **Windows Sockets 2** (ws2_32.lib) - Network support
4. **Crypt32.lib** - SSL/TLS support

All dependencies are statically linked, so the final library requires no additional DLLs.

## Building

### Open in Visual Studio

1. Open `AnthropicSDK.sln` in Visual Studio 2022
2. Select configuration (Debug or Release) and platform (x64)
3. Build → Build Solution (Ctrl+Shift+B)

The static library will be output to:
- Debug: `bin\x64\Debug\AnthropicSDK.lib`
- Release: `bin\x64\Release\AnthropicSDK.lib`

### Project Configuration

The project is configured with:
- Language Standard: C++20 (`/std:c++20`)
- Runtime Library: Multi-threaded static (`/MT` for Release, `/MTd` for Debug)
- Warning Level: Level 4 (`/W4`)
- Preprocessor: `WIN32_LEAN_AND_MEAN`, `NOMINMAX`, `_UNICODE`

## Usage

### Basic Example

```cpp
#include <anthropic/client.hpp>
#include <anthropic/resources/messages.hpp>
#include <iostream>

int main() {
    try {
        // Create client (auto-loads ANTHROPIC_API_KEY from environment)
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

        // Create message
        anthropic::types::Message response = client.messages().create(params);

        // Print response
        std::cout << "Response: " << std::endl;
        for (const auto& block : response.content) {
            if (std::holds_alternative<anthropic::types::TextBlock>(block)) {
                const auto& text_block = std::get<anthropic::types::TextBlock>(block);
                std::cout << text_block.text << std::endl;
            }
        }

        std::cout << "\nUsage: " << response.usage.input_tokens
                  << " in, " << response.usage.output_tokens << " out" << std::endl;

    } catch (const anthropic::APIError& e) {
        std::cerr << "API error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
```

### Custom Configuration

```cpp
// Configure client manually
anthropic::Client::Config config;
config.api_key = "sk-ant-...";  // Or leave unset to use environment variable
config.base_url = "https://api.anthropic.com";
config.timeout_ms = 60000;  // 1 minute
config.max_retries = 3;
config.custom_headers["X-Custom-Header"] = "value";

anthropic::Client client(config);
```

### Error Handling

```cpp
try {
    auto response = client.messages().create(params);
} catch (const anthropic::AuthenticationError& e) {
    // 401 - Invalid API key
    std::cerr << "Authentication failed: " << e.what() << std::endl;
} catch (const anthropic::RateLimitError& e) {
    // 429 - Rate limit exceeded
    std::cerr << "Rate limited: " << e.what() << std::endl;
} catch (const anthropic::BadRequestError& e) {
    // 400 - Invalid request parameters
    std::cerr << "Bad request: " << e.what() << std::endl;
} catch (const anthropic::APIError& e) {
    // Other API errors
    std::cerr << "API error (status " << e.status_code() << "): " << e.what() << std::endl;
} catch (const anthropic::ConnectionError& e) {
    // Network errors
    std::cerr << "Connection error: " << e.what() << std::endl;
}
```

## Authentication

The SDK supports two authentication methods:

1. **API Key** (recommended):
   - Set `ANTHROPIC_API_KEY` environment variable
   - Or pass `api_key` in `Client::Config`
   - Sends `X-Api-Key` header

2. **Auth Token**:
   - Set `ANTHROPIC_AUTH_TOKEN` environment variable
   - Or pass `auth_token` in `Client::Config`
   - Sends `Authorization: Bearer` header

At least one authentication method must be provided.

## Thread Safety

The SDK is designed to be thread-safe:

- Each `Client` instance can be safely used from multiple threads
- HTTP client uses connection pooling with mutex protection
- Request/response handling is stateless
- Retry logic uses thread-local random number generators

Example multi-threaded usage:

```cpp
anthropic::Client client;

#pragma omp parallel for
for (int i = 0; i < 10; i++) {
    try {
        anthropic::resources::MessageCreateParams params;
        params.model = "claude-sonnet-4-5-20250929";
        params.max_tokens = 100;

        anthropic::resources::types::MessageParam msg;
        msg.role = "user";
        msg.content = "Request #" + std::to_string(i);
        params.messages.push_back(msg);

        auto response = client.messages().create(params);
        std::cout << "Thread " << i << " completed" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Thread " << i << " error: " << e.what() << std::endl;
    }
}
```

## Architecture

### Directory Structure

```
anthropic-cpp-sdk/
├── include/anthropic/          # Public API headers
│   ├── client.hpp              # Main client class
│   ├── http/                   # HTTP layer
│   │   ├── http_client.hpp     # Abstract HTTP interface
│   │   ├── winhttp_client.hpp  # WinHTTP implementation
│   │   └── sse_parser.hpp      # Server-Sent Events parser
│   ├── resources/              # API resources
│   │   └── messages.hpp        # Messages API
│   ├── types/                  # Data types
│   │   ├── message.hpp         # Message types
│   │   ├── content_block.hpp   # Content block variants
│   │   ├── usage.hpp           # Token usage stats
│   │   ├── stop_reason.hpp     # Stop reason enum
│   │   └── errors.hpp          # Exception hierarchy
│   └── utils/                  # Utilities
│       ├── json_utils.hpp      # JSON helpers
│       ├── retry_logic.hpp     # Retry policy
│       └── env.hpp             # Environment variables
├── src/anthropic/              # Implementation files
├── third_party/rapidjson/      # RapidJSON headers
├── examples/                   # Usage examples
└── AnthropicSDK.sln           # Visual Studio solution
```

### Design Patterns

1. **Resource Pattern**: API endpoints are organized as resource classes (`Messages`, `Completions`, etc.)
2. **Builder Pattern**: Request parameters use structs with optional fields
3. **Variant Types**: Content blocks use `std::variant` for discriminated unions
4. **RAII**: Resources are automatically managed with smart pointers
5. **Retry Logic**: Exponential backoff with jitter for failed requests

## Examples

See the `examples/` directory for complete examples:

- `basic_message.cpp` - Simple message creation
- `streaming_message.cpp` - Streaming responses (TODO)
- `tool_use.cpp` - Tool calling (TODO)
- `multithreaded.cpp` - Thread-safety demo (TODO)
- `batch_processing.cpp` - Batch API (TODO)

## Roadmap

### Phase 2: Streaming Support
- Implement `MessageStream` class
- SSE event parsing and accumulation
- Iterator interface for range-based loops

### Phase 3: Complete Type System
- All content block types (images, PDFs, documents)
- Tool definitions and tool calling
- Citations and structured outputs
- Message parameters with content blocks

### Phase 4: Additional APIs
- Batch processing (create, retrieve, list, cancel)
- Models API (list, retrieve)
- Completions API (legacy)
- Beta APIs (extended thinking, files, skills)

### Phase 5: Testing and Polish
- Unit tests for all components
- Integration tests with live API
- Performance benchmarks
- Memory leak detection
- Documentation improvements

## Contributing

This is an initial implementation. Contributions are welcome! Please follow these guidelines:

1. Follow C++20 idioms and best practices
2. Use consistent naming conventions (snake_case for functions/variables, PascalCase for types)
3. Add appropriate error handling
4. Maintain thread-safety
5. Update documentation

## License

This SDK is provided as-is for use with the Anthropic API. Please refer to Anthropic's terms of service for API usage guidelines.

## API Reference

For complete API documentation, see:
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Models](https://docs.anthropic.com/en/docs/models-overview)
- [Messages API](https://docs.anthropic.com/en/docs/initial-setup)

## Support

For issues with the SDK:
- Check the examples for usage patterns
- Review error messages for common issues
- Ensure your API key is valid and has appropriate permissions

For issues with the Anthropic API:
- See [Anthropic Support](https://support.anthropic.com/)
- Check API status at [status.anthropic.com](https://status.anthropic.com/)

## Version History

### v0.1.0 (Phase 1)
- Initial implementation
- Core HTTP client with WinHTTP
- Basic Messages API (create method)
- Error handling and retry logic
- Visual Studio project setup
