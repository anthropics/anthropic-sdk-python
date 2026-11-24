from __future__ import annotations

import httpx2

from ._exceptions import (
    ConflictError,
    NotFoundError,
    APIStatusError,
    RateLimitError,
    BadRequestError,
    OverloadedError,
    AuthenticationError,
    GatewayTimeoutError,
    InternalServerError,
    RequestTimeoutError,
    ContentTooLargeError,
    PaymentRequiredError,
    PermissionDeniedError,
    HTTPNotImplementedError,
    PreconditionFailedError,
    ServiceUnavailableError,
    ClientClosedRequestError,
    UnprocessableEntityError,
    RequestHeaderFieldsTooLargeError,
    extract_error_code,
)
from .types.file_expired_error import FileExpiredError
from .types.thread_not_found_error import ThreadNotFoundError
from .types.tool_name_conflict_error import ToolNameConflictError
from .types.beta_storage_in_use_error import BetaStorageInUseError
from .types.rbac_role_not_found_error import RBACRoleNotFoundError
from .types.file_not_downloadable_error import FileNotDownloadableError
from .types.user_profile_required_error import UserProfileRequiredError
from .types.beta_cmek_not_approved_error import BetaCMEKNotApprovedError
from .types.change_outcome_unknown_error import ChangeOutcomeUnknownError
from .types.compaction_unavailable_error import CompactionUnavailableError
from .types.storage_quota_exceeded_error import StorageQuotaExceededError
from .types.user_profile_not_found_error import UserProfileNotFoundError
from .types.beta_unsupported_charset_error import BetaUnsupportedCharsetError
from .types.shared.cmek_key_disabled_error import CMEKKeyDisabledError
from .types.thread_already_continued_error import ThreadAlreadyContinuedError
from .types.beta_region_not_supported_error import BetaRegionNotSupportedError
from .types.beta_request_body_timeout_error import BetaRequestBodyTimeoutError
from .types.beta_storage_not_approved_error import BetaStorageNotApprovedError
from .types.org_member_limit_exceeded_error import OrgMemberLimitExceededError
from .types.thread_continue_in_flight_error import ThreadContinueInFlightError
from .types.tool_reference_unresolved_error import ToolReferenceUnresolvedError
from .types.user_profile_not_billable_error import UserProfileNotBillableError
from .types.beta.beta_invalid_metadata_error import BetaInvalidMetadataError
from .types.compaction_block_ambiguous_error import CompactionBlockAmbiguousError
from .types.compaction_block_misplaced_error import CompactionBlockMisplacedError
from .types.compaction_incomplete_turn_error import CompactionIncompleteTurnError
from .types.image_dimensions_too_large_error import ImageDimensionsTooLargeError
from .types.shared.ramp_limit_exceeded_error import RampLimitExceededError
from .types.thread_unsupported_request_error import ThreadUnsupportedRequestError
from .types.beta.beta_approval_required_error import BetaApprovalRequiredError
from .types.beta_external_key_not_found_error import BetaExternalKeyNotFoundError
from .types.compaction_content_mismatch_error import CompactionContentMismatchError
from .types.organization.already_member_error import AlreadyMemberError
from .types.shared.cmek_key_unreachable_error import CMEKKeyUnreachableError
from .types.shared.organization_on_hold_error import OrganizationOnHoldError
from .types.thread_fingerprint_mismatch_error import ThreadFingerprintMismatchError
from .types.compaction_signature_invalid_error import CompactionSignatureInvalidError
from .types.concurrent_membership_change_error import ConcurrentMembershipChangeError
from .types.beta_gcp_project_not_verified_error import BetaGCPProjectNotVerifiedError
from .types.available_tools_limit_exceeded_error import AvailableToolsLimitExceededError
from .types.beta.beta_environment_archived_error import BetaEnvironmentArchivedError
from .types.beta.beta_environment_not_found_error import BetaEnvironmentNotFoundError
from .types.compaction_nothing_to_summarize_error import CompactionNothingToSummarizeError
from .types.shared.cmek_context_unavailable_error import CMEKContextUnavailableError
from .types.shared.cmek_key_network_blocked_error import CMEKKeyNetworkBlockedError
from .types.compaction_tool_changes_mismatch_error import CompactionToolChangesMismatchError
from .types.shared.sandbox_egress_restricted_error import SandboxEgressRestrictedError
from .types.skill_read_blocked_undecryptable_error import SkillReadBlockedUndecryptableError
from .types.organization.external_key_changed_error import ExternalKeyChangedError
from .types.organization.key_profile_mismatch_error import KeyProfileMismatchError
from .types.beta.organization.beta_scan_failed_error import BetaScanFailedError
from .types.organization.invite_already_exists_error import InviteAlreadyExistsError
from .types.shared.claude_code_version_too_old_error import ClaudeCodeVersionTooOldError
from .types.beta.beta_organization_not_eligible_error import BetaOrganizationNotEligibleError
from .types.beta.organization.beta_scan_pending_error import BetaScanPendingError
from .types.beta_external_key_provider_mismatch_error import BetaExternalKeyProviderMismatchError
from .types.compaction_too_many_tool_references_error import CompactionTooManyToolReferencesError
from .types.shared.contract_spend_limit_reached_error import ContractSpendLimitReachedError
from .types.shared.enforced_spend_limit_reached_error import EnforcedSpendLimitReachedError
from .types.shared.parent_organization_required_error import ParentOrganizationRequiredError
from .types.user_profile_billing_not_authorized_error import UserProfileBillingNotAuthorizedError
from .types.beta.beta_human_review_not_available_error import BetaHumanReviewNotAvailableError
from .types.beta.beta_invalid_config_type_change_error import BetaInvalidConfigTypeChangeError
from .types.shared.request_body_encoding_invalid_error import RequestBodyEncodingInvalidError
from .types.beta.beta_environment_create_disabled_error import BetaEnvironmentCreateDisabledError
from .types.beta.beta_environment_update_disabled_error import BetaEnvironmentUpdateDisabledError
from .types.beta.organization.beta_bundle_on_call_error import BetaBundleOnCallError
from .types.beta.organization.beta_grant_required_error import BetaGrantRequiredError
from .types.organization.email_domain_not_allowed_error import EmailDomainNotAllowedError
from .types.organization.storage_profile_mismatch_error import StorageProfileMismatchError
from .types.beta_organization_not_enrolled_in_beta_error import BetaOrganizationNotEnrolledInBetaError
from .types.organization.cannot_remove_last_member_error import CannotRemoveLastMemberError
from .types.shared.organization_type_not_supported_error import OrganizationTypeNotSupportedError
from .types.shared.workspace_human_review_disabled_error import WorkspaceHumanReviewDisabledError
from .types.beta.organization.beta_skill_name_taken_error import BetaSkillNameTakenError
from .types.organization.org_api_key_limit_exceeded_error import OrgAPIKeyLimitExceededError
from .types.organization.workspace_policy_violation_error import WorkspacePolicyViolationError
from .types.beta.organization.beta_plugin_name_taken_error import BetaPluginNameTakenError
from .types.shared.request_body_encoding_unsupported_error import RequestBodyEncodingUnsupportedError
from .types.beta.beta_authorization_check_unavailable_error import BetaAuthorizationCheckUnavailableError
from .types.beta.organization.beta_unsupported_region_error import BetaUnsupportedRegionError
from .types.organization.workspace_created_incomplete_error import WorkspaceCreatedIncompleteError
from .types.shared.claude_code_key_creator_not_member_error import ClaudeCodeKeyCreatorNotMemberError
from .types.beta.organization.beta_invalid_storage_arn_error import BetaInvalidStorageARNError
from .types.beta.organization.beta_cannot_sign_out_self_error import BetaCannotSignOutSelfError
from .types.beta.organization.beta_provider_not_allowed_error import BetaProviderNotAllowedError
from .types.beta.organization.beta_rbac_group_not_found_error import BetaRBACGroupNotFoundError
from .types.beta.organization.beta_registration_pending_error import BetaRegistrationPendingError
from .types.organization.external_key_validation_failed_error import ExternalKeyValidationFailedError
from .types.organization.rbac_group_grants_owner_access_error import RBACGroupGrantsOwnerAccessError
from .types.beta.organization.beta_api_key_scope_missing_error import BetaAPIKeyScopeMissingError
from .types.beta.organization.beta_cannot_sign_out_owner_error import BetaCannotSignOutOwnerError
from .types.organization.storage_attached_during_archive_error import StorageAttachedDuringArchiveError
from .types.organization.workspace_member_limit_exceeded_error import WorkspaceMemberLimitExceededError
from .types.shared.request_body_too_large_after_decoding_error import RequestBodyTooLargeAfterDecodingError
from .types.beta.organization.beta_storage_not_attachable_error import BetaStorageNotAttachableError
from .types.organization.external_key_in_workspace_policy_error import ExternalKeyInWorkspacePolicyError
from .types.organization.workspace_api_key_limit_exceeded_error import WorkspaceAPIKeyLimitExceededError
from .types.beta.organization.beta_external_storage_in_use_error import BetaExternalStorageInUseError
from .types.organization.external_key_validation_timed_out_error import ExternalKeyValidationTimedOutError
from .types.shared.linked_organization_billing_unavailable_error import LinkedOrganizationBillingUnavailableError
from .types.shared.linked_organization_spend_limit_reached_error import LinkedOrganizationSpendLimitReachedError
from .types.organization.rbac_group_owner_access_unconfirmed_error import RBACGroupOwnerAccessUnconfirmedError
from .types.beta.organization.beta_storage_already_registered_error import BetaStorageAlreadyRegisteredError
from .types.beta.organization.beta_storage_verification_failed_error import BetaStorageVerificationFailedError
from .types.beta.organization.beta_storage_attach_limit_reached_error import BetaStorageAttachLimitReachedError
from .types.beta.organization.beta_storage_changed_concurrently_error import BetaStorageChangedConcurrentlyError
from .types.beta.organization.beta_transcripts_storage_required_error import BetaTranscriptsStorageRequiredError
from .types.beta_gcp_project_controlled_by_another_organization_error import (
    BetaGCPProjectControlledByAnotherOrganizationError,
)
from .types.beta.environments.beta_heartbeat_precondition_failed_error import BetaHeartbeatPreconditionFailedError
from .types.beta.organization.beta_cannot_sign_out_primary_owner_error import BetaCannotSignOutPrimaryOwnerError
from .types.beta.organization.beta_claude_tag_writes_not_enabled_error import BetaClaudeTagWritesNotEnabledError
from .types.beta.organization.beta_cannot_sign_out_managed_member_error import BetaCannotSignOutManagedMemberError
from .types.beta.organization.beta_external_storage_not_available_error import BetaExternalStorageNotAvailableError
from .types.beta.organization.beta_storage_profile_still_required_error import BetaStorageProfileStillRequiredError
from .types.beta.organization.beta_workspace_changed_concurrently_error import BetaWorkspaceChangedConcurrentlyError
from .types.beta.organization.beta_bundle_attachment_not_supported_error import BetaBundleAttachmentNotSupportedError
from .types.beta.organization.beta_cannot_sign_out_membership_admin_error import BetaCannotSignOutMembershipAdminError
from .types.beta.organization.beta_cannot_sign_out_privileged_member_error import BetaCannotSignOutPrivilegedMemberError
from .types.organization.cannot_invite_emails_with_unverified_domains_error import (
    CannotInviteEmailsWithUnverifiedDomainsError,
)
from .types.beta.organization.beta_compliance_configuration_restricted_error import (
    BetaComplianceConfigurationRestrictedError,
)
from .types.beta.organization.beta_external_storage_in_workspace_policy_error import (
    BetaExternalStorageInWorkspacePolicyError,
)
from .types.beta.organization.claude_code.beta_cmek_feature_unsupported_error import BetaCMEKFeatureUnsupportedError
from .types.beta.organization.beta_human_review_on_with_external_storage_error import (
    BetaHumanReviewOnWithExternalStorageError,
)
from .types.beta.organization.beta_slack_channel_set_up_settings_refused_error import (
    BetaSlackChannelSetUpSettingsRefusedError,
)
from .types.beta.organization.beta_slack_channel_set_up_settings_conflict_error import (
    BetaSlackChannelSetUpSettingsConflictError,
)
from .types.beta.organization.beta_spend_limits_admin_api_writes_not_enabled_error import (
    BetaSpendLimitsAdminAPIWritesNotEnabledError,
)
from .types.beta.organization.beta_organization_level_scoped_api_key_required_error import (
    BetaOrganizationLevelScopedAPIKeyRequiredError,
)
from .types.beta.organization.beta_slack_channel_set_up_environment_not_found_error import (
    BetaSlackChannelSetUpEnvironmentNotFoundError,
)
from .types.beta.organization.claude_code.beta_rbac_group_order_limit_exceeded_error import (
    BetaRBACGroupOrderLimitExceededError,
)
from .types.beta.organization.claude_code.beta_settings_history_limit_exceeded_error import (
    BetaSettingsHistoryLimitExceededError,
)
from .types.beta.organization.claude_code.beta_settings_document_limit_exceeded_error import (
    BetaSettingsDocumentLimitExceededError,
)
from .types.beta.organization.claude_code.beta_rbac_group_managed_settings_not_found_error import (
    BetaRBACGroupManagedSettingsNotFoundError,
)

ERROR_CLASSES: dict[tuple[int, str | None], type[APIStatusError]] = {
    (400, None): BadRequestError,
    (401, None): AuthenticationError,
    (402, None): PaymentRequiredError,
    (403, None): PermissionDeniedError,
    (404, None): NotFoundError,
    (408, None): RequestTimeoutError,
    (409, None): ConflictError,
    (412, None): PreconditionFailedError,
    (413, None): ContentTooLargeError,
    (422, None): UnprocessableEntityError,
    (429, None): RateLimitError,
    (431, None): RequestHeaderFieldsTooLargeError,
    (499, None): ClientClosedRequestError,
    (501, None): HTTPNotImplementedError,
    (503, None): ServiceUnavailableError,
    (504, None): GatewayTimeoutError,
    (529, None): OverloadedError,
    (400, "already_member"): AlreadyMemberError,
    (400, "approval_required"): BetaApprovalRequiredError,
    (400, "available_tools_limit_exceeded"): AvailableToolsLimitExceededError,
    (400, "bundle_attachment_not_supported"): BetaBundleAttachmentNotSupportedError,
    (400, "bundle_on_call"): BetaBundleOnCallError,
    (400, "cannot_invite_emails_with_unverified_domains"): CannotInviteEmailsWithUnverifiedDomainsError,
    (400, "cannot_remove_last_member"): CannotRemoveLastMemberError,
    (400, "cannot_sign_out_primary_owner"): BetaCannotSignOutPrimaryOwnerError,
    (400, "cannot_sign_out_self"): BetaCannotSignOutSelfError,
    (400, "claude_code_key_creator_not_member"): ClaudeCodeKeyCreatorNotMemberError,
    (400, "claude_code_version_too_old"): ClaudeCodeVersionTooOldError,
    (400, "cmek_feature_unsupported"): BetaCMEKFeatureUnsupportedError,
    (400, "cmek_key_disabled"): CMEKKeyDisabledError,
    (400, "cmek_key_network_blocked"): CMEKKeyNetworkBlockedError,
    (400, "cmek_not_approved"): BetaCMEKNotApprovedError,
    (400, "compaction_block_ambiguous"): CompactionBlockAmbiguousError,
    (400, "compaction_block_misplaced"): CompactionBlockMisplacedError,
    (400, "compaction_content_mismatch"): CompactionContentMismatchError,
    (400, "compaction_incomplete_turn"): CompactionIncompleteTurnError,
    (400, "compaction_nothing_to_summarize"): CompactionNothingToSummarizeError,
    (400, "compaction_signature_invalid"): CompactionSignatureInvalidError,
    (400, "compaction_too_many_tool_references"): CompactionTooManyToolReferencesError,
    (400, "compaction_tool_changes_mismatch"): CompactionToolChangesMismatchError,
    (400, "email_domain_not_allowed"): EmailDomainNotAllowedError,
    (400, "environment_archived"): BetaEnvironmentArchivedError,
    (400, "external_key_in_workspace_policy"): ExternalKeyInWorkspacePolicyError,
    (400, "external_key_not_found"): BetaExternalKeyNotFoundError,
    (400, "external_key_provider_mismatch"): BetaExternalKeyProviderMismatchError,
    (400, "external_key_validation_failed"): ExternalKeyValidationFailedError,
    (400, "external_key_validation_timed_out"): ExternalKeyValidationTimedOutError,
    (400, "external_storage_in_use"): BetaExternalStorageInUseError,
    (400, "external_storage_in_workspace_policy"): BetaExternalStorageInWorkspacePolicyError,
    (400, "external_storage_not_available"): BetaExternalStorageNotAvailableError,
    (400, "file_not_downloadable"): FileNotDownloadableError,
    (400, "gcp_project_not_verified"): BetaGCPProjectNotVerifiedError,
    (400, "grant_required"): BetaGrantRequiredError,
    (400, "human_review_not_available"): BetaHumanReviewNotAvailableError,
    (400, "human_review_on_with_external_storage"): BetaHumanReviewOnWithExternalStorageError,
    (400, "image_dimensions_too_large"): ImageDimensionsTooLargeError,
    (400, "invalid_config_type_change"): BetaInvalidConfigTypeChangeError,
    (400, "invalid_metadata"): BetaInvalidMetadataError,
    (400, "invalid_storage_arn"): BetaInvalidStorageARNError,
    (400, "invite_already_exists"): InviteAlreadyExistsError,
    (400, "key_profile_mismatch"): KeyProfileMismatchError,
    (400, "org_api_key_limit_exceeded"): OrgAPIKeyLimitExceededError,
    (400, "org_member_limit_exceeded"): OrgMemberLimitExceededError,
    (400, "organization_not_eligible"): BetaOrganizationNotEligibleError,
    (400, "organization_not_enrolled_in_beta"): BetaOrganizationNotEnrolledInBetaError,
    (400, "organization_on_hold"): OrganizationOnHoldError,
    (400, "organization_type_not_supported"): OrganizationTypeNotSupportedError,
    (400, "parent_organization_required"): ParentOrganizationRequiredError,
    (400, "provider_not_allowed"): BetaProviderNotAllowedError,
    (400, "rbac_group_grants_owner_access"): RBACGroupGrantsOwnerAccessError,
    (400, "rbac_group_order_limit_exceeded"): BetaRBACGroupOrderLimitExceededError,
    (400, "rbac_group_owner_access_unconfirmed"): RBACGroupOwnerAccessUnconfirmedError,
    (400, "region_not_supported"): BetaRegionNotSupportedError,
    (400, "request_body_encoding_invalid"): RequestBodyEncodingInvalidError,
    (400, "request_body_encoding_unsupported"): RequestBodyEncodingUnsupportedError,
    (400, "request_body_timeout"): BetaRequestBodyTimeoutError,
    (400, "scan_failed"): BetaScanFailedError,
    (400, "settings_document_limit_exceeded"): BetaSettingsDocumentLimitExceededError,
    (400, "settings_history_limit_exceeded"): BetaSettingsHistoryLimitExceededError,
    (400, "slack_channel_set_up_settings_refused"): BetaSlackChannelSetUpSettingsRefusedError,
    (400, "storage_attach_limit_reached"): BetaStorageAttachLimitReachedError,
    (400, "storage_not_approved"): BetaStorageNotApprovedError,
    (400, "storage_not_attachable"): BetaStorageNotAttachableError,
    (400, "storage_profile_mismatch"): StorageProfileMismatchError,
    (400, "storage_profile_still_required"): BetaStorageProfileStillRequiredError,
    (400, "storage_quota_exceeded"): StorageQuotaExceededError,
    (400, "storage_verification_failed"): BetaStorageVerificationFailedError,
    (400, "thread_already_continued"): ThreadAlreadyContinuedError,
    (400, "thread_continue_in_flight"): ThreadContinueInFlightError,
    (400, "thread_fingerprint_mismatch"): ThreadFingerprintMismatchError,
    (400, "thread_unsupported_request"): ThreadUnsupportedRequestError,
    (400, "tool_name_conflict"): ToolNameConflictError,
    (400, "tool_reference_unresolved"): ToolReferenceUnresolvedError,
    (400, "transcripts_storage_required"): BetaTranscriptsStorageRequiredError,
    (400, "unsupported_charset"): BetaUnsupportedCharsetError,
    (400, "unsupported_region"): BetaUnsupportedRegionError,
    (400, "user_profile_not_found"): UserProfileNotFoundError,
    (400, "user_profile_required"): UserProfileRequiredError,
    (400, "workspace_api_key_limit_exceeded"): WorkspaceAPIKeyLimitExceededError,
    (400, "workspace_human_review_disabled"): WorkspaceHumanReviewDisabledError,
    (400, "workspace_member_limit_exceeded"): WorkspaceMemberLimitExceededError,
    (400, "workspace_policy_violation"): WorkspacePolicyViolationError,
    (402, "linked_organization_billing_unavailable"): LinkedOrganizationBillingUnavailableError,
    (402, "linked_organization_spend_limit_reached"): LinkedOrganizationSpendLimitReachedError,
    (403, "api_key_scope_missing"): BetaAPIKeyScopeMissingError,
    (403, "cannot_sign_out_managed_member"): BetaCannotSignOutManagedMemberError,
    (403, "cannot_sign_out_membership_admin"): BetaCannotSignOutMembershipAdminError,
    (403, "cannot_sign_out_owner"): BetaCannotSignOutOwnerError,
    (403, "cannot_sign_out_privileged_member"): BetaCannotSignOutPrivilegedMemberError,
    (403, "claude_tag_writes_not_enabled"): BetaClaudeTagWritesNotEnabledError,
    (403, "compliance_configuration_restricted"): BetaComplianceConfigurationRestrictedError,
    (403, "environment_create_disabled"): BetaEnvironmentCreateDisabledError,
    (403, "environment_update_disabled"): BetaEnvironmentUpdateDisabledError,
    (403, "organization_level_scoped_api_key_required"): BetaOrganizationLevelScopedAPIKeyRequiredError,
    (403, "sandbox_egress_restricted"): SandboxEgressRestrictedError,
    (403, "spend_limits_admin_api_writes_not_enabled"): BetaSpendLimitsAdminAPIWritesNotEnabledError,
    (403, "user_profile_billing_not_authorized"): UserProfileBillingNotAuthorizedError,
    (403, "user_profile_not_billable"): UserProfileNotBillableError,
    (404, "environment_not_found"): BetaEnvironmentNotFoundError,
    (404, "file_expired"): FileExpiredError,
    (404, "rbac_group_managed_settings_not_found"): BetaRBACGroupManagedSettingsNotFoundError,
    (404, "rbac_group_not_found"): BetaRBACGroupNotFoundError,
    (404, "rbac_role_not_found"): RBACRoleNotFoundError,
    (404, "slack_channel_set_up_environment_not_found"): BetaSlackChannelSetUpEnvironmentNotFoundError,
    (404, "thread_not_found"): ThreadNotFoundError,
    (409, "concurrent_membership_change"): ConcurrentMembershipChangeError,
    (409, "external_key_changed"): ExternalKeyChangedError,
    (409, "gcp_project_controlled_by_another_organization"): BetaGCPProjectControlledByAnotherOrganizationError,
    (409, "plugin_name_taken"): BetaPluginNameTakenError,
    (409, "scan_pending"): BetaScanPendingError,
    (409, "skill_name_taken"): BetaSkillNameTakenError,
    (409, "skill_read_blocked_undecryptable"): SkillReadBlockedUndecryptableError,
    (409, "slack_channel_set_up_settings_conflict"): BetaSlackChannelSetUpSettingsConflictError,
    (409, "storage_already_registered"): BetaStorageAlreadyRegisteredError,
    (409, "storage_attached_during_archive"): StorageAttachedDuringArchiveError,
    (409, "storage_changed_concurrently"): BetaStorageChangedConcurrentlyError,
    (409, "storage_in_use"): BetaStorageInUseError,
    (409, "workspace_changed_concurrently"): BetaWorkspaceChangedConcurrentlyError,
    (412, "heartbeat_precondition_failed"): BetaHeartbeatPreconditionFailedError,
    (413, "request_body_too_large_after_decoding"): RequestBodyTooLargeAfterDecodingError,
    (429, "contract_spend_limit_reached"): ContractSpendLimitReachedError,
    (429, "enforced_spend_limit_reached"): EnforcedSpendLimitReachedError,
    (429, "ramp_limit_exceeded"): RampLimitExceededError,
    (503, "authorization_check_unavailable"): BetaAuthorizationCheckUnavailableError,
    (503, "change_outcome_unknown"): ChangeOutcomeUnknownError,
    (503, "cmek_context_unavailable"): CMEKContextUnavailableError,
    (503, "cmek_key_unreachable"): CMEKKeyUnreachableError,
    (503, "registration_pending"): BetaRegistrationPendingError,
    (503, "workspace_created_incomplete"): WorkspaceCreatedIncompleteError,
    (529, "compaction_unavailable"): CompactionUnavailableError,
}


def make_status_error(err_msg: str, *, body: object, response: httpx2.Response) -> APIStatusError:
    error_class = (
        ERROR_CLASSES.get((response.status_code, extract_error_code(body)))
        or ERROR_CLASSES.get((response.status_code, None))
        or (InternalServerError if response.status_code >= 500 else APIStatusError)
    )
    return error_class(err_msg, response=response, body=body)
