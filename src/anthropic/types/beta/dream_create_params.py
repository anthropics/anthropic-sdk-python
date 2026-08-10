# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_dream_input_param import BetaDreamInputParam
from .beta_dream_model_config_param import BetaDreamModelConfigParam

__all__ = [
    "DreamCreateParams",
    "Model",
    "OutputBehavior",
    "OutputBehaviorBetaOutputBehaviorCreateNew",
    "OutputBehaviorBetaOutputBehaviorUpdateExisting",
]


class DreamCreateParams(TypedDict, total=False):
    inputs: Required[Iterable[BetaDreamInputParam]]

    model: Required[Model]
    """Model identifier and configuration applied to every pipeline stage."""

    instructions: Optional[str]

    output_behavior: OutputBehavior
    """
    The default destination: the job creates a new output memory store as a clone of
    the memory_store input and writes the consolidated memories into it. The input
    store is never mutated.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


Model: TypeAlias = Union[str, BetaDreamModelConfigParam]


class OutputBehaviorBetaOutputBehaviorCreateNew(TypedDict, total=False):
    """
    The default destination: the job creates a new output memory store as a clone of the memory_store input and writes the consolidated memories into it. The input store is never mutated.
    """

    type: Required[Literal["create_new"]]


class OutputBehaviorBetaOutputBehaviorUpdateExisting(TypedDict, total=False):
    """
    The job writes the consolidated memories into this existing memory store instead of creating one. In EAP the store must be the job's own memory_store input, so the job consolidates the store in place.
    """

    memory_store_id: Required[str]

    type: Required[Literal["update_existing"]]


OutputBehavior: TypeAlias = Union[
    OutputBehaviorBetaOutputBehaviorCreateNew, OutputBehaviorBetaOutputBehaviorUpdateExisting
]
