# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMemoryStoreResourceConfig"]


class BetaManagedAgentsMemoryStoreResourceConfig(BaseModel):
    """A memory store attached to each session created from this deployment."""

    memory_store_id: str
    """The memory store ID (memstore\\__...).

    Must belong to the caller's organization and workspace.
    """

    type: Literal["memory_store"]

    access: Optional[Literal["read_write", "read_only"]] = None
    """Access mode for an attached memory store."""

    instructions: Optional[str] = None
    """Per-attachment guidance for the agent on how to use this store.

    Rendered into the memory section of the system prompt. Max 4096 chars.
    """
