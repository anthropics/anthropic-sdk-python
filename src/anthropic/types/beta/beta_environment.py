# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_cloud_config import BetaCloudConfig
from .beta_self_hosted_config import BetaSelfHostedConfig

__all__ = ["BetaEnvironment", "Config"]

Config: TypeAlias = Annotated[Union[BetaCloudConfig, BetaSelfHostedConfig], PropertyInfo(discriminator="type")]


class BetaEnvironment(BaseModel):
    """Unified Environment resource for both cloud and self-hosted environments."""

    id: str
    """Environment identifier (e.g., 'env\\__...')"""

    archived_at: Optional[str] = None
    """RFC 3339 timestamp when environment was archived, or null if not archived"""

    config: Config
    """Environment configuration (either Anthropic Cloud or self-hosted)"""

    created_at: str
    """RFC 3339 timestamp when environment was created"""

    description: str
    """User-provided description for the environment"""

    metadata: Dict[str, str]
    """User-provided metadata key-value pairs"""

    name: str
    """Human-readable name for the environment"""

    type: Literal["environment"]
    """The type of object (always 'environment')"""

    updated_at: str
    """RFC 3339 timestamp when environment was last updated"""

    scope: Optional[Literal["organization", "account"]] = None
    """The visibility scope for this environment.

    'organization' means visible to all accounts. 'account' means visible only to
    the owning account.
    """
