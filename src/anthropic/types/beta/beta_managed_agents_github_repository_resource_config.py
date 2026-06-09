# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_branch_checkout import BetaManagedAgentsBranchCheckout
from .beta_managed_agents_commit_checkout import BetaManagedAgentsCommitCheckout

__all__ = ["BetaManagedAgentsGitHubRepositoryResourceConfig", "Checkout"]

Checkout: TypeAlias = Annotated[
    Union[BetaManagedAgentsBranchCheckout, BetaManagedAgentsCommitCheckout, None], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsGitHubRepositoryResourceConfig(BaseModel):
    """A GitHub repository mounted into each session's container.

    The authorization token is write-only and never returned.
    """

    type: Literal["github_repository"]

    url: str
    """Github URL of the repository"""

    checkout: Optional[Checkout] = None
    """Branch or commit to check out. Defaults to the repository's default branch."""

    mount_path: Optional[str] = None
    """Mount path in the container. Defaults to `/workspace/<repo-name>`."""
