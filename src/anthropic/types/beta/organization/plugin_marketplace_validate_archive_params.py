from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...._types import FileTypes
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["PluginMarketplaceValidateArchiveParams"]


class PluginMarketplaceValidateArchiveParams(TypedDict, total=False):
    archive: Required[FileTypes]
    """
    A .zip of the marketplace directory (its contents at the root, or wrapped in one
    folder as a Git host's download produces), sent as a file part with a filename;
    DEFLATE- or STORE-compressed, at most 32 MB. A part sent without a filename, a
    second archive part, or any other form field is a 400; a larger archive is
    a 413.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `ce-plugins-2026-09-01` in this
    header.
    """
