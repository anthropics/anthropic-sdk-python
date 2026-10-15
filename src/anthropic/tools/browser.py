"""Browser toolset helpers for `browser_toolset_20260801`: the classes a driver subclasses, their
constructor option, context and result types, and the errors that belong to the browser toolset alone. `ToolError`
and the errors both toolsets raise are exported from `anthropic.tools`. The generated member inputs
(`BetaBrowserNavigateInput`, ... and their union `BetaBrowserMemberInput`) and wire types
(`BetaBrowserToolset20260801Param`, the `browser_state` block and its entries) are in `anthropic.types.beta`.
Documentation:
https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool (the tool) and
`browser-toolset.md` (this SDK's guide)."""

from ..lib.tools._toolsets._base import BetaScreenshotResult as BetaScreenshotResult
from ..lib.tools._toolsets._hooks import (
    BetaURLPolicy as BetaURLPolicy,
    BetaFilePolicy as BetaFilePolicy,
    BetaURLContext as BetaURLContext,
    BetaToolConfigs as BetaToolConfigs,
    BetaAsyncURLPolicy as BetaAsyncURLPolicy,
    BetaConfirmContext as BetaConfirmContext,
    BetaConfirmCallable as BetaConfirmCallable,
    BetaAsyncConfirmCallable as BetaAsyncConfirmCallable,
)
from ..lib.tools._toolsets._errors import (
    TabMissingError as TabMissingError,
    URLRefusedError as URLRefusedError,
    UploadRefusedError as UploadRefusedError,
)
from ..lib.tools._toolsets._browser import (
    BetaAbstractBrowserToolset20260801 as BetaAbstractBrowserToolset20260801,
    BetaAsyncAbstractBrowserToolset20260801 as BetaAsyncAbstractBrowserToolset20260801,
)
from ..lib.tools._toolsets._results import (
    BetaBrowserState as BetaBrowserState,
    BetaDialogDismissed as BetaDialogDismissed,
    BetaNavigationRefused as BetaNavigationRefused,
    BetaBrowserMemberResult as BetaBrowserMemberResult,
    BetaBrowserNavigateResult as BetaBrowserNavigateResult,
)
from ..lib.tools._toolsets._runnable import (
    BetaToolsetContent as BetaToolsetContent,
    BetaToolsetCallContext as BetaToolsetCallContext,
)
from ..lib.tools._toolsets._security import (
    BetaLocalFilePolicy as BetaLocalFilePolicy,
    beta_check_upload_path as beta_check_upload_path,
)

__all__ = [
    # the classes a driver subclasses
    "BetaAbstractBrowserToolset20260801",
    "BetaAsyncAbstractBrowserToolset20260801",
    # constructor options and hooks
    "BetaConfirmContext",
    "BetaToolConfigs",
    "BetaConfirmCallable",
    "BetaAsyncConfirmCallable",
    "BetaURLContext",
    "BetaURLPolicy",
    "BetaAsyncURLPolicy",
    "BetaFilePolicy",
    "BetaLocalFilePolicy",
    "beta_check_upload_path",
    # call context and content
    "BetaToolsetCallContext",
    "BetaToolsetContent",
    # results and browser state
    "BetaBrowserNavigateResult",
    "BetaScreenshotResult",
    "BetaNavigationRefused",
    "BetaDialogDismissed",
    "BetaBrowserState",
    "BetaBrowserMemberResult",
    # errors that belong to the browser toolset alone
    "URLRefusedError",
    "TabMissingError",
    "UploadRefusedError",
]
