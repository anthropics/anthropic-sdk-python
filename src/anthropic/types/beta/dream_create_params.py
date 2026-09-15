from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_dream_input_param import BetaDreamInputParam
from .beta_output_behavior_param import BetaOutputBehaviorParam
from .beta_dream_model_config_param import BetaDreamModelConfigParam

__all__ = ["DreamCreateParams", "Model"]


class DreamCreateParams(TypedDict, total=False):
    inputs: Required[Iterable[BetaDreamInputParam]]

    model: Required[Model]

    instructions: Optional[str]

    output_behavior: BetaOutputBehaviorParam

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str


Model: TypeAlias = Union[str, BetaDreamModelConfigParam]
