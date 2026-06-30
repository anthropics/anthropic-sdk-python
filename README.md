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

## File uploads

Request methods that accept `files` use the same tuple format as
[httpx](https://www.python-httpx.org/advanced/clients/#multipart-file-encoding):
`("filename", file_or_bytes, "content/type")`.

Skill uploads require each filename to include a single top-level directory that
contains `SKILL.md`. That directory name must exactly match the `name` field in
`SKILL.md`. For example, if `SKILL.md` contains `name: greeting`, upload it as
`greeting/SKILL.md`, not just `SKILL.md`:

```python
with open("SKILL.md", "rb") as skill_file:
    client.beta.skills.create(
        display_title="Greeting skill",
        files=[("greeting/SKILL.md", skill_file, "text/markdown")],
    )
```

For a skill directory on disk, `anthropic.lib.files_from_dir()` can build the
proper paths for you:

```python
from anthropic.lib import files_from_dir

client.beta.skills.create(
    display_title="Greeting skill",
    files=files_from_dir("greeting"),
)
```

## Requirements

Python 3.9+

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
