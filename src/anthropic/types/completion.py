# File generated from our OpenAPI spec by Stainless.

from .._models import BaseModel

__all__ = ["Completion"]


class Completion(BaseModel):
    completion: str
    """The resulting completion up to and excluding the stop sequences."""

    model: str
    """The model that performed the completion."""

    stop_reason: str
    """The reason that we stopped sampling.

    This may be one the following values:

    - `"stop_sequence"`: we reached a stop sequence — either provided by you via the
      `stop_sequences` parameter, or a stop sequence built into the model
    - `"max_tokens"`: we exceeded `max_tokens_to_sample` or the model's maximum
    """
