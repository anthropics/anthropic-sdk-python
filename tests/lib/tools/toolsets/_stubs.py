"""Stub toolsets shared by the toolset tests: they record calls and echo the member name plus input,
and raise on the `boom` / `crash` / `misuse` members."""

from __future__ import annotations

import json
from typing import Any
from typing_extensions import override

from anthropic.lib.tools import ToolError
from anthropic.lib.tools._toolsets import (
    BetaToolsetParam,
    BetaToolsetContent,
    BetaRunnableToolset,
    ToolsetContractError,
    BetaToolsetCallContext,
    BetaAsyncRunnableToolset,
)

BROWSER_ENTRY: BetaToolsetParam = {
    "type": "browser_toolset_20260801",
    "configs": {"javascript_exec": {"enabled": True}},
}


def _echo(name: str, input: object) -> str | BetaToolsetContent:
    if name == "boom":
        raise ToolError(
            [
                {"type": "text", "text": "member refused"},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "AAAA"}},
            ]
        )
    if name == "blank":
        raise ToolError([{"type": "text", "text": ""}])  # an empty text block only
    if name == "crash":
        raise RuntimeError("backend exploded")
    if name == "misuse":
        raise ToolsetContractError("the driver misused the SDK surface")
    return f"{name}:{json.dumps(input, sort_keys=True)}"


class EchoBrowserToolset(BetaRunnableToolset):
    toolset_name = "browser"

    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.contexts: list[BetaToolsetCallContext] = []
        self.closed = 0

    @override
    def to_dict(self) -> BetaToolsetParam:
        return BROWSER_ENTRY

    @override
    def call(self, context: BetaToolsetCallContext, name: str, input: object) -> str | BetaToolsetContent:
        self.calls.append((name, input))
        self.contexts.append(context)
        return _echo(name, input)

    @override
    def close(self) -> None:
        self.closed += 1
        super().close()


class AsyncEchoBrowserToolset(BetaAsyncRunnableToolset):
    toolset_name = "browser"

    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.contexts: list[BetaToolsetCallContext] = []
        self.closed = 0

    @override
    def to_dict(self) -> BetaToolsetParam:
        return BROWSER_ENTRY

    @override
    async def call(self, context: BetaToolsetCallContext, name: str, input: object) -> str | BetaToolsetContent:
        self.calls.append((name, input))
        self.contexts.append(context)
        return _echo(name, input)

    @override
    async def close(self) -> None:
        self.closed += 1
        await super().close()
