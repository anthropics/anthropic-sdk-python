"""Loaded as an early pytest plugin (`-p tests._alias_httpx` in `pyproject.toml`).

`respx` mocks `httpx`, while this SDK is built on `httpx2`, so we make `import httpx` (and `httpcore`)
resolve to `httpx2` (and `httpcore2`) before `respx` is imported, which lets it mock our client.
"""

import httpx2

httpx2.alias_httpx()
