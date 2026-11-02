from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginContentScan"]


class BetaPluginContentScan(BaseModel):
    assessment: Optional[Literal["fail", "pass", "unknown", "warn"]] = None
    """The scan's verdict; set only when `status` is `completed`.

    A `warn` can mean a `fail` that was allowed in claude.ai.
    """

    reason: Optional[str] = None
    """
    The primary mechanism behind a `warn` or `fail`, such as `credential-exposure`
    or `guardrail-tampering`; a mechanism this API does not yet name reads as
    `other`. Null on a `pass`, whenever `assessment` is null, and when no mechanism
    is reported for the verdict.
    """

    status: Literal["completed", "errored", "processing"]
    """
    `processing` while a scan runs, `completed` when it ran to completion, `errored`
    when it could not run. Once a scan of the version has completed, `content_scan`
    describes the newest completed scan, even while a later scan runs. While the
    scan outcome cannot be read, `status` is `errored` instead.
    """
