from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from ..file_expired_error_details import FileExpiredErrorDetails
from ..thread_not_found_error_details import ThreadNotFoundErrorDetails
from .cmek_key_disabled_error_details import CMEKKeyDisabledErrorDetails
from ..tool_name_conflict_error_details import ToolNameConflictErrorDetails
from .ramp_limit_exceeded_error_details import RampLimitExceededErrorDetails
from ..beta_storage_in_use_error_details import BetaStorageInUseErrorDetails
from ..rbac_role_not_found_error_details import RBACRoleNotFoundErrorDetails
from .cmek_key_unreachable_error_details import CMEKKeyUnreachableErrorDetails
from .organization_on_hold_error_details import OrganizationOnHoldErrorDetails
from ..file_not_downloadable_error_details import FileNotDownloadableErrorDetails
from ..user_profile_required_error_details import UserProfileRequiredErrorDetails
from ..beta_cmek_not_approved_error_details import BetaCMEKNotApprovedErrorDetails
from ..change_outcome_unknown_error_details import ChangeOutcomeUnknownErrorDetails
from ..compaction_unavailable_error_details import CompactionUnavailableErrorDetails
from ..storage_quota_exceeded_error_details import StorageQuotaExceededErrorDetails
from ..user_profile_not_found_error_details import UserProfileNotFoundErrorDetails
from .cmek_context_unavailable_error_details import CMEKContextUnavailableErrorDetails
from .cmek_key_network_blocked_error_details import CMEKKeyNetworkBlockedErrorDetails
from ..beta_unsupported_charset_error_details import BetaUnsupportedCharsetErrorDetails
from ..thread_already_continued_error_details import ThreadAlreadyContinuedErrorDetails
from .sandbox_egress_restricted_error_details import SandboxEgressRestrictedErrorDetails
from ..beta_region_not_supported_error_details import BetaRegionNotSupportedErrorDetails
from ..beta_request_body_timeout_error_details import BetaRequestBodyTimeoutErrorDetails
from ..beta_storage_not_approved_error_details import BetaStorageNotApprovedErrorDetails
from ..org_member_limit_exceeded_error_details import OrgMemberLimitExceededErrorDetails
from ..thread_continue_in_flight_error_details import ThreadContinueInFlightErrorDetails
from ..tool_reference_unresolved_error_details import ToolReferenceUnresolvedErrorDetails
from ..user_profile_not_billable_error_details import UserProfileNotBillableErrorDetails
from ..beta.beta_invalid_metadata_error_details import BetaInvalidMetadataErrorDetails
from ..compaction_block_ambiguous_error_details import CompactionBlockAmbiguousErrorDetails
from ..compaction_block_misplaced_error_details import CompactionBlockMisplacedErrorDetails
from ..compaction_incomplete_turn_error_details import CompactionIncompleteTurnErrorDetails
from ..image_dimensions_too_large_error_details import ImageDimensionsTooLargeErrorDetails
from ..thread_unsupported_request_error_details import ThreadUnsupportedRequestErrorDetails
from .claude_code_version_too_old_error_details import ClaudeCodeVersionTooOldErrorDetails
from ..beta.beta_approval_required_error_details import BetaApprovalRequiredErrorDetails
from ..beta_external_key_not_found_error_details import BetaExternalKeyNotFoundErrorDetails
from ..compaction_content_mismatch_error_details import CompactionContentMismatchErrorDetails
from ..organization.already_member_error_details import AlreadyMemberErrorDetails
from ..thread_fingerprint_mismatch_error_details import ThreadFingerprintMismatchErrorDetails
from .contract_spend_limit_reached_error_details import ContractSpendLimitReachedErrorDetails
from .enforced_spend_limit_reached_error_details import EnforcedSpendLimitReachedErrorDetails
from .parent_organization_required_error_details import ParentOrganizationRequiredErrorDetails
from ..compaction_signature_invalid_error_details import CompactionSignatureInvalidErrorDetails
from ..concurrent_membership_change_error_details import ConcurrentMembershipChangeErrorDetails
from .request_body_encoding_invalid_error_details import RequestBodyEncodingInvalidErrorDetails
from ..beta_gcp_project_not_verified_error_details import BetaGCPProjectNotVerifiedErrorDetails
from ..available_tools_limit_exceeded_error_details import AvailableToolsLimitExceededErrorDetails
from ..beta.beta_environment_archived_error_details import BetaEnvironmentArchivedErrorDetails
from .organization_type_not_supported_error_details import OrganizationTypeNotSupportedErrorDetails
from .workspace_human_review_disabled_error_details import WorkspaceHumanReviewDisabledErrorDetails
from ..beta.beta_environment_not_found_error_details import BetaEnvironmentNotFoundErrorDetails
from ..compaction_nothing_to_summarize_error_details import CompactionNothingToSummarizeErrorDetails
from ..compaction_tool_changes_mismatch_error_details import CompactionToolChangesMismatchErrorDetails
from ..skill_read_blocked_undecryptable_error_details import SkillReadBlockedUndecryptableErrorDetails
from .request_body_encoding_unsupported_error_details import RequestBodyEncodingUnsupportedErrorDetails
from ..organization.external_key_changed_error_details import ExternalKeyChangedErrorDetails
from ..organization.key_profile_mismatch_error_details import KeyProfileMismatchErrorDetails
from .claude_code_key_creator_not_member_error_details import ClaudeCodeKeyCreatorNotMemberErrorDetails
from ..beta.organization.beta_scan_failed_error_details import BetaScanFailedErrorDetails
from ..organization.invite_already_exists_error_details import InviteAlreadyExistsErrorDetails
from ..beta.beta_organization_not_eligible_error_details import BetaOrganizationNotEligibleErrorDetails
from ..beta.organization.beta_scan_pending_error_details import BetaScanPendingErrorDetails
from ..beta_external_key_provider_mismatch_error_details import BetaExternalKeyProviderMismatchErrorDetails
from ..compaction_too_many_tool_references_error_details import CompactionTooManyToolReferencesErrorDetails
from ..user_profile_billing_not_authorized_error_details import UserProfileBillingNotAuthorizedErrorDetails
from ..beta.beta_human_review_not_available_error_details import BetaHumanReviewNotAvailableErrorDetails
from ..beta.beta_invalid_config_type_change_error_details import BetaInvalidConfigTypeChangeErrorDetails
from .request_body_too_large_after_decoding_error_details import RequestBodyTooLargeAfterDecodingErrorDetails
from ..beta.beta_environment_create_disabled_error_details import BetaEnvironmentCreateDisabledErrorDetails
from ..beta.beta_environment_update_disabled_error_details import BetaEnvironmentUpdateDisabledErrorDetails
from ..beta.organization.beta_bundle_on_call_error_details import BetaBundleOnCallErrorDetails
from ..beta.organization.beta_grant_required_error_details import BetaGrantRequiredErrorDetails
from ..organization.email_domain_not_allowed_error_details import EmailDomainNotAllowedErrorDetails
from ..organization.storage_profile_mismatch_error_details import StorageProfileMismatchErrorDetails
from ..beta_organization_not_enrolled_in_beta_error_details import BetaOrganizationNotEnrolledInBetaErrorDetails
from ..organization.cannot_remove_last_member_error_details import CannotRemoveLastMemberErrorDetails
from .linked_organization_billing_unavailable_error_details import LinkedOrganizationBillingUnavailableErrorDetails
from .linked_organization_spend_limit_reached_error_details import LinkedOrganizationSpendLimitReachedErrorDetails
from ..beta.organization.beta_skill_name_taken_error_details import BetaSkillNameTakenErrorDetails
from ..organization.org_api_key_limit_exceeded_error_details import OrgAPIKeyLimitExceededErrorDetails
from ..organization.workspace_policy_violation_error_details import WorkspacePolicyViolationErrorDetails
from ..beta.organization.beta_plugin_name_taken_error_details import BetaPluginNameTakenErrorDetails
from ..beta.beta_authorization_check_unavailable_error_details import BetaAuthorizationCheckUnavailableErrorDetails
from ..beta.organization.beta_unsupported_region_error_details import BetaUnsupportedRegionErrorDetails
from ..organization.workspace_created_incomplete_error_details import WorkspaceCreatedIncompleteErrorDetails
from ..beta.organization.beta_invalid_storage_arn_error_details import BetaInvalidStorageARNErrorDetails
from ..beta.organization.beta_cannot_sign_out_self_error_details import BetaCannotSignOutSelfErrorDetails
from ..beta.organization.beta_provider_not_allowed_error_details import BetaProviderNotAllowedErrorDetails
from ..beta.organization.beta_rbac_group_not_found_error_details import BetaRBACGroupNotFoundErrorDetails
from ..beta.organization.beta_registration_pending_error_details import BetaRegistrationPendingErrorDetails
from ..organization.external_key_validation_failed_error_details import ExternalKeyValidationFailedErrorDetails
from ..organization.rbac_group_grants_owner_access_error_details import RBACGroupGrantsOwnerAccessErrorDetails
from ..beta.organization.beta_api_key_scope_missing_error_details import BetaAPIKeyScopeMissingErrorDetails
from ..beta.organization.beta_cannot_sign_out_owner_error_details import BetaCannotSignOutOwnerErrorDetails
from ..organization.storage_attached_during_archive_error_details import StorageAttachedDuringArchiveErrorDetails
from ..organization.workspace_member_limit_exceeded_error_details import WorkspaceMemberLimitExceededErrorDetails
from ..beta.organization.beta_storage_not_attachable_error_details import BetaStorageNotAttachableErrorDetails
from ..organization.external_key_in_workspace_policy_error_details import ExternalKeyInWorkspacePolicyErrorDetails
from ..organization.workspace_api_key_limit_exceeded_error_details import WorkspaceAPIKeyLimitExceededErrorDetails
from ..beta.organization.beta_external_storage_in_use_error_details import BetaExternalStorageInUseErrorDetails
from ..organization.external_key_validation_timed_out_error_details import ExternalKeyValidationTimedOutErrorDetails
from ..organization.rbac_group_owner_access_unconfirmed_error_details import RBACGroupOwnerAccessUnconfirmedErrorDetails
from ..beta.organization.beta_storage_already_registered_error_details import BetaStorageAlreadyRegisteredErrorDetails
from ..beta.organization.beta_storage_verification_failed_error_details import BetaStorageVerificationFailedErrorDetails
from ..beta.organization.beta_storage_attach_limit_reached_error_details import (
    BetaStorageAttachLimitReachedErrorDetails,
)
from ..beta.organization.beta_storage_changed_concurrently_error_details import (
    BetaStorageChangedConcurrentlyErrorDetails,
)
from ..beta.organization.beta_transcripts_storage_required_error_details import (
    BetaTranscriptsStorageRequiredErrorDetails,
)
from ..beta_gcp_project_controlled_by_another_organization_error_details import (
    BetaGCPProjectControlledByAnotherOrganizationErrorDetails,
)
from ..beta.environments.beta_heartbeat_precondition_failed_error_details import (
    BetaHeartbeatPreconditionFailedErrorDetails,
)
from ..beta.organization.beta_cannot_sign_out_primary_owner_error_details import (
    BetaCannotSignOutPrimaryOwnerErrorDetails,
)
from ..beta.organization.beta_claude_tag_writes_not_enabled_error_details import (
    BetaClaudeTagWritesNotEnabledErrorDetails,
)
from ..beta.organization.beta_cannot_sign_out_managed_member_error_details import (
    BetaCannotSignOutManagedMemberErrorDetails,
)
from ..beta.organization.beta_external_storage_not_available_error_details import (
    BetaExternalStorageNotAvailableErrorDetails,
)
from ..beta.organization.beta_storage_profile_still_required_error_details import (
    BetaStorageProfileStillRequiredErrorDetails,
)
from ..beta.organization.beta_workspace_changed_concurrently_error_details import (
    BetaWorkspaceChangedConcurrentlyErrorDetails,
)
from ..beta.organization.beta_bundle_attachment_not_supported_error_details import (
    BetaBundleAttachmentNotSupportedErrorDetails,
)
from ..beta.organization.beta_cannot_sign_out_membership_admin_error_details import (
    BetaCannotSignOutMembershipAdminErrorDetails,
)
from ..beta.organization.beta_cannot_sign_out_privileged_member_error_details import (
    BetaCannotSignOutPrivilegedMemberErrorDetails,
)
from ..organization.cannot_invite_emails_with_unverified_domains_error_details import (
    CannotInviteEmailsWithUnverifiedDomainsErrorDetails,
)
from ..beta.organization.beta_compliance_configuration_restricted_error_details import (
    BetaComplianceConfigurationRestrictedErrorDetails,
)
from ..beta.organization.beta_external_storage_in_workspace_policy_error_details import (
    BetaExternalStorageInWorkspacePolicyErrorDetails,
)
from ..beta.organization.claude_code.beta_cmek_feature_unsupported_error_details import (
    BetaCMEKFeatureUnsupportedErrorDetails,
)
from ..beta.organization.beta_human_review_on_with_external_storage_error_details import (
    BetaHumanReviewOnWithExternalStorageErrorDetails,
)
from ..beta.organization.beta_slack_channel_set_up_settings_refused_error_details import (
    BetaSlackChannelSetUpSettingsRefusedErrorDetails,
)
from ..beta.organization.beta_slack_channel_set_up_settings_conflict_error_details import (
    BetaSlackChannelSetUpSettingsConflictErrorDetails,
)
from ..beta.organization.beta_spend_limits_admin_api_writes_not_enabled_error_details import (
    BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails,
)
from ..beta.organization.beta_organization_level_scoped_api_key_required_error_details import (
    BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails,
)
from ..beta.organization.beta_slack_channel_set_up_environment_not_found_error_details import (
    BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails,
)
from ..beta.organization.claude_code.beta_rbac_group_order_limit_exceeded_error_details import (
    BetaRBACGroupOrderLimitExceededErrorDetails,
)
from ..beta.organization.claude_code.beta_settings_history_limit_exceeded_error_details import (
    BetaSettingsHistoryLimitExceededErrorDetails,
)
from ..beta.organization.claude_code.beta_settings_document_limit_exceeded_error_details import (
    BetaSettingsDocumentLimitExceededErrorDetails,
)
from ..beta.organization.claude_code.beta_rbac_group_managed_settings_not_found_error_details import (
    BetaRBACGroupManagedSettingsNotFoundErrorDetails,
)

__all__ = ["ErrorDetails"]

ErrorDetails: TypeAlias = Annotated[
    Union[
        AvailableToolsLimitExceededErrorDetails,
        ClaudeCodeKeyCreatorNotMemberErrorDetails,
        ClaudeCodeVersionTooOldErrorDetails,
        CMEKKeyDisabledErrorDetails,
        CMEKKeyNetworkBlockedErrorDetails,
        CompactionBlockAmbiguousErrorDetails,
        CompactionBlockMisplacedErrorDetails,
        CompactionContentMismatchErrorDetails,
        CompactionIncompleteTurnErrorDetails,
        CompactionNothingToSummarizeErrorDetails,
        CompactionSignatureInvalidErrorDetails,
        CompactionTooManyToolReferencesErrorDetails,
        CompactionToolChangesMismatchErrorDetails,
        ImageDimensionsTooLargeErrorDetails,
        OrganizationOnHoldErrorDetails,
        RequestBodyEncodingInvalidErrorDetails,
        RequestBodyEncodingUnsupportedErrorDetails,
        ThreadAlreadyContinuedErrorDetails,
        ThreadContinueInFlightErrorDetails,
        ThreadFingerprintMismatchErrorDetails,
        ThreadUnsupportedRequestErrorDetails,
        ToolNameConflictErrorDetails,
        ToolReferenceUnresolvedErrorDetails,
        UserProfileRequiredErrorDetails,
        LinkedOrganizationBillingUnavailableErrorDetails,
        LinkedOrganizationSpendLimitReachedErrorDetails,
        UserProfileBillingNotAuthorizedErrorDetails,
        UserProfileNotBillableErrorDetails,
        ThreadNotFoundErrorDetails,
        SkillReadBlockedUndecryptableErrorDetails,
        RequestBodyTooLargeAfterDecodingErrorDetails,
        ContractSpendLimitReachedErrorDetails,
        EnforcedSpendLimitReachedErrorDetails,
        RampLimitExceededErrorDetails,
        CMEKKeyUnreachableErrorDetails,
        CompactionUnavailableErrorDetails,
        WorkspaceHumanReviewDisabledErrorDetails,
        StorageQuotaExceededErrorDetails,
        FileNotDownloadableErrorDetails,
        FileExpiredErrorDetails,
        CMEKContextUnavailableErrorDetails,
        OrgAPIKeyLimitExceededErrorDetails,
        WorkspaceAPIKeyLimitExceededErrorDetails,
        SandboxEgressRestrictedErrorDetails,
        UserProfileNotFoundErrorDetails,
        ExternalKeyInWorkspacePolicyErrorDetails,
        AlreadyMemberErrorDetails,
        CannotInviteEmailsWithUnverifiedDomainsErrorDetails,
        EmailDomainNotAllowedErrorDetails,
        InviteAlreadyExistsErrorDetails,
        OrgMemberLimitExceededErrorDetails,
        RBACGroupGrantsOwnerAccessErrorDetails,
        RBACGroupOwnerAccessUnconfirmedErrorDetails,
        CannotRemoveLastMemberErrorDetails,
        ConcurrentMembershipChangeErrorDetails,
        ExternalKeyValidationFailedErrorDetails,
        ExternalKeyValidationTimedOutErrorDetails,
        KeyProfileMismatchErrorDetails,
        WorkspacePolicyViolationErrorDetails,
        ExternalKeyChangedErrorDetails,
        WorkspaceCreatedIncompleteErrorDetails,
        StorageProfileMismatchErrorDetails,
        ChangeOutcomeUnknownErrorDetails,
        StorageAttachedDuringArchiveErrorDetails,
        WorkspaceMemberLimitExceededErrorDetails,
        OrganizationTypeNotSupportedErrorDetails,
        ParentOrganizationRequiredErrorDetails,
        RBACRoleNotFoundErrorDetails,
        BetaEnvironmentCreateDisabledErrorDetails,
        BetaEnvironmentArchivedErrorDetails,
        BetaInvalidConfigTypeChangeErrorDetails,
        BetaEnvironmentUpdateDisabledErrorDetails,
        BetaHeartbeatPreconditionFailedErrorDetails,
        BetaInvalidMetadataErrorDetails,
        BetaGrantRequiredErrorDetails,
        BetaOrganizationNotEligibleErrorDetails,
        BetaProviderNotAllowedErrorDetails,
        BetaUnsupportedRegionErrorDetails,
        BetaStorageAlreadyRegisteredErrorDetails,
        BetaAuthorizationCheckUnavailableErrorDetails,
        BetaInvalidStorageARNErrorDetails,
        BetaExternalStorageInUseErrorDetails,
        BetaExternalStorageInWorkspacePolicyErrorDetails,
        BetaStorageVerificationFailedErrorDetails,
        BetaCMEKNotApprovedErrorDetails,
        BetaExternalKeyNotFoundErrorDetails,
        BetaExternalKeyProviderMismatchErrorDetails,
        BetaGCPProjectNotVerifiedErrorDetails,
        BetaRegionNotSupportedErrorDetails,
        BetaStorageNotApprovedErrorDetails,
        BetaGCPProjectControlledByAnotherOrganizationErrorDetails,
        BetaStorageInUseErrorDetails,
        BetaCannotSignOutPrimaryOwnerErrorDetails,
        BetaCannotSignOutSelfErrorDetails,
        BetaOrganizationNotEnrolledInBetaErrorDetails,
        BetaCannotSignOutManagedMemberErrorDetails,
        BetaCannotSignOutMembershipAdminErrorDetails,
        BetaCannotSignOutOwnerErrorDetails,
        BetaCannotSignOutPrivilegedMemberErrorDetails,
        BetaApprovalRequiredErrorDetails,
        BetaExternalStorageNotAvailableErrorDetails,
        BetaHumanReviewNotAvailableErrorDetails,
        BetaHumanReviewOnWithExternalStorageErrorDetails,
        BetaStorageNotAttachableErrorDetails,
        BetaTranscriptsStorageRequiredErrorDetails,
        BetaStorageAttachLimitReachedErrorDetails,
        BetaStorageProfileStillRequiredErrorDetails,
        BetaStorageChangedConcurrentlyErrorDetails,
        BetaWorkspaceChangedConcurrentlyErrorDetails,
        BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails,
        BetaUnsupportedCharsetErrorDetails,
        BetaPluginNameTakenErrorDetails,
        BetaSkillNameTakenErrorDetails,
        BetaRegistrationPendingErrorDetails,
        BetaScanFailedErrorDetails,
        BetaScanPendingErrorDetails,
        BetaRequestBodyTimeoutErrorDetails,
        BetaSettingsDocumentLimitExceededErrorDetails,
        BetaSettingsHistoryLimitExceededErrorDetails,
        BetaCMEKFeatureUnsupportedErrorDetails,
        BetaRBACGroupManagedSettingsNotFoundErrorDetails,
        BetaRBACGroupOrderLimitExceededErrorDetails,
        BetaRBACGroupNotFoundErrorDetails,
        BetaSlackChannelSetUpSettingsRefusedErrorDetails,
        BetaAPIKeyScopeMissingErrorDetails,
        BetaClaudeTagWritesNotEnabledErrorDetails,
        BetaComplianceConfigurationRestrictedErrorDetails,
        BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails,
        BetaEnvironmentNotFoundErrorDetails,
        BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails,
        BetaSlackChannelSetUpSettingsConflictErrorDetails,
        BetaBundleAttachmentNotSupportedErrorDetails,
        BetaBundleOnCallErrorDetails,
    ],
    UnionDiscriminator("error_code"),
]
