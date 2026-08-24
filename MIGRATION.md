# Migrating to v1

- [Upgrading](#upgrading)
- [Environment requirements](#environment-requirements)
- [The SDK is built on `httpx2`](#the-sdk-is-built-on-httpx2)
- [`.with_raw_response` returns the new response classes](#with_raw_response-returns-the-new-response-classes)
- [Removed: the legacy Text Completions API](#removed-the-legacy-text-completions-api)
- [Removed: deprecated request parameters](#removed-deprecated-request-parameters)
- [Removed: deprecated type aliases and exports](#removed-deprecated-type-aliases-and-exports)
- [Removed: deprecated helper arguments and behaviour](#removed-deprecated-helper-arguments-and-behaviour)
- [Header names are matched case-insensitively](#header-names-are-matched-case-insensitively)
- [bytes header values no longer work](#bytes-header-values-no-longer-work)
- [Bedrock: a region is now required](#bedrock-a-region-is-now-required)
- [Bedrock: unknown streaming events are skipped](#bedrock-unknown-streaming-events-are-skipped)
- [Quick reference](#quick-reference)

## Upgrading

```sh
pip install --upgrade "anthropic>=1,<2"
```

If you use Claude Code, the fastest route through the rest of this guide is to let it do the edits:
run `/claude-api upgrade python` in your project and review the diff.

A type checker (`pyright` / `mypy`) will flag almost everything below as an error after upgrading, which makes
it a good checklist even if you don't normally run one.

## Environment requirements

The minimum supported Python version has increased from 3.9 to 3.10.

Nothing else about your environment needs to change. In particular Pydantic v1 and v2 both remain supported.

## The SDK is built on `httpx2`

The SDK's HTTP layer moved from `httpx`, which is no longer actively maintained, to [`httpx2`](https://github.com/pydantic/httpx2) - an API-compatible fork maintained by the Pydantic team.

`httpx2` is a drop-in continuation of `httpx`, with the same classes, same behaviour, and security fixes included.
This only affects code that hands `httpx` objects **to** the SDK or inspects the ones it gets **back**.

If you only ever pass plain values (`timeout=30.0`, `max_retries=3`, …) there is _likely_ nothing for you to do.
The exception is tooling that hooks `httpx` itself rather than your code — tracing / APM instrumentation and HTTP
mocking libraries. Those keep working but silently stop seeing the SDK's requests until you point them at `httpx2`;
see [Tracing, instrumentation and mocking libraries](#tracing-instrumentation-and-mocking-libraries) below.

### Custom HTTP clients, transports, timeouts and limits

Anything you construct from `httpx` and pass to the client must now come from `httpx2`. The simplest edit is
to alias the import; the SDK's own re-exports (`anthropic.Timeout`, `anthropic.DefaultHttpxClient`,
`anthropic.DefaultAsyncHttpxClient`, `anthropic.DefaultAioHttpClient`) already point at `httpx2` and keep working
unchanged.

```python
# Before
import httpx
from anthropic import Anthropic, DefaultHttpxClient

client = Anthropic(
    timeout=httpx.Timeout(60.0, connect=5.0),
    http_client=DefaultHttpxClient(
        proxy="http://my.proxy.example",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)

# After
import httpx2 as httpx  # or `import httpx2` and rename the references
from anthropic import Anthropic, DefaultHttpxClient

client = Anthropic(
    timeout=httpx.Timeout(60.0, connect=5.0),
    http_client=DefaultHttpxClient(
        proxy="http://my.proxy.example",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

Passing an `httpx.Client` / `httpx.AsyncClient` (from the old package) as `http_client=` raises a `TypeError`
at construction time, so this cannot fail silently.

If you would rather not edit imports — or other code in your application still imports `httpx` and has to
share clients, transports or exception types with the SDK — call `httpx2.alias_httpx()` once at start-up instead.
It makes `import httpx` (and `import httpcore`) resolve to `httpx2` (and `httpcore2`) for the whole process. It has
to run before anything imports `httpx` (it raises a `RuntimeError` otherwise), and it is meant for applications:
a library should never call it on behalf of its users.

```python
# the very first lines of your entry point
import httpx2

httpx2.alias_httpx()

import httpx  # this is now the httpx2 module

assert httpx.Client is httpx2.Client
```

### Response and error objects

The objects the SDK returns are now `httpx2` types: `APIStatusError.response`, `APIConnectionError.request`,
`response.http_response` / `.headers` / `.url` on raw responses, and the `response=` argument your custom
`http_client` event hooks receive. They have exactly the same attributes as before; only `isinstance` checks and
type annotations that name `httpx.Response` / `httpx.Request` / `httpx.Headers` need to switch to `httpx2`.

```python
# Before
def log_failure(err: anthropic.APIStatusError) -> None:
    response: httpx.Response = err.response
    print(response.status_code, response.headers.get("request-id"))


# After
def log_failure(err: anthropic.APIStatusError) -> None:
    response: httpx2.Response = err.response
    print(response.status_code, response.headers.get("request-id"))
```

### `aiohttp` support

`pip install anthropic[aiohttp]` and `http_client=DefaultAioHttpClient()` work as they did before.
However the `aiohttp` extra no longer installs the `httpx_aiohttp` package as it now ships inside the SDK.

### Tracing, instrumentation and mocking libraries

Libraries that observe or stub HTTP traffic by patching `httpx` — for example OpenTelemetry's
`HTTPXClientInstrumentor`, Sentry's `httpx` integration, [`respx`](https://lundberg.github.io/respx/),
`pytest-httpx` or `vcrpy` — patch the `httpx` package, which the SDK no longer uses. These libraries can silently
fail, making it difficult to identify failure points. You can holistically fix this by running `httpx2.alias_httpx()`
before anything else imports `httpx`.

In an application, call it at the top of your entry point as shown above. Under pytest, an early plugin is the
least intrusive way to run it before `respx` / `pytest-httpx` and your test modules are imported:

```python
# tests/_alias_httpx.py
import httpx2

httpx2.alias_httpx()  # makes `import httpx` / `import httpcore` resolve to httpx2 / httpcore2
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "-p tests._alias_httpx"
pythonpath = ["."]
```

### Removed old `httpx` re-exports

The top-level `anthropic.Transport` and `anthropic.ProxiesTypes` exports were unused aliases of `httpx` types and
are gone. Use `httpx2.BaseTransport`, `httpx2.AsyncBaseTransport` and `httpx2.Proxy` (or a proxy URL string) directly.

## `.with_raw_response` returns the new response classes

`.with_raw_response` used to return a `LegacyAPIResponse` class for both the sync and the async client. It now returns
the same `APIResponse` / `AsyncAPIResponse` classes that `.with_streaming_response` already used. Two things change:

**On the async client, reading the response is now async.** `parse()`, `read()`, `text()` and `json()` are
coroutines on `AsyncAPIResponse`.

```python
# Before
response = await client.messages.with_raw_response.create(...)
print(response.headers["request-id"])
message = response.parse()

# After
response = await client.messages.with_raw_response.create(...)
print(response.headers["request-id"])  # metadata is still plain attribute access
message = await response.parse()
```

**`.text` and `.content` became methods.** This applies to the sync client too. The new classes also expose
`json()` and the `iter_bytes()` / `iter_text()` / `iter_lines()` iterators directly, which previously meant
reaching for the underlying `response.http_response`.

| `LegacyAPIResponse` (before)                                                                      | `APIResponse` (sync, after)                                | `AsyncAPIResponse` (async, after)             |
| ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------- |
| `response.parse()`                                                                                | `response.parse()`                                         | `await response.parse()`                      |
| `response.text`                                                                                   | `response.text()`                                          | `await response.text()`                       |
| `response.content`                                                                                | `response.read()`                                          | `await response.read()`                       |
| — (only `response.http_response.json()`)                                                          | `response.json()`                                          | `await response.json()`                       |
| — (only `response.http_response.iter_bytes()` …)                                                  | `response.iter_bytes()` / `.iter_text()` / `.iter_lines()` | `async for chunk in response.iter_bytes():` … |
| `.headers`, `.status_code`, `.url`, `.request_id`, `.retries_taken`, `.http_response`, `.elapsed` | unchanged                                                  | unchanged                                     |

## Removed: the legacy Text Completions API

`client.completions.create()` (the `/v1/complete` endpoint), its types (`Completion`,
`CompletionCreateParams`) and the `anthropic.HUMAN_PROMPT` / `anthropic.AI_PROMPT` prompt constants have been
removed. Every current model is served through the Messages API, which has been the recommended interface since
2023 — see [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
if you still have code calling the legacy endpoint.

## Removed: deprecated request parameters

These parameters were deprecated by the API and are no longer accepted by the generated methods (passing them is
a `TypeError`, and a type checker flags it). They are also gone from the per-request `params` of
`messages.batches.create()`, where a type checker flags the key but the SDK still forwards it at runtime:

| Method(s)                                                                                                                                                                                       | Removed parameter               | Use instead                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `messages.create()`, `messages.stream()`, `messages.parse()` and their `beta.messages` counterparts, `beta.messages.tool_runner()`, and the per-request `params` of `messages.batches.create()` | `temperature`, `top_p`, `top_k` | Remove them. Current models do not use these sampling parameters; for an older model that still does, pass them through `extra_body` (see below).                                                                                                                                                                                          |
| `beta.messages.create()`, `beta.messages.count_tokens()`, batch request params                                                                                                                  | `output_format`                 | `output_config={"format": {...}}` — see [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs). The `output_format=MyModel` argument of the `parse()` / `stream()` / `count_tokens()` / `tool_runner()` **helpers** still takes a type; those helpers no longer accept a schema dict there either. |

```python
# Before
client.beta.messages.create(
    ...,
    temperature=0.2,
    output_format={"type": "json_schema", "schema": Order.model_json_schema()},
)

# After
client.beta.messages.create(
    ...,
    output_config={"format": {"type": "json_schema", "schema": Order.model_json_schema()}},
)
# or let the helper build the schema and parse the result:
client.beta.messages.parse(..., output_format=Order)
```

The sampling parameters are only gone from the method signatures, not from the API: models that predate the
change still honour them. If you are pinned to such a model and really need a sampling setting, pass it through
`extra_body`, which is merged into the request JSON as-is (for `messages.batches.create()`, put the key straight into
the request's `params` dict):

```python
# Before
client.messages.create(..., model="claude-sonnet-4-6", temperature=0.2)

# After
client.messages.create(..., model="claude-sonnet-4-6", extra_body={"temperature": 0.2})
```

The `output_format=` argument of `messages.parse()` / `stream()` / `count_tokens()` and `beta.messages.parse()` /
`stream()` / `tool_runner()` now only accepts a **type**. `messages.stream()`,
`messages.count_tokens()` and `beta.messages.stream()` used to accept a raw schema dict there too and forward it as
`output_config.format`; that form raises a `TypeError` now. Pass schema dicts via `output_config` and keep
`output_format=` for classes — the `DeprecationWarning` that `beta.messages.parse()` / `stream()` / `tool_runner()` used to
emit for the class form is gone, since that is now the only form they take:

```python
# Before
client.messages.count_tokens(..., output_format={"type": "json_schema", "schema": {...}})
client.messages.count_tokens(..., output_format=Order)

# After
client.messages.count_tokens(..., output_config={"format": {"type": "json_schema", "schema": {...}}})
client.messages.count_tokens(..., output_format=Order)  # unchanged
```

## Removed: deprecated type aliases and exports

| Removed                                                                                                 | Replacement                                                                         |
| ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `anthropic.types.beta.BetaBase64PDFBlockParam`                                                          | `anthropic.types.beta.BetaRequestDocumentBlockParam`                                |
| `anthropic.Transport`, `anthropic.ProxiesTypes` (and `anthropic._types.AsyncTransport` / `ProxiesDict`) | `httpx2.BaseTransport`, `httpx2.Proxy` (`httpx2.AsyncBaseTransport`)                |
| `anthropic.HUMAN_PROMPT`, `anthropic.AI_PROMPT`                                                         | none — see [the Text Completions section](#removed-the-legacy-text-completions-api) |
| `anthropic.lib.tools.agent_toolset.READ_MAX_BYTES`                                                      | `anthropic.lib.tools.agent_toolset.DEFAULT_MAX_FILE_BYTES`                          |

## Removed: deprecated helper arguments and behaviour

### `messages.parse(stream=True)`

`parse()` always performs a non-streaming request; the `stream` argument never worked and has been removed from
`messages.parse()` / `beta.messages.parse()`. Use the streaming helper, which supports the same structured
output types:

```python
# Before (which would crash)
client.messages.parse(..., output_format=Order, stream=True)

# After
with client.messages.stream(..., output_format=Order) as stream:
    for event in stream:
        ...
    order = stream.get_final_message().parsed_output
```

### `tool_runner(compaction_control=...)`

Client-side compaction in the tool runner (the `compaction_control=` argument and the `CompactionControl` dict)
has been removed in favour of server-side compaction, which summarises the conversation inside the API instead of
with an extra client round-trip:

```python
# Before
runner = client.beta.messages.tool_runner(
    ...,
    compaction_control={"enabled": True, "context_token_threshold": 100_000},
)

# After
runner = client.beta.messages.tool_runner(
    ...,
    betas=["compact-2026-01-12"],
    context_management={
        "edits": [
            {"type": "compact_20260112", "trigger": {"type": "input_tokens", "value": 100_000}}
        ]
    },
)
```

The trigger threshold must be at least 50,000 tokens. See [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
for the other options (`pause_after_compaction`, custom `instructions`).

### Raw bytes as `body=` on `client.get/post/put/patch/delete`

The low-level request methods accepted `bytes` for `body=` with a deprecation warning. `body=` is now always
JSON-serialised and raw payloads go through `content=` (which also accepts iterators for streaming uploads):

```python
# Before
client.post("/v1/example", body=b"raw payload", cast_to=httpx.Response)

# After
client.post("/v1/example", content=b"raw payload", cast_to=httpx2.Response)
```

### `isinstance(stream, anthropic.Stream)` for message streams

`MessageStream` / `AsyncMessageStream` (what `client.messages.stream()` yields) stopped inheriting from
`Stream` / `AsyncStream` many releases ago; a compatibility shim kept `isinstance()` checks passing with a
`DeprecationWarning`. The shim is gone, so such checks now return `False`. Check for the concrete classes instead:

```python
# Before
from anthropic import Stream

if isinstance(obj, Stream):
    ...

# After
from anthropic.lib.streaming import MessageStream

if isinstance(obj, MessageStream):
    ...  # or `Stream` if you really mean a raw `create(stream=True)` stream
```

## Header names are matched case-insensitively

HTTP header names are case-insensitive, and the SDK now treats them that way everywhere it merges headers. An entry
in `default_headers`, `extra_headers`, `with_options(default_headers=...)` or the `ANTHROPIC_CUSTOM_HEADERS`
environment variable replaces a header of the same name whatever its casing — including the headers the SDK sets
itself — instead of being sent alongside it, and `omit` removes one the same way.

```python
from anthropic import Anthropic, omit

client = Anthropic(default_headers={"USER-AGENT": "my-app/1.0"})
client.messages.create(..., extra_headers={"x-api-key": other_key, "X-Stainless-Timeout": omit})

# Before: sent `User-Agent: Anthropic/Python ...` and `USER-AGENT: my-app/1.0`, both API keys,
#         and still sent `x-stainless-timeout`
# After:  sends `USER-AGENT: my-app/1.0`, only `x-api-key: <other_key>`, and no `x-stainless-timeout` header
```

If you relied on two casings of a name producing two header lines, send one comma-joined value instead.

## `bytes` header values no longer work

Previously even though the type annotations did not allow it, you could pass `bytes` as header values, this now raises an error:

```python
# Before (worked despite the type error)
client.messages.create(..., extra_headers={"X-Signature": signature_bytes})

# After
client.messages.create(..., extra_headers={"X-Signature": signature_bytes.decode()})
```

## Bedrock: a region is now required

`AnthropicBedrock` / `AsyncAnthropicBedrock` used to log a warning and silently fall back to `us-east-1` when no
AWS region could be found. They now raise a `ValueError` at construction time instead.

The region is resolved from, in order:

- the `aws_region=` argument
- the `AWS_REGION` / `AWS_DEFAULT_REGION` environment variables
- the configuration of the boto3 session for the given `aws_profile` (previously the profile argument was ignored for region lookup).

```python
# Before — implicitly us-east-1 if nothing was configured
client = AnthropicBedrock()

# After
client = AnthropicBedrock(aws_region="us-east-1")  # or export AWS_REGION / configure your profile
```

## Bedrock: unknown streaming events are skipped

Previously all streaming events that the Bedrock API returned would be yielded by the SDK, now they are skipped.

The only known case this affects is an `amazon-bedrock-invocationMetrics` event.

If you made use of this event please open an issue to let us know.

## Quick reference

| You have…                                                                             | Do this                                                                           |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Python 3.9                                                                            | upgrade to Python ≥ 3.10                                                          |
| `import httpx` objects passed to / received from the SDK                              | `import httpx2 as httpx` (or rename); annotations `httpx.X` → `httpx2.X`          |
| `respx` / `pytest-httpx` / `vcrpy`, or OpenTelemetry / Sentry `httpx` instrumentation | run `httpx2.alias_httpx()` before anything imports `httpx`                        |
| `httpx_aiohttp` in your requirements                                                  | drop it; `anthropic[aiohttp]` is enough                                           |
| `await client.….with_raw_response.…()` then `.parse()` / `.text` / `.content`         | `await response.parse()` / `await response.text()` / `await response.read()`      |
| sync `.with_raw_response` then `.text` / `.content`                                   | `response.text()` / `response.read()`                                             |
| `client.completions.create()`, `HUMAN_PROMPT`, `AI_PROMPT`                            | move to `client.messages.create()`                                                |
| `temperature=` / `top_p=` / `top_k=` on message methods                               | remove; use `extra_body={"temperature": ...}` if an older model still needs it    |
| `output_format={...}` (a schema dict) on any message method or helper                 | `output_config={"format": {...}}`; helpers keep `output_format=Model` for a class |
| `BetaBase64PDFBlockParam`                                                             | `BetaRequestDocumentBlockParam`                                                   |
| `anthropic.Transport` / `ProxiesTypes` (or `anthropic._types.AsyncTransport`)         | `httpx2.BaseTransport` / `Proxy` / `AsyncBaseTransport`                           |
| `messages.parse(stream=True)`                                                         | `messages.stream(...)`                                                            |
| `tool_runner(compaction_control=...)`                                                 | server-side `context_management` compaction                                       |
| `client.post(..., body=b"...")`                                                       | `content=b"..."`                                                                  |
| `isinstance(x, Stream)` meant for message streams                                     | `isinstance(x, MessageStream)`                                                    |
| two casings of one header name across `default_headers` / `extra_headers`             | the later one now replaces the earlier; join the values yourself if you need both |
| `bytes` header values                                                                 | `.decode()` them — header values must be `str`                                    |
| `AnthropicBedrock()` with no region configured                                        | pass `aws_region=` or set `AWS_REGION`                                            |
| `agent_toolset.READ_MAX_BYTES`                                                        | `DEFAULT_MAX_FILE_BYTES`                                                          |
