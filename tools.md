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
    tools=[get_weather.to_dict()],
    # ...
    max_tokens=1024,
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "What is 2 + 2?"}],
)
```

or you can use our [tool runner](#tool-runner)!

## Tool runner

We provide a `client.beta.messages.tool_runner()` method that can automatically call tools defined with `@beta_tool()`. This method returns a `BetaToolRunner` class that is an iterator where each iteration yields a new `BetaMessage` instance from an API call, iteration will stop when there no tool call content blocks.

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
