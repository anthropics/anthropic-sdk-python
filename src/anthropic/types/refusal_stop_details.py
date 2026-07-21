# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RefusalStopDetails"]


class RefusalStopDetails(BaseModel):
    """Structured information about a refusal."""

    category: Optional[Literal["cyber", "bio", "frontier_llm", "reasoning_extraction", "general_harms"]] = None
    """The policy category that triggered a refusal.

    - `cyber` - The request could enable cyber harm, such as malware or exploit
      development. Benign cybersecurity work can also trigger this category.
    - `bio` - The request could enable biological harm, such as dangerous lab
      methods. Beneficial life sciences work can also trigger this category.
    - `frontier_llm` - The request could assist the development of competing AI
      models, which is restricted under
      [Anthropic's commercial terms](https://www.anthropic.com/legal/commercial-terms).
      Benign machine learning work can also trigger this category.
    - `reasoning_extraction` - The request asks the model to reproduce its internal
      reasoning in the response text. To get reasoning in a structured form instead,
      use
      [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking).
    - `general_harms` - The request could be related to an area that was determined
      as harmful. Benign work might sometimes trigger this category.
    """

    explanation: Optional[str] = None
    """Human-readable explanation of the refusal.

    This text is not guaranteed to be stable. `null` when no explanation is
    available for the category.
    """

    type: Literal["refusal"]
