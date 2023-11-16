# Anthropic Python API library

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)

The Anthropic Python library provides convenient access to the Anthropic REST API from any Python 3.7+
application. It includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

For the AWS Bedrock API, see [`anthropic-bedrock`](https://github.com/anthropics/anthropic-bedrock-python).

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

The full API of this library can be found in [api.md](https://www.github.com/anthropics/anthropic-sdk-python/blob/main/api.md).

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my api key",
)

completion = anthropic.completions.create(
    model="claude-2",
    max_tokens_to_sample=300,
    prompt=f"{HUMAN_PROMPT} how does a court case get to the Supreme Court?{AI_PROMPT}",
)
print(completion.completion)
```

While you can provide an `api_key` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add `ANTHROPIC_API_KEY="my-anthropic-api-key"` to your `.env` file
so that your API Key is not stored in source control.

## Async usage

Simply import `AsyncAnthropic` instead of `Anthropic` and use `await` with each API call:

```python
from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = AsyncAnthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="my api key",
)


async def main():
    completion = await anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=f"{HUMAN_PROMPT} how does a court case get to the Supreme Court?{AI_PROMPT}",
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
    prompt=f"{HUMAN_PROMPT} Your prompt here{AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
    stream=True,
)
for completion in stream:
    print(completion.completion, end="", flush=True)
```

The async client uses the exact same interface.

```python
from anthropic import AsyncAnthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = AsyncAnthropic()

stream = await anthropic.completions.create(
    prompt=f"{HUMAN_PROMPT} Your prompt here{AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
    stream=True,
)
async for completion in stream:
    print(completion.completion, end="", flush=True)
```

## Token counting

You can estimate billing for a given request with the `client.count_tokens()` method, eg:

```py
client = Anthropic()
client.count_tokens('Hello world!')  # 3
```

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

client = anthropic.Anthropic()

try:
    client.completions.create(
        prompt=f"{anthropic.HUMAN_PROMPT} Your prompt here{anthropic.AI_PROMPT}",
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

Certain errors are automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict,
429 Rate Limit, and >=500 Internal errors are all retried by default.

You can use the `max_retries` option to configure or disable retry settings:

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Configure the default for all requests:
anthropic = Anthropic(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
anthropic.with_options(max_retries=5).completions.create(
    prompt=f"{HUMAN_PROMPT} Can you help me effectively ask for a raise at work?{AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
)
```

### Timeouts

By default requests time out after 10 minutes. You can configure this with a `timeout` option,
which accepts a float or an [`httpx.Timeout`](https://www.python-httpx.org/advanced/#fine-tuning-the-configuration) object:

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Configure the default for all requests:
anthropic = Anthropic(
    # default is 10 minutes
    timeout=20.0,
)

# More granular control:
anthropic = Anthropic(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
anthropic.with_options(timeout=5 * 1000).completions.create(
    prompt=f"{HUMAN_PROMPT} Where can I get a good coffee in my neighbourhood?{AI_PROMPT}",
    max_tokens_to_sample=300,
    model="claude-2",
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

The "raw" Response object can be accessed by prefixing `.with_raw_response.` to any HTTP method call.

```py
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = Anthropic()

response = anthropic.completions.with_raw_response.create(
    model="claude-2",
    max_tokens_to_sample=300,
    prompt=f"{HUMAN_PROMPT} how does a court case get to the Supreme Court?{AI_PROMPT}",
)
print(response.headers.get('X-My-Header'))

completion = response.parse()  # get the object that `completions.create()` would have returned
print(completion.completion)
```

These methods return an [`APIResponse`](https://github.com/anthropics/anthropic-sdk-python/tree/main/src/anthropic/_response.py) object.

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
