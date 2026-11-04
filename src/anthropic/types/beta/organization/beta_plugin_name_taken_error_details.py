from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginNameTakenErrorDetails"]


class BetaPluginNameTakenErrorDetails(BaseModel):
    """The marketplace already holds this name.

    `plugin_id` is the Plugin that holds it, and can be absent.
    """

    error_code: Literal["plugin_name_taken"]

    plugin_id: Optional[str] = None
