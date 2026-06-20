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

# Self-Hosted Environment Runner

For running a managed agent's tools locally against a self-hosted environment, the SDK exposes three pieces:

- `client.beta.environments.work.worker(...)` — the full worker (an `EnvironmentWorker`; also
  constructible directly as `EnvironmentWorker(client, ...)` from `anthropic.lib.environments`):
  polls the environment for work, and for each claimed session sets up the workdir + downloads the
  session agent's skills, runs your tools against the session's `agent.tool_use` /
  `agent.custom_tool_use` events while heartbeating the work-item lease, force-stops the work on
  exit, and loops. `worker.handle_item(...)`
  runs that same per-item flow for a single work item you've already claimed; with no arguments it
  reads the work id / environment id / session id from `ANTHROPIC_WORK_ID` /
  `ANTHROPIC_ENVIRONMENT_ID` / `ANTHROPIC_SESSION_ID` and the environment key from
  `ANTHROPIC_ENVIRONMENT_KEY` (the env vars `ant worker poll --on-work` sets). `environment_id`
  passed to `worker()` is only needed by `run()`'s poll loop; `environment_key` is the worker's
  single credential — `handle_item()` falls back to the value passed to `worker()` and then to
  `ANTHROPIC_ENVIRONMENT_KEY`. Async only; built on `anyio`, so it works under either `asyncio` or
  `trio`.
- `client.beta.sessions.events.tool_runner(...)` — the sessions-side counterpart to
  `client.beta.messages.tool_runner`: a `SessionToolRunner`, an async iterable that attaches to a
  session's event stream, runs the matching tool for each tool-call event — `agent.tool_use`
  (built-in tools) answered with `user.tool_result`, and `agent.custom_tool_use` (custom tools)
  answered with `user.custom_tool_result` — posts the result back, and yields one
  `DispatchedToolCall` per completed call. Use it directly when you want to observe each dispatch
  (the worker drives one internally). Async only.
- `client.beta.environments.work.poller(...)` — the control-plane only piece: claims work items,
  ack's each one, and yields each claimed work item. Async only — available on `AsyncAnthropic`
  (its `worker(...)` companion is async too, so the sync client does not expose either).

The standard `agent_toolset_20260401` implementations (`bash`, `read`, `write`, `edit`, `glob`,
`grep`) plus the workdir/skills `AgentToolContext` live in `anthropic.lib.tools.agent_toolset`.

The high-level worker is one object:

```python
import os, asyncio
from anthropic import AsyncAnthropic
from anthropic.lib.tools import beta_async_tool
from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401

client = AsyncAnthropic()


@beta_async_tool
async def deploy(target: str) -> str:
    ...


# `client.beta.environments.work.worker(...)` builds an `EnvironmentWorker`; you can also construct
# one directly with `EnvironmentWorker(client, ...)` from `anthropic.lib.environments`.
await client.beta.environments.work.worker(
    environment_id=os.environ["ANTHROPIC_ENVIRONMENT_ID"],
    environment_key=os.environ["ANTHROPIC_ENVIRONMENT_KEY"],
    workdir="/workspace",
    # `tools` is a fixed list or a factory invoked per session with that session's `AgentToolContext`
    # (use the factory form to bind `beta_agent_toolset_20260401` to the right session). Defaults to
    # `beta_agent_toolset_20260401(env)`.
    tools=lambda env: [*beta_agent_toolset_20260401(env), deploy],
).run()  # loops forever; cancel the task / wrap in asyncio.wait_for to bound it
```

If you already hold a claimed work item — e.g. an `ant worker poll --on-work` script handed one to a
fresh process — call `handle_item` to run just the per-item flow (build the workdir + skills, run the
session's tools while heartbeating the lease, force-stop on exit). Inside that command the work id /
environment id / session id / environment key are already in the environment, so the sandbox case is
just:

```python
await client.beta.environments.work.worker(workdir="/workspace", tools=tools).handle_item()
```

Pass the values explicitly when you have the objects in hand (e.g. you iterate the poller yourself):

```python
await client.beta.environments.work.worker(workdir="/workspace", tools=tools).handle_item(
    work_id=work.id,
    environment_id=work.environment_id,
    session_id=work.data.id,
    environment_key=environment_key,
)
```

If you want to observe each tool call (or wire up the workdir / poller yourself), use the
session tool runner directly:

```python
from anthropic import AsyncAnthropic
from anthropic.lib.tools.agent_toolset import AgentToolContext, beta_agent_toolset_20260401

client = AsyncAnthropic()

async for work in client.beta.environments.work.poller(
    environment_id=..., environment_key=environment_key,
):
    if work.data.type != "session":
        continue
    # Passing `client` and `session_id` makes `AgentToolContext` fetch the session's resolved agent
    # on enter and download each of its skills into `{workdir}/skills/<name>/`.
    async with AgentToolContext(workdir="/workspace", client=client, session_id=work.data.id) as env:
        async for call in client.beta.sessions.events.tool_runner(
            work.data.id,
            tools=beta_agent_toolset_20260401(env),
            environment_key=environment_key,
        ):
            print(f"{call.name} -> {'error' if call.is_error else 'ok'}")
```

`beta_agent_toolset_20260401(env)` returns a plain `list[BetaAsyncFunctionTool]`. Filter or extend
it directly:

```python
from anthropic.lib.tools import beta_async_tool
from anthropic.lib.tools.agent_toolset import beta_read_tool, beta_agent_toolset_20260401

tools = [*beta_agent_toolset_20260401(env), deploy]
tools = [t for t in beta_agent_toolset_20260401(env) if t.name != "bash"]
```

> **Run stateful tools under the session tool runner, not the Messages tool runner.** The `bash`
> tool owns a persistent `/bin/bash` subprocess that is only torn down by its `close` cleanup hook.
> Only `client.beta.sessions.events.tool_runner(...)` (the `SessionToolRunner`) and the
> `EnvironmentWorker` built on it call that hook. `client.beta.messages.tool_runner(...)` does
> **not** call `close`, so handing it this toolset leaks one orphaned shell per run. Use the
> session tool runner / environment worker for the agent toolset, or drop `bash` (as in the second
> line above) before passing the toolset to the Messages tool runner.

The `bash` tool runs an unrestricted `/bin/bash` and executes file operations and shell commands
directly on the host. Run the worker inside a container or other isolation boundary you control.
(The file tools — `read`/`write`/`edit`/`glob`/`grep` — confine to the workdir with a symlink-aware
check, so they are safe without a sandbox; `bash` is not.) `bash` does not inherit the runner's
`ANTHROPIC_*` credentials; pass `AgentToolContext(env=...)` to control the subprocess environment.

See [`examples/managed-agents-self-hosted-sandbox-worker.py`](examples/managed-agents-self-hosted-sandbox-worker.py) for a complete example.
