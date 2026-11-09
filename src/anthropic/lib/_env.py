from __future__ import annotations

import os
from collections.abc import Mapping


def with_environment_headers(default_headers: Mapping[str, str] | None) -> Mapping[str, str] | None:
    """Adds the headers of `ANTHROPIC_CUSTOM_HEADERS` to `default_headers`, which win, as `Anthropic` does."""
    custom_headers_env = os.environ.get("ANTHROPIC_CUSTOM_HEADERS")
    if custom_headers_env is None:
        return default_headers

    parsed: dict[str, str] = {}
    for line in custom_headers_env.split("\n"):
        colon = line.find(":")
        if colon >= 0:
            parsed[line[:colon].strip()] = line[colon + 1 :].strip()

    return {**parsed, **(default_headers or {})}
