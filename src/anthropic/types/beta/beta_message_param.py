# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_content_block_param import BetaContentBlockParam
from .beta_system_message_output_config_param import BetaSystemMessageOutputConfigParam

__all__ = ["BetaMessageParam"]


class BetaMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[BetaContentBlockParam]]]

    role: Required[Literal["user", "assistant", "system"]]

    clear_at: Optional[Literal["next_user_message", "never"]]
    """How long this system message's text stays in front of the model.

    `"never"` (the default) renders it on every request that includes it.
    `"next_user_message"` renders it only for the user turn it follows: once a later
    `role: "user"` message exists in `messages` the message stays in the array (send
    it unchanged) but is no longer shown to the model. Only permitted on
    `role: "system"` messages.
    """

    output_config: Optional[BetaSystemMessageOutputConfigParam]
    """Per-message output configuration on a role:"system" input message.

    Fields here apply per-turn; `format` remains top-level only. An empty `{}` is
    accepted on a message that carries content; a message with neither content nor
    output_config fields is rejected.
    """
