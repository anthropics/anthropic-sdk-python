from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_analytics_federated_actor_aws_provider import BetaAnalyticsFederatedActorAWSProvider
from .beta_analytics_federated_actor_gcp_provider import BetaAnalyticsFederatedActorGCPProvider
from .beta_analytics_federated_actor_oidc_provider import BetaAnalyticsFederatedActorOIDCProvider
from .beta_analytics_federated_actor_azure_provider import BetaAnalyticsFederatedActorAzureProvider

__all__ = ["BetaAnalyticsFederatedActorProvider"]

BetaAnalyticsFederatedActorProvider: TypeAlias = Annotated[
    Union[
        BetaAnalyticsFederatedActorAWSProvider,
        BetaAnalyticsFederatedActorAzureProvider,
        BetaAnalyticsFederatedActorGCPProvider,
        BetaAnalyticsFederatedActorOIDCProvider,
    ],
    UnionDiscriminator("type"),
]
