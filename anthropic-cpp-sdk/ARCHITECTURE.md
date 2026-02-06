# Architecture Overview

This document provides a detailed overview of the Anthropic C++ SDK architecture.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       User Application                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ #include <anthropic/client.hpp>
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      Anthropic::Client                       │
│  - Configuration (API key, timeout, retries)                 │
│  - Authentication (X-Api-Key, Bearer token)                  │
│  - Default headers setup                                     │
└──────────┬──────────────────────────┬────────────────────────┘
           │                          │
           │                          │
┌──────────▼────────┐      ┌──────────▼────────┐
│ Messages Resource │      │ Models Resource   │
│ - create()        │      │ - retrieve()      │
│ - stream()        │      │ - list()          │
│ - count_tokens()  │      └───────────────────┘
└──────────┬────────┘
           │
           │
┌──────────▼────────────────────────────────────────────────┐
│                     HTTP Client Layer                      │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ WinHTTP Client (Windows-native)                      │ │
│  │  - URL parsing                                       │ │
│  │  - Connection management                             │ │
│  │  - SSL/TLS support                                   │ │
│  │  - Request/Response handling                         │ │
│  │  - Streaming support                                 │ │
│  └──────────────────────────────────────────────────────┘ │
└───────────────────────────┬────────────────────────────────┘
                            │
                            │ HTTPS
                            │
┌───────────────────────────▼─────────────────────────────────┐
│              Anthropic API (api.anthropic.com)              │
│  - /v1/messages                                             │
│  - /v1/models                                               │
│  - /v1/completions                                          │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Client Layer

**File:** `client.hpp/cpp`

```
Client
├── Config
│   ├── api_key (optional, from env)
│   ├── auth_token (optional, from env)
│   ├── base_url (default: api.anthropic.com)
│   ├── timeout_ms (default: 10 min)
│   └── max_retries (default: 2)
├── initialize_auth()
├── setup_default_headers()
└── Resource Accessors
    ├── messages() → Messages&
    ├── completions() → Completions&
    └── models() → Models&
```

**Responsibilities:**
- Configuration management
- Authentication initialization
- Default header setup
- Resource lifecycle management
- HTTP client integration

### 2. Resource Layer

**Files:** `resources/messages.hpp/cpp`, `resources/models.hpp/cpp`

```
Messages (Resource)
├── Client& client (reference to parent)
├── create(MessageCreateParams) → Message
│   ├── build_request_body()
│   ├── execute HTTP request
│   ├── retry on failure
│   └── parse_response()
├── stream(MessageCreateParams) → MessageStream
└── count_tokens(CountTokensParams) → TokensCount
```

**Responsibilities:**
- API endpoint implementation
- Request parameter validation
- JSON request building
- Response parsing
- Error handling

### 3. HTTP Client Layer

**Files:** `http/http_client.hpp`, `http/winhttp_client.hpp/cpp`

```
HttpClient (Abstract Interface)
├── execute(Request) → Response
├── execute_stream(Request, StreamCallback) → Response
└── set_default_headers(headers)

WinHttpClient (Implementation)
├── HINTERNET session_handle
├── parse_url(url) → URLComponents
├── get_connection(host, port) → HINTERNET
├── parse_response_headers()
├── to_wide() / to_narrow() (UTF-8 conversion)
└── execute() / execute_stream()
```

**Responsibilities:**
- HTTP request execution
- SSL/TLS handling
- Timeout management
- Header parsing
- Streaming data delivery
- UTF-8 encoding conversion

### 4. Type System

**Files:** `types/*.hpp`

```
Message
├── id: string
├── type: string
├── role: string
├── model: string
├── content: vector<ContentBlock>
├── stop_reason: optional<StopReason>
├── stop_sequence: optional<string>
└── usage: Usage

ContentBlock (std::variant)
├── TextBlock
│   ├── type: "text"
│   ├── text: string
│   └── citations: optional<vector<Citation>>
├── ThinkingBlock
│   ├── type: "thinking"
│   ├── thinking: string
│   └── signature: string
├── ToolUseBlock
│   ├── type: "tool_use"
│   ├── id: string
│   ├── name: string
│   └── input: Document (JSON)
└── ... (other block types)

Usage
├── input_tokens: int
├── output_tokens: int
├── cache_creation_input_tokens: optional<int>
├── cache_read_input_tokens: optional<int>
├── inference_geo: optional<string>
└── service_tier: optional<string>
```

**Responsibilities:**
- Type definitions
- Discriminated unions (std::variant)
- Data validation
- Serialization/deserialization

### 5. Utilities Layer

**Files:** `utils/*.hpp/cpp`

```
Utilities
├── JSON Utils
│   ├── json_to_string()
│   ├── string_to_json()
│   ├── get_optional_string/int/bool()
│   └── get_required_string/int/bool()
├── Retry Logic
│   ├── RetryPolicy
│   ├── should_retry(status_code, attempt)
│   ├── calculate_delay(attempt)
│   └── parse_retry_after()
├── Environment
│   └── get_env(name)
└── SSE Parser
    ├── parse(chunk, callback)
    ├── process_line()
    └── dispatch_event()
```

**Responsibilities:**
- JSON parsing and serialization
- Retry policy implementation
- Environment variable access
- Server-Sent Events parsing

### 6. Error Handling

**File:** `types/errors.hpp`

```
Exception Hierarchy
├── std::runtime_error
    └── AnthropicError (base)
        ├── APIError (with status_code)
        │   ├── BadRequestError (400)
        │   ├── AuthenticationError (401)
        │   ├── PermissionDeniedError (403)
        │   ├── NotFoundError (404)
        │   ├── ConflictError (409)
        │   ├── UnprocessableEntityError (422)
        │   ├── RateLimitError (429)
        │   └── InternalServerError (500+)
        ├── ConnectionError
        └── TimeoutError
```

**Responsibilities:**
- Exception hierarchy
- Status code mapping
- Error message formatting
- Response body preservation

## Data Flow

### Synchronous Request Flow

```
User Code
  │
  └─→ messages.create(params)
        │
        ├─→ build_request_body(params) → JSON string
        │
        ├─→ http_client.execute(request)
        │     │
        │     ├─→ WinHttpOpenRequest()
        │     ├─→ WinHttpSendRequest()
        │     ├─→ WinHttpReceiveResponse()
        │     └─→ WinHttpReadData() → response body
        │
        ├─→ Check status code
        │     │
        │     ├─→ [4xx/5xx] → Create APIError
        │     │                  │
        │     │                  └─→ should_retry()?
        │     │                        │
        │     │                        ├─→ Yes → sleep + retry
        │     │                        └─→ No  → throw error
        │     │
        │     └─→ [2xx] → Continue
        │
        └─→ parse_response(body) → Message
              │
              ├─→ Parse JSON with RapidJSON
              ├─→ Extract fields
              ├─→ Parse content blocks
              └─→ Return Message object
```

### Streaming Request Flow (TODO)

```
User Code
  │
  └─→ messages.stream(params)
        │
        ├─→ build_request_body(params) → JSON string
        │
        └─→ http_client.execute_stream(request, callback)
              │
              ├─→ WinHttpReadData() in loop
              │     │
              │     └─→ callback(chunk)
              │           │
              │           └─→ sse_parser.parse(chunk, event_callback)
              │                 │
              │                 └─→ event_callback(SSEEvent)
              │                       │
              │                       ├─→ Parse event type
              │                       ├─→ Deserialize event data
              │                       └─→ Yield to user
              │
              └─→ Return MessageStream
```

## Threading Model

### Thread Safety

The SDK is designed to be thread-safe:

```
┌─────────────────────────────────────────────────────┐
│                  Client Instance                     │
│  (Shared across threads - thread-safe)              │
└───────────┬─────────────────────────────────────────┘
            │
            ├─→ Thread 1 ──→ messages.create(params1)
            │                   │
            │                   └─→ HTTP Request 1
            │
            ├─→ Thread 2 ──→ messages.create(params2)
            │                   │
            │                   └─→ HTTP Request 2
            │
            └─→ Thread 3 ──→ messages.create(params3)
                                │
                                └─→ HTTP Request 3

All threads share:
  - Client configuration (immutable after init)
  - HTTP client (stateless per-request)
  - Default headers (immutable after init)

Each request gets:
  - Separate HINTERNET connection handle
  - Independent request/response buffers
  - Isolated error handling
```

**Thread-Safety Mechanisms:**
1. **Immutable Configuration**: Client config set once at construction
2. **Stateless Operations**: Each request is independent
3. **Connection Management**: WinHTTP handles are request-scoped
4. **Mutex Protection**: (TODO) Connection pooling will use mutexes
5. **Thread-Local RNG**: Retry jitter uses per-thread random generator

### Synchronization Points

Currently:
- ✅ No shared mutable state
- ✅ Configuration is read-only after init
- ✅ Each request creates new connection handle

Future (with connection pooling):
- ⚠️ Connection pool access → requires mutex
- ⚠️ Connection handle reuse → atomic reference counting

## Memory Management

### Ownership Model

```
Client
├── unique_ptr<HttpClient> (owns)
├── unique_ptr<RetryPolicy> (owns)
├── unique_ptr<Messages> (owns, lazy init)
├── unique_ptr<Completions> (owns, lazy init)
└── unique_ptr<Models> (owns, lazy init)

Messages
└── Client& (reference, does not own)

WinHttpClient
├── HINTERNET session_handle (owns, closed in destructor)
└── For each request:
    ├── HINTERNET connect (RAII-wrapped)
    └── HINTERNET request (RAII-wrapped)
```

**Principles:**
- **RAII**: Resources automatically cleaned up
- **Smart Pointers**: unique_ptr for exclusive ownership
- **References**: Resources passed by reference when not owned
- **Value Semantics**: POD types (Message, Usage, etc.) passed by value or const&

### RapidJSON Memory Management

RapidJSON uses custom allocators for performance:

```cpp
Document doc;  // Uses MemoryPoolAllocator by default
doc.SetObject();
auto& allocator = doc.GetAllocator();

// All additions use the allocator
doc.AddMember("key", Value("value", allocator), allocator);
```

**Benefits:**
- Fast allocation (pool-based)
- Automatic cleanup (pool destroyed with Document)
- Zero-copy strings possible

**Caveats:**
- Values must use correct allocator
- Document owns all allocated memory
- Moving/copying requires care

## Extensibility Points

### Adding New Resources

```cpp
// 1. Create resource class
class CustomResource {
public:
    explicit CustomResource(Client& client) : client_(client) {}

    CustomResponse custom_method(const CustomParams& params) {
        // Build request
        // Execute via client_.http_client()
        // Parse response
        return response;
    }

private:
    Client& client_;
};

// 2. Add to Client
class Client {
    // ...
    CustomResource& custom_resource();
private:
    std::unique_ptr<CustomResource> custom_resource_;
};

// 3. Implement accessor
CustomResource& Client::custom_resource() {
    if (!custom_resource_) {
        custom_resource_ = std::make_unique<CustomResource>(*this);
    }
    return *custom_resource_;
}
```

### Adding New Content Block Types

```cpp
// 1. Define block struct
struct CustomBlock {
    std::string type = "custom";
    std::string custom_field;
};

// 2. Add to ContentBlock variant
using ContentBlock = std::variant<
    TextBlock,
    ThinkingBlock,
    CustomBlock,  // Add here
    // ...
>;

// 3. Add parsing logic
if (block_type == "custom") {
    CustomBlock block;
    block.custom_field = get_required_string(json, "custom_field");
    message.content.push_back(block);
}

// 4. Add serialization logic
if (std::holds_alternative<CustomBlock>(block)) {
    const auto& custom = std::get<CustomBlock>(block);
    // Serialize custom fields
}
```

### Adding New Error Types

```cpp
// Define new exception
class CustomError : public APIError {
public:
    CustomError(const std::string& msg, const std::string& body = "")
        : APIError(418, msg, body) {}  // Status code 418
};

// Update factory function
inline std::unique_ptr<APIError> create_api_error(int status_code, ...) {
    switch (status_code) {
        // ...
        case 418:
            return std::make_unique<CustomError>(message, response_body);
        // ...
    }
}
```

## Performance Considerations

### Request Latency

```
Typical Request Breakdown:
├── JSON Serialization:    ~1ms
├── HTTP Connection:       ~50-100ms (first request)
├── TLS Handshake:        ~50-100ms (first request)
├── Network Round-Trip:   ~100-500ms (depends on location)
├── Server Processing:    ~500-5000ms (depends on model/complexity)
├── Response Transfer:    ~10-100ms (depends on size)
└── JSON Deserialization: ~1-5ms

Total: ~700-6000ms per request
```

**Optimization Strategies:**
1. **Connection Reuse** (TODO): Keep connections alive between requests (-100ms per request)
2. **Request Batching** (TODO): Combine multiple requests (-50% latency for batch)
3. **Streaming**: Start processing before complete response (+perceived speed)
4. **Parallel Requests**: Multiple threads for independent requests

### Memory Usage

```
Typical Memory Footprint:
├── Client Instance:       ~1KB
├── HTTP Client:          ~10KB (session + buffers)
├── Per Request:
│   ├── Request JSON:     ~500B - 10KB (depends on message length)
│   ├── Response JSON:    ~1KB - 100KB (depends on response length)
│   ├── Parsed Message:   ~2KB - 200KB (mirrors response)
│   └── HTTP Buffers:     ~16KB (WinHTTP buffers)
└── RapidJSON Document:   ~2x response size (for parsing)

Total: ~50KB - 500KB per active request
```

**Memory Management:**
- Buffers reused per connection
- RapidJSON uses in-situ parsing where possible
- Response strings released after parsing
- RAII ensures cleanup on exceptions

### Build Time

```
Compilation:
├── Headers (first time):  ~3s
├── Implementation:        ~5s per .cpp
├── Linking:              ~2s
└── Total (clean build):  ~15-20s

Incremental:
└── Single file change:   ~2-5s
```

**Optimization:**
- Header-only RapidJSON (slower compile, faster iteration)
- Forward declarations minimize includes
- Precompiled headers possible for large projects

## Design Patterns Used

1. **Resource Pattern**: API endpoints as resource objects
2. **Builder Pattern**: MessageCreateParams with optional fields
3. **Factory Pattern**: create_api_error() for exception creation
4. **RAII**: Automatic resource cleanup
5. **Visitor Pattern**: std::variant with std::visit for ContentBlock
6. **Strategy Pattern**: RetryPolicy for retry behavior
7. **Template Method**: HttpClient abstract interface
8. **Singleton-like**: Resource lazy initialization in Client

## Dependency Graph

```
client.hpp
  ├─→ http/http_client.hpp
  ├─→ utils/retry_logic.hpp
  └─→ resources/messages.hpp
        ├─→ types/message.hpp
        │     ├─→ types/content_block.hpp
        │     ├─→ types/stop_reason.hpp
        │     └─→ types/usage.hpp
        └─→ utils/json_utils.hpp
              └─→ rapidjson/*

http/winhttp_client.hpp
  ├─→ http/http_client.hpp
  └─→ windows.h / winhttp.h

types/errors.hpp
  └─→ stdexcept

No circular dependencies!
```

## Future Architecture Enhancements

### Connection Pooling

```cpp
class ConnectionPool {
    std::mutex mutex_;
    std::vector<HINTERNET> available_connections_;
    std::map<HINTERNET, bool> in_use_;

public:
    HINTERNET acquire(const std::string& host, int port);
    void release(HINTERNET handle);
};
```

### Async Support

```cpp
class Client {
    std::future<Message> create_async(const MessageCreateParams& params);
    // Uses std::async internally
};
```

### Caching Layer

```cpp
class CachingHttpClient : public HttpClient {
    std::map<std::string, CachedResponse> cache_;
    std::chrono::seconds ttl_;

    Response execute(const Request& request) override {
        if (auto cached = check_cache(request)) {
            return *cached;
        }
        auto response = underlying_client_->execute(request);
        cache_response(request, response);
        return response;
    }
};
```

This architecture provides a solid foundation for extending the SDK with additional features while maintaining clean separation of concerns and testability.
