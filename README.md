# Claude SDK for Python

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)

The Claude SDK for Python provides access to the [Claude API](https://docs.anthropic.com/en/api/) from Python applications.

## Documentation

Tool helpers (`@beta_tool`, the tool runner and `ToolError`) are documented in [tools.md](tools.md). The browser and computer toolset classes have their own guides, [browser-toolset.md](browser-toolset.md) and [computer-toolset.md](computer-toolset.md).

Full documentation is available at **[platform.claude.com/docs/en/api/sdks/python](https://platform.claude.com/docs/en/api/sdks/python)**.

## Installation

```sh
pip install anthropic
```

Upgrading from a `0.x` release? See the [v1 migration guide](MIGRATION.md).

## Getting started

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello, Claude",
        }
    ],

    model="claude-opus-5-5",
)

print(message.content)
```


## OpenTelemetry

The SDK reports each API call as an OpenTelemetry span when your application has registered a tracer provider.
It depends on `opentelemetry-api`, a required dependency, and never on an OpenTelemetry SDK.

```python
# a provider other than the registered one
client = Anthropic(open_telemetry={"tracer_provider": tracer_provider})
# no spans
quiet = Anthropic(open_telemetry=False)
# adds prompts and completions
verbose = Anthropic(open_telemetry={"traces": {"content_mode": "content"}})
# keeps the content of one span within this size
bounded = Anthropic(
    open_telemetry={"traces": {"content_mode": "content", "max_content_bytes": 65_536}}
)
# sends no trace context headers, for an application whose HTTP client instrumentation already sends them, so that
# a request does not carry them twice
unpropagated = Anthropic(open_telemetry={"propagation": False})

# sets gen_ai.conversation.id on the spans of one conversation's requests. with_options replaces the whole option,
# so start from client.open_telemetry, which has the client's
conversation = client.with_options(
    open_telemetry={**client.open_telemetry, "conversation_id": conversation_id}
)
conversation.messages.create(...)
```

A client that is given no `open_telemetry` option reads these environment variables when it is constructed: `ANTHROPIC_OPEN_TELEMETRY=false` turns its spans off, `ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE=content` adds prompts and completions, `ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES` sets `max_content_bytes`, and `ANTHROPIC_OPEN_TELEMETRY_PROPAGATION=false` sends no trace context headers.
A client that is given the option, even `{}` or a `tracer_provider` alone, reads none of them: what the option leaves out has its default (spans on, trace context headers sent, no prompts or completions, 750,000 bytes).
A copy made with `with_options` or `copy` keeps its client's option unless it is given its own.

## Requirements

Python 3.10+

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
