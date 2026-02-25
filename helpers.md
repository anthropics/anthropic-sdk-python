# Message Helpers

## Streaming Responses

```python
async with client.messages.stream(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Say hello there!",
        }
    ],
    model="claude-3-5-sonnet-latest",
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
    print()
```

`client.messages.stream()` returns a `MessageStreamManager`, which is a context manager that yields a `MessageStream` which is iterable, emits events and accumulates messages.

Alternatively, you can use `client.messages.create(..., stream=True)` which returns an
iterable of the events in the stream and uses less memory (most notably, it does not accumulate a final message
object for you).

The stream will be cancelled when the context manager exits but you can also close it prematurely by calling `stream.close()`.

See an example of streaming helpers in action in [`examples/messages_stream.py`](examples/messages_stream.py).

> [!NOTE]
> The synchronous client has the same interface just without `async/await`.

### Lenses

#### `.text_stream`

Provides an iterator over just the text deltas in the stream:

```py
async for text in stream.text_stream:
    print(text, end="", flush=True)
print()
```

### Events

The events listed here are just the event types that the SDK extends, for a full list of the events returned by the API, see [these docs](https://docs.anthropic.com/en/api/messages-streaming#event-types).

```py
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async with client.messages.stream(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Say hello there!",
        }
    ],
    model="claude-3-5-sonnet-latest",
) as stream:
    async for event in stream:
        if event.type == "text":
            print(event.text, end="", flush=True)
        elif event.type == 'content_block_stop':
            print('\n\ncontent block finished accumulating:', event.content_block)

    print()

# you can still get the accumulated final message outside of
# the context manager, as long as the entire stream was consumed
# inside of the context manager
accumulated = await stream.get_final_message()
print("accumulated message: ", accumulated.to_json())
```

#### `text`

This event is yielded whenever a text `content_block_delta` event is returned by the API & includes the delta and the accumulated snapshot, e.g.

```py
if event.type == "text":
    event.text  # " there"
    event.snapshot  # "Hello, there"
```

#### `input_json`

This event is yielded whenever a JSON `content_block_delta` event is returned by the API & includes the delta and the accumulated snapshot, e.g.

```py
if event.type == "input_json":
    event.partial_json  # ' there"'
    event.snapshot  # '{"message": "Hello, there"'
```

#### `message_stop`

The event is fired when a full Message object has been accumulated.

```py
if event.type == "message_stop":
    event.message  # Message
```

#### `content_block_stop`

The event is fired when a full ContentBlock object has been accumulated.

```py
if event.type == "content_block_stop":
    event.content_block  # ContentBlock
```

### Methods

#### `await .close()`

Aborts the request.

#### `await .until_done()`

Blocks until the stream has been read to completion.

#### `await .get_final_message()`

Blocks until the stream has been read to completion and returns the accumulated `Message` object.

#### `await .get_final_text()`

> [!NOTE]
> Currently the API will only ever return 1 content block

Blocks until the stream has been read to completion and returns all `text` content blocks concatenated together.

## MCP Helpers

This SDK provides helpers for integrating with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers. These helpers convert MCP types to Anthropic API types, reducing boilerplate when working with MCP tools, prompts, and resources.

> **Note:** The Claude API also supports an [`mcp_servers` parameter](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) that lets Claude connect directly to remote MCP servers.
>
> - Use `mcp_servers` when you have remote servers accessible via URL and only need tool support.
> - Use the MCP helpers when you need local MCP servers, prompts, resources, or more control over the MCP connection.

> **Requires:** `pip install anthropic[mcp]` (Python 3.10+)

### Using MCP tools with tool_runner

```py
from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

client = AsyncAnthropic()

async with stdio_client(StdioServerParameters(command="mcp-server")) as (read, write):
    async with ClientSession(read, write) as mcp_client:
        await mcp_client.initialize()

        tools_result = await mcp_client.list_tools()
        runner = await client.beta.messages.tool_runner(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Use the available tools"}],
            tools=[async_mcp_tool(t, mcp_client) for t in tools_result.tools],
        )
        async for message in runner:
            print(message)
```

> [!TIP]
> If you're using the sync client, replace `async_mcp_tool` with `mcp_tool`.

### Using MCP prompts

```py
from anthropic.lib.tools.mcp import mcp_message

prompt = await mcp_client.get_prompt(name="my-prompt")
response = await client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[mcp_message(m) for m in prompt.messages],
)
```

### Using MCP resources as content

```py
from anthropic.lib.tools.mcp import mcp_resource_to_content

resource = await mcp_client.read_resource(uri="file:///path/to/doc.txt")
response = await client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            mcp_resource_to_content(resource),
            {"type": "text", "text": "Summarize this document"},
        ],
    }],
)
```

### Uploading MCP resources as files

```py
from anthropic.lib.tools.mcp import mcp_resource_to_file

resource = await mcp_client.read_resource(uri="file:///path/to/data.json")
uploaded = await client.beta.files.upload(file=mcp_resource_to_file(resource))
```

### Error handling

The conversion functions raise `UnsupportedMCPValueError` if an MCP value cannot be converted to a format supported by the Claude API (e.g., unsupported content type like audio, unsupported MIME type).
