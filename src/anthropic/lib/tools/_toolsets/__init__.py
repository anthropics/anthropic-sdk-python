"""Internal machinery for Anthropic-defined toolsets (`browser_toolset_20260801`, `computer_toolset_20260801`).

Nothing in this package is a supported import. User code imports the browser and computer
toolset classes and their option, context, result and error types from `anthropic.tools.browser` and
`anthropic.tools.computer`.
"""

from ._errors import (
    TabMissingError as TabMissingError,
    URLRefusedError as URLRefusedError,
    ToolsetUsageError as ToolsetUsageError,
    ConfirmFailedError as ConfirmFailedError,
    ToolsetClosedError as ToolsetClosedError,
    ToolsetConfigError as ToolsetConfigError,
    UnknownMemberError as UnknownMemberError,
    UploadRefusedError as UploadRefusedError,
    DisabledMemberError as DisabledMemberError,
    ConfirmDeclinedError as ConfirmDeclinedError,
    ToolsetContractError as ToolsetContractError,
    UnavailableMemberError as UnavailableMemberError,
    InvalidMemberInputError as InvalidMemberInputError,
)
from ._runnable import (
    ToolsetFamily as ToolsetFamily,
    BetaToolsetParam as BetaToolsetParam,
    BetaToolsetContent as BetaToolsetContent,
    BetaRunnableToolset as BetaRunnableToolset,
    BetaAnyRunnableToolset as BetaAnyRunnableToolset,
    BetaToolsetCallContext as BetaToolsetCallContext,
    BetaAsyncRunnableToolset as BetaAsyncRunnableToolset,
    toolset_result_block as toolset_result_block,
)

__all__ = [
    "ToolsetUsageError",
    "ToolsetClosedError",
    "ToolsetConfigError",
    "ToolsetContractError",
    "UnknownMemberError",
    "DisabledMemberError",
    "UnavailableMemberError",
    "InvalidMemberInputError",
    "URLRefusedError",
    "TabMissingError",
    "ConfirmDeclinedError",
    "ConfirmFailedError",
    "UploadRefusedError",
    "ToolsetFamily",
    "BetaToolsetContent",
    "BetaToolsetParam",
    "BetaToolsetCallContext",
    "BetaRunnableToolset",
    "BetaAnyRunnableToolset",
    "BetaAsyncRunnableToolset",
    "toolset_result_block",
]
