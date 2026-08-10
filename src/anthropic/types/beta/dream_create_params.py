# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_dream_input_param import BetaDreamInputParam
from .beta_output_behavior_param import BetaOutputBehaviorParam
from .beta_dream_model_config_param import BetaDreamModelConfigParam

__all__ = ["DreamCreateParams", "Model"]


class DreamCreateParams(TypedDict, total=False):
    inputs: Required[Iterable[BetaDreamInputParam]]

    model: Required[Model]
    """Model identifier and configuration applied to every pipeline stage."""

    instructions: Optional[str]

    output_behavior: BetaOutputBehaviorParam
    """
    The default destination: the job creates a new output memory store as a clone of
    the memory_store input and writes the consolidated memories into it. The input
    store is never mutated.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


Model: TypeAlias = Union[str, BetaDreamModelConfigParam]
