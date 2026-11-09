from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from ..file_expired_error_details import FileExpiredErrorDetails
from ..thread_not_found_error_details import ThreadNotFoundErrorDetails
from .cmek_key_disabled_error_details import CMEKKeyDisabledErrorDetails
from ..tool_name_conflict_error_details import ToolNameConflictErrorDetails
from .ramp_limit_exceeded_error_details import RampLimitExceededErrorDetails
from .cmek_key_unreachable_error_details import CMEKKeyUnreachableErrorDetails
from .organization_on_hold_error_details import OrganizationOnHoldErrorDetails
from ..file_not_downloadable_error_details import FileNotDownloadableErrorDetails
from ..compaction_unavailable_error_details import CompactionUnavailableErrorDetails
from ..storage_quota_exceeded_error_details import StorageQuotaExceededErrorDetails
from ..user_profile_not_found_error_details import UserProfileNotFoundErrorDetails
from .cmek_context_unavailable_error_details import CMEKContextUnavailableErrorDetails
from .cmek_key_network_blocked_error_details import CMEKKeyNetworkBlockedErrorDetails
from ..beta_unsupported_charset_error_details import BetaUnsupportedCharsetErrorDetails
from ..thread_already_continued_error_details import ThreadAlreadyContinuedErrorDetails
from .sandbox_egress_restricted_error_details import SandboxEgressRestrictedErrorDetails
from ..org_member_limit_exceeded_error_details import OrgMemberLimitExceededErrorDetails
from ..thread_continue_in_flight_error_details import ThreadContinueInFlightErrorDetails
from ..tool_reference_unresolved_error_details import ToolReferenceUnresolvedErrorDetails
from ..beta.beta_invalid_metadata_error_details import BetaInvalidMetadataErrorDetails
from ..compaction_block_ambiguous_error_details import CompactionBlockAmbiguousErrorDetails
from ..compaction_block_misplaced_error_details import CompactionBlockMisplacedErrorDetails
from ..compaction_incomplete_turn_error_details import CompactionIncompleteTurnErrorDetails
from ..thread_unsupported_request_error_details import ThreadUnsupportedRequestErrorDetails
from .claude_code_version_too_old_error_details import ClaudeCodeVersionTooOldErrorDetails
from ..compaction_content_mismatch_error_details import CompactionContentMismatchErrorDetails
from ..organization.already_member_error_details import AlreadyMemberErrorDetails
from ..thread_fingerprint_mismatch_error_details import ThreadFingerprintMismatchErrorDetails
from .enforced_spend_limit_reached_error_details import EnforcedSpendLimitReachedErrorDetails
from ..compaction_signature_invalid_error_details import CompactionSignatureInvalidErrorDetails
from ..concurrent_membership_change_error_details import ConcurrentMembershipChangeErrorDetails
from .request_body_encoding_invalid_error_details import RequestBodyEncodingInvalidErrorDetails
from ..available_tools_limit_exceeded_error_details import AvailableToolsLimitExceededErrorDetails
from ..beta.beta_environment_archived_error_details import BetaEnvironmentArchivedErrorDetails
from .organization_type_not_supported_error_details import OrganizationTypeNotSupportedErrorDetails
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
from ..beta.organization.beta_scan_pending_error_details import BetaScanPendingErrorDetails
from ..compaction_too_many_tool_references_error_details import CompactionTooManyToolReferencesErrorDetails
from ..beta.beta_invalid_config_type_change_error_details import BetaInvalidConfigTypeChangeErrorDetails
from .request_body_too_large_after_decoding_error_details import RequestBodyTooLargeAfterDecodingErrorDetails
from ..beta.beta_environment_create_disabled_error_details import BetaEnvironmentCreateDisabledErrorDetails
from ..beta.beta_environment_update_disabled_error_details import BetaEnvironmentUpdateDisabledErrorDetails
from ..organization.email_domain_not_allowed_error_details import EmailDomainNotAllowedErrorDetails
from ..beta_organization_not_enrolled_in_beta_error_details import BetaOrganizationNotEnrolledInBetaErrorDetails
from ..organization.cannot_remove_last_member_error_details import CannotRemoveLastMemberErrorDetails
from ..beta.organization.beta_skill_name_taken_error_details import BetaSkillNameTakenErrorDetails
from ..organization.org_api_key_limit_exceeded_error_details import OrgAPIKeyLimitExceededErrorDetails
from ..organization.workspace_policy_violation_error_details import WorkspacePolicyViolationErrorDetails
from ..beta.organization.beta_plugin_name_taken_error_details import BetaPluginNameTakenErrorDetails
from ..beta.organization.beta_cannot_sign_out_self_error_details import BetaCannotSignOutSelfErrorDetails
from ..beta.organization.beta_registration_pending_error_details import BetaRegistrationPendingErrorDetails
from ..organization.external_key_validation_failed_error_details import ExternalKeyValidationFailedErrorDetails
from ..organization.rbac_group_grants_owner_access_error_details import RBACGroupGrantsOwnerAccessErrorDetails
from ..beta.organization.beta_api_key_scope_missing_error_details import BetaAPIKeyScopeMissingErrorDetails
from ..beta.organization.beta_cannot_sign_out_owner_error_details import BetaCannotSignOutOwnerErrorDetails
from ..organization.workspace_member_limit_exceeded_error_details import WorkspaceMemberLimitExceededErrorDetails
from ..organization.external_key_in_workspace_policy_error_details import ExternalKeyInWorkspacePolicyErrorDetails
from ..organization.workspace_api_key_limit_exceeded_error_details import WorkspaceAPIKeyLimitExceededErrorDetails
from ..organization.external_key_validation_timed_out_error_details import ExternalKeyValidationTimedOutErrorDetails
from ..organization.rbac_group_owner_access_unconfirmed_error_details import RBACGroupOwnerAccessUnconfirmedErrorDetails
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
        OrganizationOnHoldErrorDetails,
        RequestBodyEncodingInvalidErrorDetails,
        RequestBodyEncodingUnsupportedErrorDetails,
        ThreadAlreadyContinuedErrorDetails,
        ThreadContinueInFlightErrorDetails,
        ThreadFingerprintMismatchErrorDetails,
        ThreadUnsupportedRequestErrorDetails,
        ToolNameConflictErrorDetails,
        ToolReferenceUnresolvedErrorDetails,
        ThreadNotFoundErrorDetails,
        SkillReadBlockedUndecryptableErrorDetails,
        RequestBodyTooLargeAfterDecodingErrorDetails,
        EnforcedSpendLimitReachedErrorDetails,
        RampLimitExceededErrorDetails,
        CMEKKeyUnreachableErrorDetails,
        CompactionUnavailableErrorDetails,
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
        WorkspaceMemberLimitExceededErrorDetails,
        OrganizationTypeNotSupportedErrorDetails,
        BetaEnvironmentCreateDisabledErrorDetails,
        BetaEnvironmentArchivedErrorDetails,
        BetaInvalidConfigTypeChangeErrorDetails,
        BetaEnvironmentUpdateDisabledErrorDetails,
        BetaHeartbeatPreconditionFailedErrorDetails,
        BetaInvalidMetadataErrorDetails,
        BetaCannotSignOutPrimaryOwnerErrorDetails,
        BetaCannotSignOutSelfErrorDetails,
        BetaOrganizationNotEnrolledInBetaErrorDetails,
        BetaCannotSignOutManagedMemberErrorDetails,
        BetaCannotSignOutMembershipAdminErrorDetails,
        BetaCannotSignOutOwnerErrorDetails,
        BetaCannotSignOutPrivilegedMemberErrorDetails,
        BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails,
        BetaUnsupportedCharsetErrorDetails,
        BetaPluginNameTakenErrorDetails,
        BetaSkillNameTakenErrorDetails,
        BetaRegistrationPendingErrorDetails,
        BetaScanFailedErrorDetails,
        BetaScanPendingErrorDetails,
        BetaSlackChannelSetUpSettingsRefusedErrorDetails,
        BetaAPIKeyScopeMissingErrorDetails,
        BetaClaudeTagWritesNotEnabledErrorDetails,
        BetaComplianceConfigurationRestrictedErrorDetails,
        BetaOrganizationLevelScopedAPIKeyRequiredErrorDetails,
        BetaEnvironmentNotFoundErrorDetails,
        BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails,
        BetaSlackChannelSetUpSettingsConflictErrorDetails,
    ],
    UnionDiscriminator("error_code"),
]
