from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_plugin_name_taken_error_details import BetaPluginNameTakenErrorDetails

__all__ = ["BetaPluginNameTakenError"]


class BetaPluginNameTakenError(ConflictError):
    """The marketplace already holds this name.

    `plugin_id` is the Plugin that holds it, and can be absent.
    """

    error_code: Literal["plugin_name_taken"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaPluginNameTakenErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
