# Anthropic Python API library

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)

The Anthropic Python library provides convenient access to the Anthropic REST API from any Python 3.7+
application. It includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Documentation

The REST API documentation can be found [on docs.anthropic.com](https://docs.anthropic.com/claude/reference/). The full API of this library can be found in [api.md](api.md).

## Installation

```sh
# install from PyPI
pip install anthropic
```

## Usage

The full API of this library can be found in [api.md](api.md).

```python
import os
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-3-opus-20240229",
)
print(message.content)
```

While you can provide an `api_key` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add `ANTHROPIC_API_KEY="my-anthropic-api-key"` to your `.env` file
so that your API Key is not stored in source control.

## Async usage

Simply import `AsyncAnthropic` instead of `Anthropic` and use `await` with each API call:

```python
import os
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


async def main() -> None:
    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-opus-20240229",
    )
    print(message.content)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Streaming Responses

We provide support for streaming responses using Server Side Events (SSE).

```python
from anthropic import Anthropic

client = Anthropic()

stream = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-3-opus-20240229",
    stream=True,
)
for event in stream:
    print(event.type)
```

The async client uses the exact same interface.

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

stream = await client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-3-opus-20240229",
    stream=True,
)
async for event in stream:
    print(event.type)
```

### Streaming Helpers

This library provides several conveniences for streaming messages, for example:

```py
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def main() -> None:
    async with client.messages.stream(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="claude-3-opus-20240229",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

    message = await stream.get_final_message()
    print(message.model_dump_json(indent=2))

asyncio.run(main())
```

Streaming with `client.messages.stream(...)` exposes [various helpers for your convenience](helpers.md) including event handlers and accumulation.

Alternatively, you can use `client.messages.create(..., stream=True)` which only returns an async iterable of the events in the stream and thus uses less memory (it does not build up a final message object for you).

## Token counting

You can see the exact usage for a given request through the `usage` response property, e.g.

```py
message = client.messages.create(...)
message.usage
# Usage(input_tokens=25, output_tokens=13)
```

## AWS Bedrock

This library also provides support for the [Anthropic Bedrock API](https://aws.amazon.com/bedrock/claude/) if you install this library with the `bedrock` extra, e.g. `pip install -U anthropic[bedrock]`.

You can then import and instantiate a separate `AnthropicBedrock` class, the rest of the API is the same.

```py
from anthropic import AnthropicBedrock

client = AnthropicBedrock()

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
    model="anthropic.claude-3-sonnet-20240229-v1:0",
)
print(message)
```

For a more fully fledged example see [`examples/bedrock.py`](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/bedrock.py).

## Google Vertex

> [!IMPORTANT]  
> This API is in private preview.

This library also provides support for the [Anthropic Vertex API](https://cloud.google.com/vertex-ai?hl=en) if you install this library with the `vertex` extra, e.g. `pip install -U anthropic[vertex]`.

You can then import and instantiate a separate `AnthropicVertex`/`AsyncAnthropicVertexAsync` class, which has the same API as the base `Anthropic`/`AsyncAnthropic` class.

```py
from anthropic import AnthropicVertex

client = AnthropicVertex()

message = client.messages.create(
    model="claude-3-sonnet@20240229",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Hello!",
        }
    ],
)
print(message)
```

For a more complete example see [`examples/vertex.py`](https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/vertex.py).

## Using types

Nested request parameters are [TypedDicts](https://docs.python.org/3/library/typing.html#typing.TypedDict). Responses are [Pydantic models](https://docs.pydantic.dev), which provide helper methods for things like:

- Serializing back into JSON, `model.model_dump_json(indent=2, exclude_unset=True)`
- Converting to a dictionary, `model.model_dump(exclude_unset=True)`

Typed requests and responses provide autocomplete and documentation within your editor. If you would like to see type errors in VS Code to help catch bugs earlier, set `python.analysis.typeCheckingMode` to `basic`.

## Handling errors

When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of `anthropic.APIConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of `anthropic.APIStatusError` is raised, containing `status_code` and `response` properties.

All errors inherit from `anthropic.APIError`.

```python
import anthropic
from anthropic import Anthropic

client = Anthropic()

try:
    client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-opus-20240229",
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

Certain errors are automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict,
429 Rate Limit, and >=500 Internal errors are all retried by default.

You can use the `max_retries` option to configure or disable retry settings:

```python
from anthropic import Anthropic

# Configure the default for all requests:
client = Anthropic(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-3-opus-20240229",
)
```

### Timeouts

By default requests time out after 10 minutes. You can configure this with a `timeout` option,
which accepts a float or an [`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration) object:

```python
from anthropic import Anthropic

# Configure the default for all requests:
client = Anthropic(
    # 20 seconds (default is 10 minutes)
    timeout=20.0,
)

# More granular control:
client = Anthropic(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5 * 1000).messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-3-opus-20240229",
)
```

On timeout, an `APITimeoutError` is thrown.

Note that requests that time out are [retried twice by default](#retries).

## Default Headers

We automatically send the `anthropic-version` header set to `2023-06-01`.

If you need to, you can override it by setting default headers per-request or on the client object.

Be aware that doing so may result in incorrect types and other unexpected or undefined behavior in the SDK.

```python
from anthropic import Anthropic

client = Anthropic(
    default_headers={"anthropic-version": "My-Custom-Value"},
)
```

## Advanced

### Logging

We use the standard library [`logging`](https://docs.python.org/3/library/logging.html) module.

You can enable logging by setting the environment variable `ANTHROPIC_LOG` to `debug`.

```shell
$ export ANTHROPIC_LOG=debug
```

### How to tell whether `None` means `null` or missing

In an API response, a field may be explicitly `null`, or missing entirely; in either case, its value is `None` in this library. You can differentiate the two cases with `.model_fields_set`:

```py
if response.my_field is None:
  if 'my_field' not in response.model_fields_set:
    print('Got json like {}, without a "my_field" key present at all.')
  else:
    print('Got json like {"my_field": null}.')
```

### Accessing raw response data (e.g. headers)

The "raw" Response object can be accessed by prefixing `.with_raw_response.` to any HTTP method call, e.g.,

```py
from anthropic import Anthropic

client = Anthropic()
response = client.messages.with_raw_response.create(
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Hello, Claude",
    }],
    model="claude-3-opus-20240229",
)
print(response.headers.get('X-My-Header'))

message = response.parse()  # get the object that `messages.create()` would have returned
print(message.content)
```

These methods return an [`LegacyAPIResponse`](https://github.com/anthropics/anthropic-sdk-python/tree/main/src/anthropic/_legacy_response.py) object. This is a legacy class as we're changing it slightly in the next major version.

For the sync client this will mostly be the same with the exception
of `content` & `text` will be methods instead of properties. In the
async client, all methods will be async.

A migration script will be provided & the migration in general should
be smooth.

#### `.with_streaming_response`

The above interface eagerly reads the full response body when you make the request, which may not always be what you want.

To stream the response body, use `.with_streaming_response` instead, which requires a context manager and only reads the response body once you call `.read()`, `.text()`, `.json()`, `.iter_bytes()`, `.iter_text()`, `.iter_lines()` or `.parse()`. In the async client, these are async methods.

As such, `.with_streaming_response` methods return a different [`APIResponse`](https://github.com/anthropics/anthropic-sdk-python/tree/main/src/anthropic/_response.py) object, and the async client returns an [`AsyncAPIResponse`](https://github.com/anthropics/anthropic-sdk-python/tree/main/src/anthropic/_response.py) object.

```python
with client.messages.with_streaming_response.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],
    model="claude-3-opus-20240229",
) as response:
    print(response.headers.get("X-My-Header"))

    for line in response.iter_lines():
        print(line)
```

The context manager is required so that the response will reliably be closed.

### Configuring the HTTP client

You can directly override the [httpx client](https://www.python-httpx.org/api/#client) to customize it for your use case, including:

- Support for proxies
- Custom transports
- Additional [advanced](https://www.python-httpx.org/advanced/#client-instances) functionality

```python
import httpx
from anthropic import Anthropic

client = Anthropic(
    # Or use the `ANTHROPIC_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

### Managing HTTP resources

By default the library closes underlying HTTP connections whenever the client is [garbage collected](https://docs.python.org/3/reference/datamodel.html#object.__del__). You can manually close the client using the `.close()` method if desired, or with a context manager that closes when exiting.

## Versioning

This package generally follows [SemVer](https://semver.org/spec/v2.0.0.html) conventions, though certain backwards-incompatible changes may be released as minor versions:

1. Changes that only affect static types, without breaking runtime behavior.
2. Changes to library internals which are technically public but not intended or documented for external use. _(Please open a GitHub issue to let us know if you are relying on such internals)_.
3. Changes that we do not expect to impact the vast majority of users in practice.

We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

We are keen for your feedback; please open an [issue](https://www.github.com/anthropics/anthropic-sdk-python/issues) with questions, bugs, or suggestions.

## Requirements

Python 3.7 or higher.
