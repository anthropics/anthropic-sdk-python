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
    """
    The memory store and sessions for the dream to read, as exactly one
    `memory_store` entry and exactly one `sessions` entry.
    """

    model: Required[Model]
    """
    The model that runs a dream, given as a model ID or as an object with `id` and
    `speed`.

    In the object form, `speed` can only be `standard`.

    The
    [limits table in the Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#limits)
    lists the supported models.
    """

    instructions: Optional[str]
    """
    Guidance that steers how the dream reads the sessions and organizes the output
    memory store, from 1 to 4,096 characters.

    See the
    [Dreams guide](https://platform.claude.com/docs/en/managed-agents/dreams#steer-with-instructions)
    for what kinds of instructions work well.
    """

    output_behavior: BetaOutputBehaviorParam
    """Which memory store a dream writes its result to.

    Defaults to `create_new` when left out of a create request.
    """

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
