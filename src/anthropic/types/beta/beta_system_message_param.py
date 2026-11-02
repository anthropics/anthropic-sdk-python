from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_text_block_param import BetaTextBlockParam
from .beta_request_tool_removal_block_param import BetaRequestToolRemovalBlockParam
from .beta_request_tool_addition_block_param import BetaRequestToolAdditionBlockParam
from .beta_system_message_output_config_param import BetaSystemMessageOutputConfigParam

__all__ = ["BetaSystemMessageParam", "ContentBlock"]

ContentBlock: TypeAlias = Union[BetaTextBlockParam, BetaRequestToolAdditionBlockParam, BetaRequestToolRemovalBlockParam]


class BetaSystemMessageParam(TypedDict, total=False):
    role: Required[Literal["system"]]

    clear_at: Optional[Literal["next_user_message", "never"]]
    """How long this system message's text stays in front of the model.

    `"never"` (the default) renders it on every request that includes it.
    `"next_user_message"` renders it only for the user turn it follows: once a later
    `role: "user"` message exists in `messages` the message stays in the array (send
    it unchanged) but is no longer shown to the model. Only permitted on
    `role: "system"` messages.
    """

    content: Union[str, Iterable[ContentBlock]]

    output_config: Optional[BetaSystemMessageOutputConfigParam]
    """Per-message output configuration on a role:"system" input message.

    Fields here apply per-turn; `format` remains top-level only. An empty `{}` is
    accepted on a message that carries content; a message with neither content nor
    output_config fields is rejected.
    """
