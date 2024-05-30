# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated

from ...._utils import PropertyInfo
from ...raw_message_stop_event import RawMessageStopEvent
from ...raw_message_delta_event import RawMessageDeltaEvent
from ...raw_message_start_event import RawMessageStartEvent
from ...raw_content_block_stop_event import RawContentBlockStopEvent
from .raw_tools_beta_content_block_delta_event import RawToolsBetaContentBlockDeltaEvent
from .raw_tools_beta_content_block_start_event import RawToolsBetaContentBlockStartEvent

__all__ = ["RawToolsBetaMessageStreamEvent"]

RawToolsBetaMessageStreamEvent = Annotated[
    Union[
        RawMessageStartEvent,
        RawMessageDeltaEvent,
        RawMessageStopEvent,
        RawToolsBetaContentBlockStartEvent,
        RawToolsBetaContentBlockDeltaEvent,
        RawContentBlockStopEvent,
    ],
    PropertyInfo(discriminator="type"),
]
