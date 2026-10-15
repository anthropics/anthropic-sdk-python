from .._models import BaseModel
from .capability_support import CapabilitySupport

__all__ = ["ThinkingTypes"]


class ThinkingTypes(BaseModel):
    """Which `thinking.type` values the model accepts on requests.

    Read each key on its own: for example, `enabled` can be false while `disabled` is true.
    """

    adaptive: CapabilitySupport
    """
    Whether the model accepts thinking with type 'adaptive' (the model decides
    whether and how much to think).
    """

    between_tools: CapabilitySupport
    """
    Whether the model accepts thinking with type 'between_tools' (thinking turned
    off, and any short progress updates the model writes between tool calls come
    back as thinking blocks). False exactly when a request that sends it gets a 400
    from this model. A request that sends 'between_tools' can still be rejected for
    another reason, such as an effort level the model does not allow with thinking
    off.
    """

    disabled: CapabilitySupport
    """Whether the model accepts thinking with type 'disabled' (thinking turned off).

    False exactly when a request that sends it gets a 400 from this model. True on a
    model that does not support thinking. A request that sends 'disabled' can still
    be rejected for another reason, such as an effort level the model does not allow
    with thinking off.
    """

    enabled: CapabilitySupport
    """
    Whether the model accepts thinking with type 'enabled' (extended thinking with a
    caller-set `budget_tokens`).
    """
