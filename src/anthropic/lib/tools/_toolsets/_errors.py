"""Errors the toolset helpers raise at your code rather than report to the model, and the SDK's own refusals.

`ToolsetUsageError` is the only exception type the tool runner lets propagate out of
a member call: it means your code used the SDK's own interface incorrectly, so the run stops.
Every other exception a member raises is reported to the model as an `is_error` result and the
loop continues. The refusals are `ToolError` subclasses, each with the SDK's own text: the model reads them as
any other `is_error` result, and your code (an `execute` override, a test) catches the subclass to tell them apart
without comparing text.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import Literal

from ._sanitize import log_safe, quoted_name
from ...._exceptions import AnthropicError
from .._beta_functions import ToolError

if TYPE_CHECKING:
    from ._runnable import ToolsetFamily  # _runnable imports this module

__all__ = [
    "ToolsetUsageError",
    "ToolsetConfigError",
    "ToolsetContractError",
    "ToolsetsFixedError",
    "ToolsetClosedError",
    "UnknownMemberError",
    "DisabledMemberError",
    "UnavailableMemberError",
    "InvalidMemberInputError",
    "URLRefusedError",
    "TabMissingError",
    "ConfirmDeclinedError",
    "ConfirmFailedError",
    "UploadRefusedError",
    "UploadNoRootsError",
    "UploadOutsideRootsError",
]


class ToolsetUsageError(AnthropicError):
    """Raised when your code uses a toolset's interface incorrectly.

    The only exception the tool runner propagates from a member call. Anything else a member
    raises becomes an `is_error` result the model can react to."""


class ToolsetConfigError(ToolsetUsageError, ValueError):
    """A construction-time mistake: an option combination the toolset cannot honour."""


class ToolsetContractError(ToolsetUsageError, TypeError):
    """Misuse of the SDK's own interface detected at call time (for example a `url_policy` that
    returns a value)."""


class ToolsetsFixedError(ToolsetContractError):
    """Raised when `add_tools()` or `remove_tools()` is given a toolset, a raw definition of one of the runner's
    toolsets, or (in `remove_tools()`) the name of one. A runner's toolsets are fixed when it is created."""

    def __init__(self, action: Literal["add", "replace", "remove"], toolset_name: str) -> None:
        method = "remove_tools" if action == "remove" else "add_tools"
        instead = (
            "build a new runner without it" if action == "remove" else "build a new runner to use a different toolset"
        )
        super().__init__(
            f"{method}() can't {action} the '{quoted_name(toolset_name)}' toolset: a tool runner's toolsets are fixed "
            f"when it is created; {instead}"
        )


class ToolsetClosedError(ToolsetUsageError, RuntimeError):
    """A member call or a `with` block on a toolset you already closed."""


# --- the SDK's own refusals -------------------------------------------------------------------------------------------


class UnknownMemberError(ToolError):
    """The refusal the model reads for a member name the toolset does not have."""

    def __init__(self, name: str, *, family: ToolsetFamily) -> None:
        super().__init__(f"Error: unknown {family} toolset member '{quoted_name(name)}'")


class DisabledMemberError(ToolError):
    """The refusal the model reads for a member your application's `configs` disabled."""

    def __init__(self, name: str) -> None:
        super().__init__(
            f"The '{name}' action is not permitted by this application's permissions and cannot be used in this session."
        )


class UnavailableMemberError(ToolError):
    """The refusal the model reads for a member the driver does not implement."""

    def __init__(self, name: str, *, family: ToolsetFamily) -> None:
        super().__init__(f"The {family} toolset member '{name}' is not available in this environment.")


class InvalidMemberInputError(ToolError):
    """The refusal the model reads when its `tool_use.input` does not fit the member. `problem` is the field and what
    is wrong with it."""

    def __init__(self, name: str, problem: str, *, family: ToolsetFamily) -> None:
        super().__init__(f"invalid input for {family} member '{name}': {problem}")


class URLRefusedError(ToolError):
    """The refusal the model reads when your `url_policy` raised something other than a `ToolError` (a `ToolError` it
    raises reaches the model as raised). `reason` is the line it reads."""

    def __init__(self, reason: str) -> None:
        # one bounded line: a reason may echo a model-written address of any length
        super().__init__(log_safe(reason))


class TabMissingError(ToolError):
    """Not raised by the SDK, which leaves a call that names a tab to the driver. Kept for code that imports it."""

    def __init__(self) -> None:
        super().__init__(
            "The tab this call was addressed to is not open; nothing was returned. Use list_tabs to see what is open."
        )


class ConfirmDeclinedError(ToolError):
    """The refusal the model reads when your `confirm` callable answered `False` for the member `name`."""

    def __init__(self, name: str) -> None:
        super().__init__(
            f"The user did not grant permission to run '{name}'. Do not retry it unless the user asks you to."
        )


class ConfirmFailedError(ToolError):
    """The refusal the model reads when your `confirm` callable raised, so no answer could be obtained for `name`."""

    def __init__(self, name: str) -> None:
        super().__init__(
            f"Permission to run '{name}' could not be obtained (the confirmation prompt failed). "
            "Do not retry it unless the user asks you to."
        )


class UploadRefusedError(ToolError):
    """The refusal the model reads for a `file_upload` the file policy, or its absence, does not admit. `reason` is
    the line it reads."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)


class UploadNoRootsError(UploadRefusedError):
    """The refusal the model reads for a `file_upload` that names paths when no upload roots are configured."""

    def __init__(self) -> None:
        super().__init__("file_upload has no configured upload roots")


class UploadOutsideRootsError(UploadRefusedError):
    """The refusal the model reads for a `file_upload` path that does not lie under a configured upload root."""

    def __init__(self) -> None:
        super().__init__("file_upload path is outside the configured upload roots")
