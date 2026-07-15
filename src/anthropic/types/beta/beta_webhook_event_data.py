# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_webhook_agent_created_event_data import BetaWebhookAgentCreatedEventData
from .beta_webhook_agent_deleted_event_data import BetaWebhookAgentDeletedEventData
from .beta_webhook_agent_updated_event_data import BetaWebhookAgentUpdatedEventData
from .beta_webhook_session_idled_event_data import BetaWebhookSessionIdledEventData
from .beta_webhook_vault_created_event_data import BetaWebhookVaultCreatedEventData
from .beta_webhook_vault_deleted_event_data import BetaWebhookVaultDeletedEventData
from .beta_webhook_agent_archived_event_data import BetaWebhookAgentArchivedEventData
from .beta_webhook_vault_archived_event_data import BetaWebhookVaultArchivedEventData
from .beta_webhook_session_created_event_data import BetaWebhookSessionCreatedEventData
from .beta_webhook_session_deleted_event_data import BetaWebhookSessionDeletedEventData
from .beta_webhook_session_pending_event_data import BetaWebhookSessionPendingEventData
from .beta_webhook_session_running_event_data import BetaWebhookSessionRunningEventData
from .beta_webhook_session_updated_event_data import BetaWebhookSessionUpdatedEventData
from .beta_webhook_session_archived_event_data import BetaWebhookSessionArchivedEventData
from .beta_webhook_deployment_paused_event_data import BetaWebhookDeploymentPausedEventData
from .beta_webhook_deployment_created_event_data import BetaWebhookDeploymentCreatedEventData
from .beta_webhook_deployment_deleted_event_data import BetaWebhookDeploymentDeletedEventData
from .beta_webhook_deployment_updated_event_data import BetaWebhookDeploymentUpdatedEventData
from .beta_webhook_deployment_archived_event_data import BetaWebhookDeploymentArchivedEventData
from .beta_webhook_deployment_unpaused_event_data import BetaWebhookDeploymentUnpausedEventData
from .beta_webhook_session_status_idled_event_data import BetaWebhookSessionStatusIdledEventData
from .beta_webhook_session_thread_idled_event_data import BetaWebhookSessionThreadIdledEventData
from .beta_webhook_deployment_run_failed_event_data import BetaWebhookDeploymentRunFailedEventData
from .beta_webhook_deployment_run_started_event_data import BetaWebhookDeploymentRunStartedEventData
from .beta_webhook_session_thread_created_event_data import BetaWebhookSessionThreadCreatedEventData
from .beta_webhook_session_requires_action_event_data import BetaWebhookSessionRequiresActionEventData
from .beta_webhook_deployment_run_succeeded_event_data import BetaWebhookDeploymentRunSucceededEventData
from .beta_webhook_vault_credential_created_event_data import BetaWebhookVaultCredentialCreatedEventData
from .beta_webhook_vault_credential_deleted_event_data import BetaWebhookVaultCredentialDeletedEventData
from .beta_webhook_session_status_terminated_event_data import BetaWebhookSessionStatusTerminatedEventData
from .beta_webhook_session_thread_terminated_event_data import BetaWebhookSessionThreadTerminatedEventData
from .beta_webhook_vault_credential_archived_event_data import BetaWebhookVaultCredentialArchivedEventData
from .beta_webhook_session_status_rescheduled_event_data import BetaWebhookSessionStatusRescheduledEventData
from .beta_webhook_session_status_run_started_event_data import BetaWebhookSessionStatusRunStartedEventData
from .beta_webhook_vault_credential_refresh_failed_event_data import BetaWebhookVaultCredentialRefreshFailedEventData
from .beta_webhook_session_outcome_evaluation_ended_event_data import BetaWebhookSessionOutcomeEvaluationEndedEventData

__all__ = ["BetaWebhookEventData"]

BetaWebhookEventData: TypeAlias = Annotated[
    Union[
        BetaWebhookSessionCreatedEventData,
        BetaWebhookSessionPendingEventData,
        BetaWebhookSessionRunningEventData,
        BetaWebhookSessionIdledEventData,
        BetaWebhookSessionRequiresActionEventData,
        BetaWebhookSessionArchivedEventData,
        BetaWebhookSessionDeletedEventData,
        BetaWebhookSessionStatusRescheduledEventData,
        BetaWebhookSessionStatusRunStartedEventData,
        BetaWebhookSessionStatusIdledEventData,
        BetaWebhookSessionStatusTerminatedEventData,
        BetaWebhookSessionThreadCreatedEventData,
        BetaWebhookSessionThreadIdledEventData,
        BetaWebhookSessionThreadTerminatedEventData,
        BetaWebhookSessionOutcomeEvaluationEndedEventData,
        BetaWebhookVaultCreatedEventData,
        BetaWebhookVaultArchivedEventData,
        BetaWebhookVaultDeletedEventData,
        BetaWebhookVaultCredentialCreatedEventData,
        BetaWebhookVaultCredentialArchivedEventData,
        BetaWebhookVaultCredentialDeletedEventData,
        BetaWebhookVaultCredentialRefreshFailedEventData,
        BetaWebhookSessionUpdatedEventData,
        BetaWebhookAgentCreatedEventData,
        BetaWebhookAgentArchivedEventData,
        BetaWebhookAgentDeletedEventData,
        BetaWebhookDeploymentPausedEventData,
        BetaWebhookDeploymentRunFailedEventData,
        BetaWebhookDeploymentCreatedEventData,
        BetaWebhookDeploymentUpdatedEventData,
        BetaWebhookDeploymentUnpausedEventData,
        BetaWebhookAgentUpdatedEventData,
        BetaWebhookDeploymentArchivedEventData,
        BetaWebhookDeploymentRunStartedEventData,
        BetaWebhookDeploymentDeletedEventData,
        BetaWebhookDeploymentRunSucceededEventData,
    ],
    PropertyInfo(discriminator="type"),
]
