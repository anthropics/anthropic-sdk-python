"""Tracking for SDK helper usage via the x-stainless-helper header.

This module is the single source of truth for the helper-telemetry header
keys and the closed tag vocabulary. The append-don't-clobber merge for the
header itself lives in :func:`anthropic._base_client.merge_headers`; here
we only carry the constants and the per-object tagging machinery.
"""

from __future__ import annotations

from typing import Any, cast
from typing_extensions import Literal

__all__ = [
    "STAINLESS_HELPER_HEADER",
    "STAINLESS_HELPER_METHOD_HEADER",
    "STAINLESS_STREAM_HELPER_HEADER",
    "HELPER_METHOD_STREAM",
    "StainlessHelperHeaderValue",
    "helper_header",
    "tag_helper",
    "get_helper_tag",
    "collect_helpers",
    "stainless_helper_header",
    "stainless_helper_header_from_file",
]


STAINLESS_HELPER_HEADER = "x-stainless-helper"
"""Telemetry header naming the SDK helper(s) a request came from.

Always this lowercase form. ``merge_headers`` matches this key
case-insensitively for its append semantics, but a single canonical casing
keeps every call site greppable and avoids two literal casings of the same
key reaching a plain dict merge anywhere upstream of it.
"""

STAINLESS_HELPER_METHOD_HEADER = "x-stainless-helper-method"
"""Telemetry header naming the SDK method (e.g. ``stream``) in use."""

STAINLESS_STREAM_HELPER_HEADER = "x-stainless-stream-helper"
"""Telemetry header naming the streaming surface (e.g. ``beta.messages``)."""

HELPER_METHOD_STREAM = "stream"


StainlessHelperHeaderValue = Literal[
    "beta.messages.parse",
    "BetaToolRunner",
    "compaction",
    "environments-work-poller",
    "environments-worker",
    "fallback-refusal-middleware",
    "mcp_content",
    "mcp_message",
    "mcp_resource_to_content",
    "mcp_resource_to_file",
    "mcp_tool",
    "messages.parse",
    "session-tool-runner",
]
"""The closed set of helper telemetry tags, shared verbatim across SDKs.

Constrained so a typo at any call site is a type error rather than silently
mistagged telemetry. Existing values keep their original spellings — telemetry
consumers match on them, so renames lose history. New tags are hyphenated
lowercase; add them here (and to the matching set in every other SDK) before
using them.
"""


def helper_header(value: StainlessHelperHeaderValue) -> dict[str, str]:
    """The ``x-stainless-helper: <value>`` header dict, for passing into a
    ``merge_headers`` call or as ``extra_headers``/``default_headers``.

    Typing keeps the value drawn from the closed vocabulary above.
    """
    return {STAINLESS_HELPER_HEADER: value}


_HELPER_ATTR = "_stainless_helper"


def tag_helper(obj: Any, name: StainlessHelperHeaderValue) -> None:
    """Mark an object as created by a named SDK helper."""
    try:
        object.__setattr__(obj, _HELPER_ATTR, name)
    except (AttributeError, TypeError):
        pass


def get_helper_tag(obj: object) -> str | None:
    """Get the helper name from an object, if any."""
    return getattr(obj, _HELPER_ATTR, None)  # type: ignore[return-value]


def collect_helpers(
    tools: Any = None,
    messages: Any = None,
) -> list[str]:
    """Collect deduplicated helper names from tools and messages."""
    helpers: list[str] = []

    def _add(tag: str | None) -> None:
        if tag is not None and tag not in helpers:
            helpers.append(tag)

    if tools:
        for tool in tools:
            _add(get_helper_tag(tool))

    if messages:
        for message in messages:
            _add(get_helper_tag(message))

            # Check content blocks within messages
            if isinstance(message, dict):
                blocks: Any = cast(dict[str, Any], message).get("content")
            else:
                blocks = getattr(message, "content", None)
            if isinstance(blocks, list):
                for block in cast(list[object], blocks):
                    _add(get_helper_tag(block))

    return helpers


def stainless_helper_header(
    tools: Any = None,
    messages: Any = None,
) -> dict[str, str]:
    """Build x-stainless-helper header dict from tools and messages.

    Returns an empty dict if no helpers are found.
    """
    helpers = collect_helpers(tools, messages)
    if not helpers:
        return {}
    return {STAINLESS_HELPER_HEADER: ", ".join(helpers)}


def stainless_helper_header_from_file(file: object) -> dict[str, str]:
    """Build x-stainless-helper header dict from a file object."""
    tag = get_helper_tag(file)
    if tag is None:
        return {}
    return {STAINLESS_HELPER_HEADER: tag}
