# C++ SDK Implementation Plan for Anthropic API

## Context

The Anthropic Python SDK (located at `C:\SOURCES\anthropic-sdk`) provides a comprehensive interface to Claude's API with support for message creation, streaming responses, tool use, batch processing, and more. This plan outlines the translation of this SDK to C++ for use in Windows applications.

**Why this is needed:**
- Enable C++ projects to integrate Claude API natively
- Provide statically linkable library with no runtime dependencies
- Support multi-threaded Windows applications
- Match Python SDK feature parity

**User Requirements:**
- **Platform:** Windows-specific (use Windows-native APIs where beneficial)
- **Linking:** Statically linkable (minimal external dependencies)
- **Thread-Safety:** Full support for multi-threaded usage
- **Language Standard:** C++20
- **Build System:** Visual Studio projects
- **API Style:** Object-oriented with clean, efficient code
- **Scope:** Full SDK including Messages, Completions, Models, Beta APIs, streaming, and batch processing

## Recommended Approach

### Technology Stack

**HTTP Library: WinHTTP**
- Windows-native, no external dependencies (statically links via `winhttp.lib`)
- Excellent SSL/TLS support built-in
- Connection pooling and keep-alive support
- Synchronous and asynchronous capabilities
- Located in Windows SDK: `#include <winhttp.h>`

**JSON Library: RapidJSON**
- Header-only library with SAX and DOM parsers
- Extremely fast parsing and serialization performance
- Zero-copy string optimization with allocators
- Supports in-situ parsing for minimal memory overhead
- No external dependencies beyond C++ standard library
- Download from: https://github.com/Tencent/rapidjson (include/rapidjson directory)
- Includes: `rapidjson/document.h`, `rapidjson/writer.h`, `rapidjson/stringbuffer.h`, `rapidjson/error/en.h`

**Threading: C++ Standard Library**
- `std::mutex` for thread-safety
- `std::shared_ptr` for automatic memory management
- Connection pooling for HTTP session reuse
- `std::atomic` for lock-free counters

### Architecture Overview

```
anthropic-cpp-sdk/
├── include/anthropic/          # Public headers
│   ├── client.hpp              # Main Anthropic client
│   ├── http/                   # HTTP abstractions
│   ├── resources/              # API resources (messages, models, etc.)
│   ├── types/                  # Data models and types
│   ├── streaming/              # Streaming support
│   └── utils/                  # Utilities
├── src/anthropic/              # Implementation files
│   ├── client.cpp
│   ├── http/
│   ├── resources/
│   ├── types/
│   ├── streaming/
│   └── utils/
├── third_party/
│   └── rapidjson/              # RapidJSON library headers
├── examples/                   # Usage examples
└── AnthropicSDK.sln           # Visual Studio solution
```

## Implementation Steps

### Phase 1: Foundation (Core Infrastructure)

**1.1 Setup Project Structure**
- Create Visual Studio solution (`AnthropicSDK.sln`)
- Create static library project (`AnthropicSDK.vcxproj`)
- Setup include paths and configurations (Debug/Release, x64)
- Download and integrate RapidJSON headers from https://github.com/Tencent/rapidjson
  - Copy `include/rapidjson` directory to `third_party/rapidjson`
  - Add `$(ProjectDir)third_party` to include directories
- Link against `winhttp.lib` and `ws2_32.lib`

**1.2 HTTP Client Layer (`anthropic/http/`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\_base_client.py`

Create:
- `http_client.hpp/cpp` - Abstract HTTP interface with Request/Response structs
- `winhttp_client.hpp/cpp` - WinHTTP implementation with:
  - Connection pooling (reuse HINTERNET handles)
  - SSL/TLS configuration
  - Timeout handling (connect/receive)
  - Request building (URL, headers, body)
  - Response parsing (status, headers, body)
- `connection_pool.hpp/cpp` - Thread-safe connection pool with `std::mutex`
- `sse_parser.hpp/cpp` - Server-Sent Events parser for streaming
  - Parse SSE format: `event:`, `data:`, `id:`, `retry:`
  - Handle multiline data with buffer accumulation
  - Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\_streaming.py` lines 299-401

**1.3 Error Handling (`anthropic/types/errors.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\_exceptions.py`

Create exception hierarchy:
- `AnthropicError` (base class inheriting from `std::runtime_error`)
- `APIError` (with status_code and response body)
- Specific errors: `BadRequestError` (400), `AuthenticationError` (401), `NotFoundError` (404), `RateLimitError` (429), `InternalServerError` (500+), etc.
- `ConnectionError`, `TimeoutError` for network issues

**1.4 Retry Logic (`anthropic/utils/retry_logic.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\_base_client.py` lines 792-832

Implement:
- `RetryPolicy` class with configurable max_retries (default: 2)
- Exponential backoff: initial_delay=500ms, max_delay=8s, factor=2.0
- Jitter calculation (±25% randomness)
- Retry decision based on status codes (408, 409, 429, 5xx)
- Support for `Retry-After` header parsing

### Phase 2: Type System (Data Models)

**2.1 Core Message Types (`anthropic/types/`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\message.py`

Create:
- `message.hpp/cpp` - `Message` struct with:
  - `std::string id, model, role, type`
  - `std::vector<ContentBlock> content`
  - `std::optional<StopReason> stop_reason`
  - `Usage usage` (input_tokens, output_tokens, cache stats)
- `stop_reason.hpp` - Enum: `EndTurn`, `MaxTokens`, `StopSequence`, `ToolUse`, `PauseTurn`, `Refusal`
- `usage.hpp` - Usage statistics struct

**2.2 Content Blocks (`anthropic/types/content_block.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\content_block.py`

Implement discriminated union using `std::variant`:
```cpp
using ContentBlock = std::variant<
    TextBlock,              // type: "text"
    ThinkingBlock,          // type: "thinking"
    ToolUseBlock,          // type: "tool_use"
    ServerToolUseBlock,    // type: "server_tool_use"
    RedactedThinkingBlock, // type: "redacted_thinking"
    WebSearchToolResultBlock // type: "web_search_tool_result"
>;
```

Each block type is a struct with:
- `std::string type` (discriminator)
- Type-specific fields (e.g., `text`, `thinking`, `name`, `input`, etc.)

**2.3 Message Parameters (`anthropic/types/message_param.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\message_param.py`

Create:
- `MessageParam` struct with `role` and `content`
- Input content block variants (TextBlockParam, ImageBlockParam, ToolUseBlockParam, ToolResultBlockParam, etc.)
- Source parameters for images/documents (Base64ImageSource, URLImageSource, Base64PDFSource, etc.)

**2.4 Tool Types (`anthropic/types/tool.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\tool_param.py`

Create:
- `Tool` struct with `name`, `description`, `input_schema` (JSON)
- `ToolChoice` as `std::variant` of ToolChoiceAuto, ToolChoiceAny, ToolChoiceTool, ToolChoiceNone
- JSON schema representation using `rapidjson::Value` and `rapidjson::Document`

**2.5 Citations (`anthropic/types/citation.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\text_citation.py`

Implement citation variants:
- `CitationCharLocation` (char-level)
- `CitationPageLocation` (page-level)
- `CitationContentBlockLocation` (block-level)
- `CitationsWebSearchResultLocation` (web search)

**2.6 JSON Serialization (`anthropic/utils/json_utils.hpp/cpp`)**

Implement serialization/deserialization functions for all types using RapidJSON:
- Create `Serialize(const T& obj, rapidjson::Writer<>&)` functions for each type
- Create `Deserialize(const rapidjson::Value&, T& obj)` functions for parsing
- Use `rapidjson::Document` for root-level parsing with `MemoryPoolAllocator`
- Handle discriminated unions by checking "type" field in JSON
- Support optional fields with `std::optional` - skip if not present, use `SetNull()` if null
- Handle arrays with `std::vector` using RapidJSON array iterators
- Use `rapidjson::StringBuffer` with `rapidjson::Writer` for efficient serialization
- Implement helper functions:
  - `JsonToString(const rapidjson::Value&)` - Convert JSON value to string
  - `StringToJson(const std::string&)` - Parse string to Document
  - `GetOptionalString(const rapidjson::Value&, const char* key)` - Safe optional access
  - `GetOptionalInt(const rapidjson::Value&, const char* key)` - Safe optional access

### Phase 3: Streaming Support

**3.1 Stream Events (`anthropic/types/stream_events.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\raw_message_stream_event.py`

Create event types:
- `MessageStartEvent` - Initial message with metadata
- `MessageDeltaEvent` - Updates to stop_reason, usage
- `MessageStopEvent` - End of message
- `ContentBlockStartEvent` - New content block begins
- `ContentBlockDeltaEvent` - Incremental content updates (text, JSON, thinking)
- `ContentBlockStopEvent` - Content block complete

Use `std::variant` for discriminated union:
```cpp
using StreamEvent = std::variant<
    MessageStartEvent,
    MessageDeltaEvent,
    MessageStopEvent,
    ContentBlockStartEvent,
    ContentBlockDeltaEvent,
    ContentBlockStopEvent
>;
```

**3.2 Stream Implementation (`anthropic/streaming/`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\_streaming.py`

Create:
- `stream.hpp/cpp` - Base streaming interface
- `message_stream.hpp/cpp` - Message streaming with:
  - Iterator interface for range-based for loops
  - SSE parsing using `SSEParser`
  - Event accumulation for `get_final_message()`
  - RAII resource management (auto-close HTTP connection)
- `stream_manager.hpp/cpp` - Manages stream lifecycle

**3.3 Delta Types (`anthropic/types/delta.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\types\raw_content_block_delta.py`

Create delta variants for incremental updates:
- `TextDelta` - Partial text chunks
- `InputJSONDelta` - Partial JSON strings for tool inputs
- `ThinkingDelta` - Partial thinking content
- `CitationsDelta` - Citation updates
- `SignatureDelta` - Signature updates

### Phase 4: API Resources

**4.1 Main Client (`anthropic/client.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\_client.py`

Implement:
- `Client` class with configuration:
  - `api_key` (from constructor or `ANTHROPIC_API_KEY` env var)
  - `auth_token` (alternative auth via Bearer token)
  - `base_url` (default: "https://api.anthropic.com")
  - `timeout` (default: 10 minutes)
  - `max_retries` (default: 2)
  - `custom_headers` (user-provided headers)
- Resource accessor methods:
  - `messages()` returns `Messages&`
  - `completions()` returns `Completions&`
  - `models()` returns `Models&`
  - `beta()` returns `Beta&`
- Authentication headers:
  - `X-Api-Key: <api_key>` for API key auth
  - `Authorization: Bearer <token>` for token auth
- Additional headers:
  - `anthropic-version: 2023-06-01`
  - `content-type: application/json`
  - User-Agent with SDK version

**4.2 Messages Resource (`anthropic/resources/messages.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\resources\messages\messages.py`

Implement:
- `Messages` class with methods:
  - `create(MessageCreateRequest)` -> `Message` (synchronous)
  - `stream(MessageCreateRequest)` -> `MessageStream` (streaming)
  - `count_tokens(CountTokensRequest)` -> `MessageTokensCount`
- `MessageCreateRequest` builder with fluent interface:
  - Required: `model`, `max_tokens`, `messages`
  - Optional: `system`, `temperature`, `top_p`, `top_k`, `stop_sequences`, `tools`, `tool_choice`, `thinking`, `output_config`, `metadata`, `stream`, `inference_geo`, `service_tier`
  - Method chaining: `.add_message()`, `.system()`, `.temperature()`, `.add_tool()`, etc.
- Batches sub-resource: `messages().batches()`

**4.3 Batches Sub-resource (`anthropic/resources/batches.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\resources\messages\batches.py`

Implement:
- `Batches` class with methods:
  - `create(MessageBatchCreateRequest)` -> `MessageBatch`
  - `retrieve(std::string id)` -> `MessageBatch`
  - `list(BatchListParams)` -> `Page<MessageBatch>`
  - `cancel(std::string id)` -> `MessageBatch`
  - `delete(std::string id)` -> `void`
  - `results(std::string id)` -> `std::vector<MessageBatchIndividualResponse>`
- Batch types:
  - `MessageBatch` - Batch metadata and status
  - `MessageBatchResult` - Variant: succeeded/errored/canceled/expired
  - `MessageBatchIndividualResponse` - Single request result with custom_id

**4.4 Completions Resource (`anthropic/resources/completions.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\resources\completions.py`

Implement legacy Completions API:
- `Completions` class with `create(CompletionCreateRequest)` -> `Completion`
- Parameters: `model`, `max_tokens_to_sample`, `prompt`, `temperature`, `top_p`, `top_k`, `stop_sequences`, `stream`
- Note: This is a legacy API, users should prefer Messages API

**4.5 Models Resource (`anthropic/resources/models.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\resources\models.py`

Implement:
- `Models` class with methods:
  - `retrieve(std::string model_id)` -> `ModelInfo`
  - `list(ModelListParams)` -> `Page<ModelInfo>`
- `ModelInfo` struct with model details
- Pagination support with `Page<T>` template

**4.6 Beta Resource (`anthropic/resources/beta/beta.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\resources\beta\beta.py`

Implement beta features container:
- `Beta` class with sub-resources:
  - `messages()` -> Extended message features
  - `models()` -> Extended model information
  - `files()` -> File handling
  - `skills()` -> Skill management
- Beta features use same patterns as main API

### Phase 5: Utilities and Helpers

**5.1 Pagination (`anthropic/pagination.hpp/cpp`)**

Reference: `C:\SOURCES\anthropic-sdk\src\anthropic\pagination.py`

Create:
- `Page<T>` template class for paginated responses
- Iterator support for seamless iteration
- `has_next_page()`, `next_page()` methods
- Automatic page fetching

**5.2 Environment Variables (`anthropic/utils/env.hpp/cpp`)**

Implement:
- `get_env(std::string name)` -> `std::optional<std::string>`
- Use Windows `GetEnvironmentVariableA()` or standard `std::getenv()`

**5.3 URL Building (`anthropic/utils/url.hpp/cpp`)**

Create:
- `URLBuilder` class for constructing URLs
- Query parameter encoding
- Path joining with proper slash handling

**5.4 Thread Pool (Optional, `anthropic/utils/thread_pool.hpp/cpp`)**

For future async support:
- Thread pool for background tasks
- Not required for initial synchronous implementation

### Phase 6: Examples and Documentation

**6.1 Basic Usage Examples**

Create `examples/` directory with:
- `basic_message.cpp` - Simple message creation
- `streaming_message.cpp` - Streaming with event handling
- `tool_use.cpp` - Tool definition and usage
- `multithreaded.cpp` - Thread-safety demonstration
- `batch_processing.cpp` - Batch API usage
- `error_handling.cpp` - Exception handling patterns

**6.2 README Documentation**

Create comprehensive README with:
- Installation instructions
- Quick start guide
- API reference examples
- Thread-safety guidelines
- Build instructions for Visual Studio

## Critical Files Reference

From Python SDK (for reference during implementation):
- `C:\SOURCES\anthropic-sdk\src\anthropic\_client.py` - Client architecture pattern
- `C:\SOURCES\anthropic-sdk\src\anthropic\_base_client.py` - HTTP request handling, retry logic (lines 440-832)
- `C:\SOURCES\anthropic-sdk\src\anthropic\_streaming.py` - SSE parser implementation (lines 299-401)
- `C:\SOURCES\anthropic-sdk\src\anthropic\types\message.py` - Message structure
- `C:\SOURCES\anthropic-sdk\src\anthropic\types\content_block.py` - Content block discriminated unions
- `C:\SOURCES\anthropic-sdk\src\anthropic\types\raw_message_stream_event.py` - Stream event types
- `C:\SOURCES\anthropic-sdk\src\anthropic\resources\messages\messages.py` - Messages API methods

## Visual Studio Project Configuration

**Project Settings:**
- Configuration: Debug/Release
- Platform: x64
- C++ Language Standard: ISO C++20 Standard (/std:c++20)
- Runtime Library: Multi-threaded (/MT for Release, /MTd for Debug) - for static linking
- Output: Static library (.lib)

**Include Directories:**
- `$(ProjectDir)include`
- `$(ProjectDir)third_party`

**Preprocessor Definitions:**
- `_UNICODE` and `UNICODE` for Windows
- `WIN32_LEAN_AND_MEAN` to reduce Windows header size
- `NOMINMAX` to avoid min/max macro conflicts

**Linker Dependencies:**
- `winhttp.lib` - HTTP client
- `ws2_32.lib` - Windows sockets (for WinHTTP)
- `crypt32.lib` - Cryptography (for SSL)

**Warning Level:** Level 4 (/W4) with warnings as errors for production code

## Implementation Order

1. **Week 1: Foundation**
   - Project setup (VS solution, structure)
   - HTTP client (WinHTTP wrapper)
   - SSE parser
   - Error handling
   - Retry logic

2. **Week 2: Type System**
   - Core types (Message, ContentBlock, Usage)
   - Message parameters
   - Tool types
   - JSON serialization
   - Stream events and deltas

3. **Week 3: Core APIs**
   - Main Client class
   - Messages resource (create, stream, count_tokens)
   - Streaming implementation
   - Connection pooling

4. **Week 4: Additional APIs**
   - Batches sub-resource
   - Completions resource
   - Models resource
   - Beta resource (basic structure)

5. **Week 5: Polish and Testing**
   - Examples
   - Documentation
   - Integration testing
   - Performance optimization

## Verification Plan

**Unit Testing:**
- Test JSON serialization/deserialization for all types
- Test SSE parser with various event formats
- Test retry logic with mocked failures
- Test connection pool thread-safety

**Integration Testing:**
- Test against live Anthropic API with real API key
- Verify message creation with various parameters
- Test streaming with different models
- Test tool use end-to-end
- Test batch processing lifecycle
- Test error handling with invalid requests

**Thread-Safety Testing:**
- Spawn multiple threads making concurrent requests
- Verify no race conditions in connection pool
- Test streaming from multiple threads simultaneously

**Example Validation:**
- Build and run all examples
- Verify output matches expected behavior
- Check for memory leaks with Visual Studio debugger

**Performance Benchmarking:**
- Compare request latency with Python SDK
- Measure streaming throughput
- Profile connection pool efficiency
- Memory usage analysis

## Success Criteria

- ✅ All core APIs implemented (Messages, Completions, Models)
- ✅ Streaming support with SSE parsing
- ✅ Batch processing support
- ✅ Thread-safe implementation verified
- ✅ Static library builds successfully in Visual Studio
- ✅ All examples compile and run correctly
- ✅ Integration tests pass against live API
- ✅ No external runtime dependencies (statically linked)
- ✅ Clean, well-documented code following C++20 idioms
- ✅ Feature parity with Python SDK for core functionality

## Risks and Mitigations

**Risk:** WinHTTP API complexity
- **Mitigation:** Create thin abstraction layer, extensive testing, reference Microsoft documentation

**Risk:** JSON parsing edge cases
- **Mitigation:** Comprehensive unit tests, handle malformed responses gracefully

**Risk:** Thread-safety bugs
- **Mitigation:** Use RAII patterns, minimize shared state, thorough stress testing

**Risk:** SSE parsing correctness
- **Mitigation:** Reference Python implementation, test with various event sequences

**Risk:** Large API surface area
- **Mitigation:** Implement incrementally (Phase 1-5), focus on Messages API first for MVP
