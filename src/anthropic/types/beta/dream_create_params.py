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
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """


Model: TypeAlias = Union[str, BetaDreamModelConfigParam]
