"""Every place a page- or model-supplied string is cleaned or cut before it reaches the model, a log, or an
SDK-written line, in one module so what each does and how they differ can be read side by side.

- `one_line`: any page- or model-supplied value that goes into one line of text (a title, a download error, a
  field of a confirmation line): line breaks, controls and bidi characters folded to a space, a lone surrogate to
  U+FFFD, trimmed, cut to the API's field limit. `log_safe` and `quoted_name` are the same, cut short, for a log
  record or a name echoed inside quotes.
- `error_text` / `error_text_content`: an exception's text as an `is_error` result reports it (as a function
  tool's does), and the text-only content such a result may hold.
- `bounded_tab_url`: a tab's or download's reported URL folded to one line and held to the field limit.
"""

from __future__ import annotations

import re
import copy

from ....types.beta import BetaTextBlockParam
from .._beta_functions import BetaFunctionToolResultType

__all__ = [
    "FIELD_MAX",
    "well_formed",
    "folded",
    "one_line",
    "log_safe",
    "quoted_name",
    "error_text",
    "error_text_content",
    "bounded_tab_url",
]

# anything that would break or reorder the one line a page-supplied value goes into
LINE_UNSAFE = "\x00-\x1f\x7f-\x9f\u061c\u200e\u200f\u2028\u2029\u202a-\u202e\u2066-\u2069"
LINE_UNSAFE_RE = re.compile(f"[{LINE_UNSAFE}]+")
# An unpaired surrogate cannot be encoded as UTF-8: in a page-chosen string it would fail every request for as long
# as the driver keeps reporting it. Folded to U+FFFD wherever page text is cleaned.
LONE_SURROGATE_RE = re.compile("[\ud800-\udfff]")


def well_formed(text: str) -> str:
    """`text` with each unpaired surrogate replaced by U+FFFD, so it can be sent."""
    return LONE_SURROGATE_RE.sub("\ufffd", text)


FIELD_MAX = 4096
"""The API's limit for a text field of the block, for a URL, and the most of an exception's text an `is_error`
result includes."""
LOG_MAX = 200


def folded(text: str) -> str:
    """`text` on one line, not yet cut: line breaks, control and bidi characters folded to spaces, a lone surrogate to
    U+FFFD, the ends trimmed. For a value that is checked before it is bounded (`one_line` is this, then the cut)."""
    return LINE_UNSAFE_RE.sub(" ", well_formed(text)).strip()


def one_line(text: str, limit: int = FIELD_MAX) -> str:
    """A page- or model-supplied text on one line the model or an operator reads: a tab's title, a download's error, a
    field of a member's confirmation line. `folded`, then cut to `limit`, since nothing else bounds it."""
    return folded(text)[:limit]


def log_safe(name: str | None) -> str:
    """A model- or page-supplied name for a log record or an SDK-written error text: `one_line`, cut short."""
    return one_line(str(name), LOG_MAX)


def quoted_name(name: str | None) -> str:
    """A model-chosen name as it is echoed inside single quotes in a text the model reads: one line, cut short, and
    without the quotes and runs of spaces that would let it pose as the text around it."""
    return re.sub("[' ]+", " ", log_safe(name)).strip()


def error_text(exc: BaseException) -> str:
    """`repr(exc)` as the `is_error` result the model reads, well formed and cut to the field limit: a
    driver's exception can embed a page-sized payload (a request URL, a script dump)."""
    return well_formed(repr(exc))[:FIELD_MAX]


def error_text_content(content: BetaFunctionToolResultType) -> str | list[BetaTextBlockParam]:
    """The text blocks of a `ToolError`'s content. Deliberate: the API accepts only text on an `is_error` result and
    answers anything else with a 400 that ends the run, so an image a member attached to its refusal is dropped here
    rather than ending the run, and the refusal's text still reaches the model."""
    if isinstance(content, str):
        return well_formed(content)

    # The API rejects an `is_error` result whose content is empty or holds a non-text block. Empty text blocks are
    # dropped too, so an error with no text left gets the placeholder from `toolset_result_block`.
    kept: list[BetaTextBlockParam] = []
    for block in content:
        if block["type"] == "text" and block["text"]:
            block = copy.copy(block)
            block["text"] = well_formed(block["text"])
            kept.append(block)
    return kept


def bounded_tab_url(url: str) -> str:
    """A tab's or download's URL as the model reads it: folded to one line, not parsed, held to `FIELD_MAX`. A longer
    one becomes `…` plus its first `FIELD_MAX - 1` characters, so a page padding its URL leaves no host to parse."""
    line = folded(url)
    return line if len(line) <= FIELD_MAX else "\u2026" + line[: FIELD_MAX - 1]
