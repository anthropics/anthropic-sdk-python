"""The types of the browser toolset's constructor hooks: the URL policy, the file policy and the confirmation
callable. `BetaToolConfigs` is every family's and is re-exported here."""

from __future__ import annotations

from collections.abc import Callable, Sequence, Awaitable
from typing_extensions import Protocol, TypeAlias, runtime_checkable

from ._base import BetaToolConfigs
from ._inputs import BetaBrowserMemberName
from ._runnable import BetaToolsetCallContext
from ...._models import BaseModel
from ....types.beta import BetaBrowserMemberInput

__all__ = [
    "BetaURLContext",
    "BetaURLPolicy",
    "BetaAsyncURLPolicy",
    "BetaFilePolicy",
    "BetaConfirmContext",
    "BetaConfirmCallable",
    "BetaAsyncConfirmCallable",
    "BetaToolConfigs",
]


class BetaURLContext(BaseModel):
    """What a hook receives about the call it serves: the first argument of `url_policy(context, url)` and of the
    file policy's `resolve_upload_paths(context, paths)` / `resolve_upload_documents(context, document_ids)`."""

    member: BetaBrowserMemberName | None = None
    """The member being called: `navigate` for the URL policy, `file_upload` for the file policy."""

    tab_id: str | None = None
    """The tab the call named, if any."""

    tool_use_id: str | None = None
    """The model call being served, or `None` when a hook is invoked outside one."""


BetaURLPolicy: TypeAlias = Callable[[BetaURLContext, str], None]
"""The synchronous toolset's URL policy: `(context, url)`, called once for each `navigate` that has a URL, with
`url` exactly as the model wrote it, before the driver receives it (`back`, `forward` and `reload` are not checked).
Return `None` to allow, raise `ToolError` to refuse."""

BetaAsyncURLPolicy: TypeAlias = Callable[[BetaURLContext, str], Awaitable[None] | None]
"""The async toolset's URL policy: a coroutine function or a plain one. The result is awaited when it is awaitable,
like the other async hooks. Same arguments and contract as `BetaURLPolicy`."""


@runtime_checkable
class BetaFilePolicy(Protocol):
    """Controls which upload paths and document ids a `file_upload` may use and which download paths
    the model may see.

    With no file policy configured, an upload input that has a path or a document id is refused
    and download paths are never shown to the model.
    """

    def resolve_upload_paths(self, context: BetaURLContext, paths: Sequence[str]) -> list[str]:
        """Resolve each path the model asked to upload, or raise `ToolError` to refuse. The driver
        receives the returned paths in `input.paths`."""
        ...

    def resolve_upload_documents(self, context: BetaURLContext, document_ids: Sequence[str]) -> list[str]:
        """Vet each document id (a file staged with the Files API) the model asked to upload, or raise
        `ToolError` to refuse. The driver receives the returned ids in `input.document_ids`."""
        ...

    def is_path_visible(self, path: str) -> bool:
        """Whether a `download_completed` path may reach the model. Only `True` shows it; any other answer forwards the
        event without it."""
        ...


class BetaConfirmContext(BetaToolsetCallContext):
    """What `confirm` receives about the call awaiting approval: the member, its parsed input, and, through
    `tab_id` and `tab_url`, the tab the call targets (the active tab when it names none) as of the last
    `browser_state` report the SDK collected, with no page read; that is the report the model saw unless the
    call before failed. Both are `None` when that report has no such tab (anything before the first). `tab_url`
    is the URL as the model read it: the driver's string, folded to one line and held to 4,096 characters. An
    approval covers that report; the page is not read again after it. `input` holds a `file_upload`'s paths and
    document ids as the file policy returned them, and a `navigate` history word in lower case."""

    member: BetaBrowserMemberName
    input: BetaBrowserMemberInput
    tab_url: str | None = None
    tab_id: str | None = None


BetaConfirmCallable: TypeAlias = Callable[[BetaConfirmContext], bool]
BetaAsyncConfirmCallable: TypeAlias = Callable[[BetaConfirmContext], bool | Awaitable[bool]]
