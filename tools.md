# Tools helpers

To define a tool, you can use the `@beta_tool` decorator on any python function like so:

```python
from anthropic import beta_tool

@beta_tool
def sum(left: int, right: int) -> str:
    """Adds two integers together.
    Args:
        left (int): The first integer to add.
        right (int): The second integer to add.
    Returns:
        int: The sum of left and right integers.
    """

    return str(left + right)
```

> [!TIP]
> If you're using the async client, replace `@beta_tool` with `@beta_async_tool` and define the function with `async def`.

The `@beta_tool` decorator will inspect the function arguments and the docstring to extract a json schema representation of the given function, in this case it'll be turned into:

```json
{
  "name": "sum",
  "description": "Adds two integers together.",
  "input_schema": {
    "additionalProperties": false,
    "properties": {
      "left": {
        "description": "The first integer to add.",
        "title": "Left",
        "type": "integer"
      },
      "right": {
        "description": "The second integer to add.",
        "title": "Right",
        "type": "integer"
      }
    },
    "required": ["left", "right"],
    "type": "object"
  }
}
```

If you want to implement calling the tool yourself, you can then pass the to the API like so:

```python
message = client.beta.messages.create(
    tools=[get_weather],
    # ...
    max_tokens=1024,
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "What is 2 + 2?"}],
)
```

or you can use our [tool runner](#tool-runner)!

## Tool runner

We provide a `client.beta.messages.tool_runner()` method that can automatically call tools defined with `@beta_tool()`. This method returns a `BetaToolRunner` class that is an iterator where each iteration yields a new `BetaMessage` instance from an API call. Iteration is driven by each message's `stop_reason`: on `tool_use` the runner executes the requested tools and sends the results back, on `pause_turn` or `compaction` it sends the turn back unchanged so the server can resume it, and on any other stop reason it stops after yielding that final message without running tools.

```py
runner = client.beta.messages.tool_runner(
    max_tokens=1024,
    model="claude-sonnet-4-5-20250929",
    tools=[sum],
    messages=[{"role": "user", "content": "What is 9 + 10?"}],
)
for message in runner:
    rich.print(message)
```

### Compacting the conversation

With the `compact-2026-09-04` beta you decide when a conversation is compacted: a request with the `compaction` param returns a single `compaction` block, which then replaces the messages it summarizes. In a tool runner, call `runner.compact_before_next_turn()` and the runner does this for you.

```py
runner = client.beta.messages.tool_runner(
    max_tokens=1024,
    model="claude-sonnet-4-5-20250929",
    betas=["compact-2026-09-04"],
    tools=[search_docs],
    messages=[{"role": "user", "content": "Find every page that mentions rate limits."}],
)
for message in runner:
    if message.usage.input_tokens > 100_000:
        runner.compact_before_next_turn()
```

The call only schedules the compaction. Once the current turn has finished, including any tool calls, the runner requests a summary, replaces its message history with the compaction response the API returns, and carries on. A turn that was paused (`pause_turn`) is resumed and finished first. If the current turn is the last one, the runner compacts and then stops. If you call it before iterating, the compaction is the first request.

The compaction response is yielded like any other message and doesn't count towards `max_iterations`. It has `stop_reason == "compaction"`, the summary is in `message.content[0].content`, and its `usage.input_tokens` is the size of the history that was just summarized. Calling `compact_before_next_turn()` while handling that message does nothing, so a threshold like the one above doesn't compact twice.

`compact_before_next_turn()` takes the same config as the `compaction` param of `messages.create()`, for example to give your own summarization instructions:

```py
runner.compact_before_next_turn({"type": "summarize", "instructions": "Keep the page URLs found so far."})
```

A few things to know:

- Calling it again before the compaction runs replaces the pending one.
- The runner doesn't add the beta for you, so pass `betas=["compact-2026-09-04"]`.
- `context_management` is left out of the compaction request, because the API doesn't accept the two together, and is sent again afterwards. `compact_before_next_turn()` raises if `context_management` has a `compact_*` edit.
- While you're handling the compaction response, `append_messages()` and replacing `messages` with `set_messages_params()` raise, because the compaction response is about to replace the messages. Other params can still be changed.
- If the API returns no summary, the runner logs a warning and keeps the history as it is.
- If the run ends on a turn that was cut short with tool calls that never ran (`stop_reason == "max_tokens"`, for example), the pending compaction is skipped with a warning. It is also skipped if the run stops at `max_iterations` or you `break` out of the loop.
- The `compaction` param itself can't be set on a tool runner, because every request in the loop would compact again.

## ToolError

To report an error from a tool back to the model, raise a `ToolError`. Unlike a plain exception, `ToolError` accepts content blocks, allowing you to include images or other structured content in the error response:

```py
from anthropic import beta_tool
from anthropic.lib.tools import ToolError

@beta_tool
def take_screenshot(url: str) -> str:
    """Take a screenshot of a URL."""
    if not is_valid_url(url):
        raise ToolError(f"Invalid URL: {url}")
    result = capture(url)
    if result.error:
        # Include the error screenshot so the model can see what went wrong
        raise ToolError([
            {"type": "text", "text": f"Failed to load page: {result.error}"},
            {"type": "image", "source": {"type": "base64", "data": result.screenshot, "media_type": "image/png"}},
        ])
    return result.data
```

If a plain exception is raised, its `repr()` will be sent to the model as a text error and logged. `ToolError` is not logged since it represents an intentional error response.
