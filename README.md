# Claude SDK for Python

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)

The Claude SDK for Python provides access to the [Claude API](https://docs.anthropic.com/en/api/) from Python applications.

## Documentation

Full documentation is available at **[platform.claude.com/docs/en/api/sdks/python](https://platform.claude.com/docs/en/api/sdks/python)**.

## Installation

```sh
pip install anthropic
```

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
    model="claude-opus-4-6",
)
print(message.content)
```

## Structured outputs

For JSON or schema-constrained responses, use `client.messages.parse()` with an `output_format`.
This keeps structured output separate from normal tool-use transcripts, so you do not need to
serialize a schema-only `tool_use` block or fabricate a `tool_result` when continuing a chat.

```python
import pydantic
from anthropic import Anthropic


class Order(pydantic.BaseModel):
    product_name: str
    price: float
    quantity: int


client = Anthropic()

parsed_message = client.messages.parse(
    model="claude-sonnet-4-5",
    messages=[
        {
            "role": "user",
            "content": "Extract the order from: 2 packs of Green Tea for 5.50 dollars each.",
        }
    ],
    max_tokens=1024,
    output_format=Order,
)

print(parsed_message.parsed_output)
```

See the runnable examples in [`examples/structured_outputs.py`](./examples/structured_outputs.py)
and [`examples/structured_outputs_streaming.py`](./examples/structured_outputs_streaming.py).

## Requirements

Python 3.9+

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
