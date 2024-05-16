# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated

from ...._utils import PropertyInfo
from ...message_stop_event import MessageStopEvent
from ...message_delta_event import MessageDeltaEvent
from ...message_start_event import MessageStartEvent
from ...content_block_stop_event import ContentBlockStopEvent
from .tools_beta_content_block_delta_event import ToolsBetaContentBlockDeltaEvent
from .tools_beta_content_block_start_event import ToolsBetaContentBlockStartEvent

__all__ = ["ToolsBetaMessageStreamEvent"]

ToolsBetaMessageStreamEvent = Annotated[
    Union[
        MessageStartEvent,
        MessageDeltaEvent,
        MessageStopEvent,
        ToolsBetaContentBlockStartEvent,
        ToolsBetaContentBlockDeltaEvent,
        ContentBlockStopEvent,
    ],
    PropertyInfo(discriminator="type"),
]
