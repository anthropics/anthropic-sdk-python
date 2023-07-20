# Anthropic Python API Library

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)

The Anthropic Python library provides convenient access to the Anthropic REST API from any Python 3.7+
application. It includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Migration from v0.2.x and below

In `v0.3.0`, we introduced a fully rewritten SDK.

The new version uses separate sync and async clients, unified streaming, typed params and structured response objects, and resource-oriented methods:

**Sync before/after:**

```diff
- client = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
+ client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
  # or, simply provide an ANTHROPIC_API_KEY environment variable:
+ client = anthropic.Anthropic()

- rsp = client.completion(**params)
- rsp["completion"]
+ rsp = client.completions.create(**params)
+ rsp.completion
```

**Async before/after:**

```diff
- client = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
+ client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

- await client.acompletion(**params)
+ await client.completions.create(**params)
```

The `.completion_stream()` and `.acompletion_stream()` methods have been removed;
simply pass `stream=True`to `.completions.create()`.

Streaming responses are now incremental; the full text is not sent in each message,
as v0.3 sends the `Anthropic-Version: 2023-06-01` header.

<details>
<summary>Example streaming diff</summary>

```diff py
  import anthropic

- client = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
+ client = anthropic.Anthropic()

  # Streams are now incremental diffs of text
  # rather than sending the whole message every time:
  text = "
- stream = client.completion_stream(**params)
- for data in stream:
-     diff = data["completion"].replace(text, "")
-     text = data["completion"]
+ stream = client.completions.create(**params, stream=True)
+ for data in stream:
+     diff = data.completion # incremental text
+     text += data.completion
      print(diff, end="")

  print("Done. Final text is:")
  print(text)
```

</details>

## Documentation

The API documentation can be found [here](https://docs.anthropic.com/claude/reference/).

## Installation

```sh
pip install anthropic
```

## Usage

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my api key",
)

completion = anthropic.completions.create(
    model="claude-2",
    max_tokens_to_sample=300,
    prompt=f"{HUMAN_PROMPT} how does a court case get to the Supreme Court? {AI_PROMPT}",
)
print(completion.completion)
```

While you can provide an `api_key` keyword argument, we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
and adding `ANTHROPIC_API_KEY="my api key"` to your `.env` file so that your API Key is not stored in source control.

## Async Usage

Simply import `AsyncAnthropic` instead of `Anthropic` and use `await` with each API call:

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = AsyncAnthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my api key",
)


async def main():
    completion = await anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=f"{HUMAN_PROMPT} how does a court case get to the Supreme Court? {AI_PROMPT}",
    )
    print(completion.completion)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Streaming Responses

We provide support for streaming responses using Server Side Events (SSE).

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = Anthropic()

stream = anthropic.completions.create(
    prompt=f"{HUMAN_PROMPT} Your prompt here {AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
    stream=True,
)
for completion in stream:
    print(completion.completion)
```

The async client uses the exact same interface.

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = AsyncAnthropic()

stream = await anthropic.completions.create(
    prompt=f"{HUMAN_PROMPT} Your prompt here {AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
    stream=True,
)
async for completion in stream:
    print(completion.completion)
```

## Using Types

Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict), while responses are [Pydantic](https://pydantic-docs.helpmanual.io/) models. This helps provide autocomplete and documentation within your editor.

If you would like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `"basic"`.

## Handling errors

When the library is unable to connect to the API (e.g., due to network connection problems or a timeout), a subclass of `anthropic.APIConnectionError` is raised.

When the API returns a non-success status code (i.e., 4xx or 5xx
response), a subclass of `anthropic.APIStatusError` will be raised, containing `status_code` and `response` properties.

All errors inherit from `anthropic.APIError`.

```python
import anthropic

client = anthropic.Anthropic()

try:
    client.completions.create(
        prompt=f"{anthropic.HUMAN_PROMPT} Your prompt here {anthropic.AI_PROMPT}",
        max_tokens_to_sample=300,
        model="claude-2",
    )
except anthropic.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except anthropic.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except anthropic.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Retries

Certain errors will be automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 409 Conflict, 429 Rate Limit,
and >=500 Internal errors will all be retried by default.

You can use the `max_retries` option to configure or disable this:

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Configure the default for all requests:
anthropic = Anthropic(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
anthropic.with_options(max_retries=5).completions.create(
    prompt=f"{HUMAN_PROMPT} Can you help me effectively ask for a raise at work? {AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
)
```

### Timeouts

Requests time out after 60 seconds by default. You can configure this with a `timeout` option,
which accepts a float or an [`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration):

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Configure the default for all requests:
anthropic = Anthropic(
    # default is 60s
    timeout=20.0,
)

# More granular control:
anthropic = Anthropic(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
anthropic.with_options(timeout=5 * 1000).completions.create(
    prompt=f"{HUMAN_PROMPT} Where can I get a good coffee in my neighbourhood? {AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
)
```

On timeout, an `APITimeoutError` is thrown.

Note that requests which time out will be [retried twice by default](#retries).

## Default Headers

We automatically send the `anthropic-version` header set to `2023-06-01`.

If you need to, you can override it by setting default headers per-request or on the client object.

Be aware that doing so may result in incorrect types and other unexpected or undefined behavior in the SDK.

```python
from anthropic import Anthropic

anthropic = Anthropic(
    default_headers={"anthropic-version": "My-Custom-Value"},
)
```

## Advanced: Configuring custom URLs, proxies, and transports

You can configure the following keyword arguments when instantiating the client:

```python
import httpx
from anthropic import Anthropic

anthropic = Anthropic(
    # Use a custom base URL
    base_url="http://my.test.server.example.com:8083",
    proxies="http://my.test.proxy.example.com",
    transport=httpx.HTTPTransport(local_address="0.0.0.0"),
)
```

See the httpx documentation for information about the [`proxies`](https://www.python-httpx.org/advanced/#http-proxying) and [`transport`](https://www.python-httpx.org/advanced/#custom-transports) keyword arguments.

## Status

This package is in beta. Its internals and interfaces are not stable and subject to change without a major semver bump;
please reach out if you rely on any undocumented behavior.

We are keen for your feedback; please open an [issue](https://www.github.com/anthropics/anthropic-sdk-python/issues) with questions, bugs, or suggestions.

## Requirements

Python 3.7 or higher.
