# Shared Types

```python
from anthropic.types import (
    APIErrorObject,
    AuthenticationError,
    BillingError,
    ErrorObject,
    ErrorResponse,
    ErrorType,
    GatewayTimeoutError,
    InvalidRequestError,
    NotFoundError,
    OverloadedError,
    PermissionError,
    RateLimitError,
)
```

# Messages

Types:

```python
from anthropic.types import (
    Base64ImageSourceParam,
    Base64PDFSource,
    Base64PDFSourceParam,
    BashCodeExecutionOutputBlock,
    BashCodeExecutionOutputBlockParam,
    BashCodeExecutionResultBlock,
    BashCodeExecutionResultBlockParam,
    BashCodeExecutionToolResultBlock,
    BashCodeExecutionToolResultBlockParam,
    BashCodeExecutionToolResultError,
    BashCodeExecutionToolResultErrorCode,
    BashCodeExecutionToolResultErrorParam,
    BrowserCloseTabConfigParam,
    BrowserDoubleClickConfigParam,
    BrowserFileUploadConfigParam,
    BrowserFindConfigParam,
    BrowserFormInputConfigParam,
    BrowserGetPageTextConfigParam,
    BrowserHoldKeyConfigParam,
    BrowserHoverConfigParam,
    BrowserJavascriptExecConfigParam,
    BrowserKeyConfigParam,
    BrowserLeftClickConfigParam,
    BrowserLeftClickDragConfigParam,
    BrowserLeftMouseDownConfigParam,
    BrowserLeftMouseUpConfigParam,
    BrowserListTabsConfigParam,
    BrowserMiddleClickConfigParam,
    BrowserMouseMoveConfigParam,
    BrowserNavigateConfigParam,
    BrowserNewTabConfigParam,
    BrowserReadConsoleConfigParam,
    BrowserReadNetworkConfigParam,
    BrowserReadPageConfigParam,
    BrowserRightClickConfigParam,
    BrowserScreenshotConfigParam,
    BrowserScrollConfigParam,
    BrowserScrollToConfigParam,
    BrowserStateBlockParam,
    BrowserStateChangeParam,
    BrowserStateChangeDownloadCompletedParam,
    BrowserStateChangeDownloadFailedParam,
    BrowserStateChangeDownloadStartedParam,
    BrowserStateChangeTabOpenedParam,
    BrowserStateTabEntryParam,
    BrowserSwitchTabConfigParam,
    BrowserToolset20260801Param,
    BrowserToolsetConfigsParam,
    BrowserTripleClickConfigParam,
    BrowserTypeConfigParam,
    BrowserWaitConfigParam,
    BrowserZoomConfigParam,
    CacheControlEphemeralParam,
    CacheCreation,
    CacheMissMessagesChanged,
    CacheMissModelChanged,
    CacheMissPreviousMessageNotFound,
    CacheMissReason,
    CacheMissSystemChanged,
    CacheMissToolsChanged,
    CacheMissUnavailable,
    CitationCharLocation,
    CitationCharLocationParam,
    CitationContentBlockLocation,
    CitationContentBlockLocationParam,
    CitationPageLocation,
    CitationPageLocationParam,
    CitationSearchResultLocationParam,
    CitationWebSearchResultLocationParam,
    CitationsConfig,
    CitationsConfigParam,
    CitationsDelta,
    CitationsSearchResultLocation,
    CitationsWebSearchResultLocation,
    CodeExecutionOutputBlock,
    CodeExecutionOutputBlockParam,
    CodeExecutionResultBlock,
    CodeExecutionResultBlockParam,
    CodeExecutionTool20250522Param,
    CodeExecutionTool20250825Param,
    CodeExecutionTool20260120Param,
    CodeExecutionTool20260521Param,
    CodeExecutionToolResultBlock,
    CodeExecutionToolResultBlockContent,
    CodeExecutionToolResultBlockParam,
    CodeExecutionToolResultBlockParamContentParam,
    CodeExecutionToolResultError,
    CodeExecutionToolResultErrorCode,
    CodeExecutionToolResultErrorParam,
    ComputerCursorPositionConfigParam,
    ComputerDoubleClickConfigParam,
    ComputerHoldKeyConfigParam,
    ComputerKeyConfigParam,
    ComputerLeftClickConfigParam,
    ComputerLeftClickDragConfigParam,
    ComputerLeftMouseDownConfigParam,
    ComputerLeftMouseUpConfigParam,
    ComputerMiddleClickConfigParam,
    ComputerMouseMoveConfigParam,
    ComputerRightClickConfigParam,
    ComputerScreenshotConfigParam,
    ComputerScrollConfigParam,
    ComputerToolset20260801Param,
    ComputerToolsetConfigsParam,
    ComputerTripleClickConfigParam,
    ComputerTypeConfigParam,
    ComputerWaitConfigParam,
    ComputerZoomConfigParam,
    Container,
    ContainerParams,
    ContainerSkill,
    ContainerUploadBlock,
    ContainerUploadBlockParam,
    ContentBlock,
    ContentBlockParam,
    ContentBlockSourceParam,
    ContentBlockSourceContentParam,
    Diagnostics,
    DiagnosticsParam,
    DirectCaller,
    DirectCallerParam,
    DocumentBlock,
    DocumentBlockParam,
    EncryptedCodeExecutionResultBlock,
    EncryptedCodeExecutionResultBlockParam,
    FileDocumentSourceParam,
    FileImageSourceParam,
    ImageBlockParam,
    ImageTransformationsParam,
    InputJSONDelta,
    JSONOutputFormatParam,
    MemoryTool20250818Param,
    Message,
    MessageCountTokensToolParam,
    MessageCreateParamsContainerParam,
    MessageDeltaUsage,
    MessageParam,
    MessageTokensCount,
    MetadataParam,
    Model,
    ModelParam,
    OutputConfigParam,
    OutputTokensDetails,
    PlainTextSource,
    PlainTextSourceParam,
    RawContentBlockDelta,
    RawContentBlockDeltaEvent,
    RawContentBlockStartEvent,
    RawContentBlockStopEvent,
    RawMessageDeltaEvent,
    RawMessageStartEvent,
    RawMessageStopEvent,
    RawMessageStreamEvent,
    RedactedThinkingBlock,
    RedactedThinkingBlockParam,
    RefusalStopDetails,
    SearchResultBlockParam,
    ServerToolCaller,
    ServerToolCallerParam,
    ServerToolCaller20260120,
    ServerToolCaller20260120Param,
    ServerToolUsage,
    ServerToolUseBlock,
    ServerToolUseBlockParam,
    SignatureDelta,
    SkillParams,
    StopReason,
    TextBlock,
    TextBlockParam,
    TextCitation,
    TextCitationParam,
    TextDelta,
    TextEditorCodeExecutionCreateResultBlock,
    TextEditorCodeExecutionCreateResultBlockParam,
    TextEditorCodeExecutionStrReplaceResultBlock,
    TextEditorCodeExecutionStrReplaceResultBlockParam,
    TextEditorCodeExecutionToolResultBlock,
    TextEditorCodeExecutionToolResultBlockParam,
    TextEditorCodeExecutionToolResultError,
    TextEditorCodeExecutionToolResultErrorCode,
    TextEditorCodeExecutionToolResultErrorParam,
    TextEditorCodeExecutionViewResultBlock,
    TextEditorCodeExecutionViewResultBlockParam,
    ThinkingBlock,
    ThinkingBlockParam,
    ThinkingConfigAdaptiveParam,
    ThinkingConfigBetweenToolsParam,
    ThinkingConfigDisabledParam,
    ThinkingConfigEnabledParam,
    ThinkingConfigParam,
    ThinkingDelta,
    ToolParam,
    ToolBash20250124Param,
    ToolChoiceParam,
    ToolChoiceAnyParam,
    ToolChoiceAutoParam,
    ToolChoiceNoneParam,
    ToolChoiceToolParam,
    ToolReferenceBlock,
    ToolReferenceBlockParam,
    ToolResultBlockParam,
    ToolSearchToolBm25_20251119Param,
    ToolSearchToolRegex20251119Param,
    ToolSearchToolResultBlock,
    ToolSearchToolResultBlockParam,
    ToolSearchToolResultError,
    ToolSearchToolResultErrorCode,
    ToolSearchToolResultErrorParam,
    ToolSearchToolSearchResultBlock,
    ToolSearchToolSearchResultBlockParam,
    ToolTextEditor20250124Param,
    ToolTextEditor20250429Param,
    ToolTextEditor20250728Param,
    ToolUnionParam,
    ToolUseBlock,
    ToolUseBlockParam,
    URLImageSourceParam,
    URLPDFSourceParam,
    Usage,
    UserLocationParam,
    WebFetchBlock,
    WebFetchBlockParam,
    WebFetchTool20250910Param,
    WebFetchTool20260209Param,
    WebFetchTool20260309Param,
    WebFetchTool20260318Param,
    WebFetchToolResultBlock,
    WebFetchToolResultBlockParam,
    WebFetchToolResultErrorBlock,
    WebFetchToolResultErrorBlockParam,
    WebFetchToolResultErrorCode,
    WebFetchURLSourceAllParam,
    WebFetchURLSourceExceptParam,
    WebFetchURLSourceNoneParam,
    WebFetchURLSourceOnlyParam,
    WebFetchURLSourceToolReferenceParam,
    WebFetchURLSourcesParam,
    WebSearchResultBlock,
    WebSearchResultBlockParam,
    WebSearchTool20250305Param,
    WebSearchTool20260209Param,
    WebSearchTool20260318Param,
    WebSearchToolRequestErrorParam,
    WebSearchToolResultBlock,
    WebSearchToolResultBlockContent,
    WebSearchToolResultBlockParam,
    WebSearchToolResultBlockParamContentParam,
    WebSearchToolResultError,
    WebSearchToolResultErrorCode,
    MessageStreamEvent,
    MessageStartEvent,
    MessageDeltaEvent,
    MessageStopEvent,
    ContentBlockStartEvent,
    ContentBlockDeltaEvent,
    ContentBlockStopEvent,
)
```

Methods:

- <code title="post /v1/messages">client.messages.<a href="./src/anthropic/resources/messages/messages.py">create</a>(\*\*<a href="src/anthropic/types/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/message.py">Message</a></code>
- <code>client.messages.<a href="./src/anthropic/resources/messages.py">stream</a>(\*args) -> MessageStreamManager[MessageStream] | MessageStreamManager[MessageStreamT]</code>
- <code title="post /v1/messages/count_tokens">client.messages.<a href="./src/anthropic/resources/messages/messages.py">count_tokens</a>(\*\*<a href="src/anthropic/types/message_count_tokens_params.py">params</a>) -> <a href="./src/anthropic/types/message_tokens_count.py">MessageTokensCount</a></code>

## Batches

Types:

```python
from anthropic.types.messages import (
    DeletedMessageBatch,
    MessageBatch,
    MessageBatchCanceledResult,
    MessageBatchErroredResult,
    MessageBatchExpiredResult,
    MessageBatchIndividualResponse,
    MessageBatchRequestCounts,
    MessageBatchResult,
    MessageBatchSucceededResult,
)
```

Methods:

- <code title="post /v1/messages/batches">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">create</a>(\*\*<a href="src/anthropic/types/messages/batch_create_params.py">params</a>) -> <a href="./src/anthropic/types/messages/message_batch.py">MessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">retrieve</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/message_batch.py">MessageBatch</a></code>
- <code title="get /v1/messages/batches">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">list</a>(\*\*<a href="src/anthropic/types/messages/batch_list_params.py">params</a>) -> <a href="./src/anthropic/types/messages/message_batch.py">SyncPage[MessageBatch]</a></code>
- <code title="delete /v1/messages/batches/{message_batch_id}">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">delete</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/deleted_message_batch.py">DeletedMessageBatch</a></code>
- <code title="post /v1/messages/batches/{message_batch_id}/cancel">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">cancel</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/message_batch.py">MessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}/results">client.messages.batches.<a href="./src/anthropic/resources/messages/batches.py">results</a>(message_batch_id) -> <a href="./src/anthropic/types/messages/message_batch_individual_response.py">JSONLDecoder[MessageBatchIndividualResponse]</a></code>

# Models

Types:

```python
from anthropic.types import (
    CapabilitySupport,
    ContextManagementCapability,
    EffortCapability,
    ModelCapabilities,
    ModelInfo,
    ThinkingCapability,
    ThinkingTypes,
)
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/anthropic/resources/models.py">retrieve</a>(model_id) -> <a href="./src/anthropic/types/model_info.py">ModelInfo</a></code>
- <code title="get /v1/models">client.models.<a href="./src/anthropic/resources/models.py">list</a>(\*\*<a href="src/anthropic/types/model_list_params.py">params</a>) -> <a href="./src/anthropic/types/model_info.py">SyncPage[ModelInfo]</a></code>

# Files

Types:

```python
from anthropic.types import DeletedFile, FileMetadata
```

Methods:

- <code title="get /v1/files">client.files.<a href="./src/anthropic/resources/files.py">list</a>(\*\*<a href="src/anthropic/types/file_list_params.py">params</a>) -> <a href="./src/anthropic/types/file_metadata.py">SyncPageCursor[FileMetadata]</a></code>
- <code title="delete /v1/files/{file_id}">client.files.<a href="./src/anthropic/resources/files.py">delete</a>(file_id) -> <a href="./src/anthropic/types/deleted_file.py">DeletedFile</a></code>
- <code title="get /v1/files/{file_id}/content">client.files.<a href="./src/anthropic/resources/files.py">download</a>(file_id) -> BinaryAPIResponse</code>
- <code title="get /v1/files/{file_id}">client.files.<a href="./src/anthropic/resources/files.py">retrieve_metadata</a>(file_id) -> <a href="./src/anthropic/types/file_metadata.py">FileMetadata</a></code>
- <code title="post /v1/files">client.files.<a href="./src/anthropic/resources/files.py">upload</a>(\*\*<a href="src/anthropic/types/file_upload_params.py">params</a>) -> <a href="./src/anthropic/types/file_metadata.py">FileMetadata</a></code>

# Skills

Types:

```python
from anthropic.types import DeletedSkill, Skill, SkillSource
```

Methods:

- <code title="post /v1/skills">client.skills.<a href="./src/anthropic/resources/skills/skills.py">create</a>(\*\*<a href="src/anthropic/types/skill_create_params.py">params</a>) -> <a href="./src/anthropic/types/skill.py">Skill</a></code>
- <code title="get /v1/skills/{skill_id}">client.skills.<a href="./src/anthropic/resources/skills/skills.py">retrieve</a>(skill_id) -> <a href="./src/anthropic/types/skill.py">Skill</a></code>
- <code title="get /v1/skills">client.skills.<a href="./src/anthropic/resources/skills/skills.py">list</a>(\*\*<a href="src/anthropic/types/skill_list_params.py">params</a>) -> <a href="./src/anthropic/types/skill.py">SyncPageCursor[Skill]</a></code>
- <code title="delete /v1/skills/{skill_id}">client.skills.<a href="./src/anthropic/resources/skills/skills.py">delete</a>(skill_id) -> <a href="./src/anthropic/types/deleted_skill.py">DeletedSkill</a></code>

## Versions

Types:

```python
from anthropic.types.skills import DeletedSkillVersion, SkillVersion
```

Methods:

- <code title="post /v1/skills/{skill_id}/versions">client.skills.versions.<a href="./src/anthropic/resources/skills/versions.py">create</a>(skill_id, \*\*<a href="src/anthropic/types/skills/version_create_params.py">params</a>) -> <a href="./src/anthropic/types/skills/skill_version.py">SkillVersion</a></code>
- <code title="get /v1/skills/{skill_id}/versions/{version}">client.skills.versions.<a href="./src/anthropic/resources/skills/versions.py">retrieve</a>(version, \*, skill_id) -> <a href="./src/anthropic/types/skills/skill_version.py">SkillVersion</a></code>
- <code title="get /v1/skills/{skill_id}/versions">client.skills.versions.<a href="./src/anthropic/resources/skills/versions.py">list</a>(skill_id, \*\*<a href="src/anthropic/types/skills/version_list_params.py">params</a>) -> <a href="./src/anthropic/types/skills/skill_version.py">SyncPageCursor[SkillVersion]</a></code>
- <code title="delete /v1/skills/{skill_id}/versions/{version}">client.skills.versions.<a href="./src/anthropic/resources/skills/versions.py">delete</a>(version, \*, skill_id) -> <a href="./src/anthropic/types/skills/deleted_skill_version.py">DeletedSkillVersion</a></code>

# Beta

Types:

```python
from anthropic.types import (
    AnthropicBetaParam,
    BetaAPIError,
    BetaAuthenticationError,
    BetaBillingError,
    BetaCurrency,
    BetaError,
    BetaErrorResponse,
    BetaGatewayTimeoutError,
    BetaInvalidRequestError,
    BetaMonetaryAmount,
    BetaMonetaryAmountParam,
    BetaNotFoundError,
    BetaOverloadedError,
    BetaPermissionError,
    BetaRateLimitError,
)
```

## Models

Types:

```python
from anthropic.types.beta import (
    BetaCapabilitySupport,
    BetaCompactionCapability,
    BetaContextManagementCapability,
    BetaEffortCapability,
    BetaModelCapabilities,
    BetaModelInfo,
    BetaThinkingCapability,
    BetaThinkingTypes,
)
```

Methods:

- <code title="get /v1/models/{model_id}?beta=true">client.beta.models.<a href="./src/anthropic/resources/beta/models.py">retrieve</a>(model_id) -> <a href="./src/anthropic/types/beta/beta_model_info.py">BetaModelInfo</a></code>
- <code title="get /v1/models?beta=true">client.beta.models.<a href="./src/anthropic/resources/beta/models.py">list</a>(\*\*<a href="src/anthropic/types/beta/model_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_model_info.py">SyncPage[BetaModelInfo]</a></code>

## Messages

Types:

```python
from anthropic.types.beta import (
    BetaAdvisorMessageIterationUsage,
    BetaAdvisorRedactedResultBlock,
    BetaAdvisorRedactedResultBlockParam,
    BetaAdvisorResultBlock,
    BetaAdvisorResultBlockParam,
    BetaAdvisorTool20260301,
    BetaAdvisorTool20260301Param,
    BetaAdvisorToolResultBlock,
    BetaAdvisorToolResultBlockParam,
    BetaAdvisorToolResultError,
    BetaAdvisorToolResultErrorParam,
    BetaAllThinkingTurnsParam,
    BetaBase64ImageSourceParam,
    BetaBase64PDFSource,
    BetaBase64PDFSourceParam,
    BetaBashCodeExecutionOutputBlock,
    BetaBashCodeExecutionOutputBlockParam,
    BetaBashCodeExecutionResultBlock,
    BetaBashCodeExecutionResultBlockParam,
    BetaBashCodeExecutionToolResultBlock,
    BetaBashCodeExecutionToolResultBlockParam,
    BetaBashCodeExecutionToolResultError,
    BetaBashCodeExecutionToolResultErrorParam,
    BetaBrowserCloseTabConfig,
    BetaBrowserCloseTabConfigParam,
    BetaBrowserDoubleClickConfig,
    BetaBrowserDoubleClickConfigParam,
    BetaBrowserFileUploadConfig,
    BetaBrowserFileUploadConfigParam,
    BetaBrowserFindConfig,
    BetaBrowserFindConfigParam,
    BetaBrowserFormInputConfig,
    BetaBrowserFormInputConfigParam,
    BetaBrowserGetPageTextConfig,
    BetaBrowserGetPageTextConfigParam,
    BetaBrowserHoldKeyConfig,
    BetaBrowserHoldKeyConfigParam,
    BetaBrowserHoverConfig,
    BetaBrowserHoverConfigParam,
    BetaBrowserJavascriptExecConfig,
    BetaBrowserJavascriptExecConfigParam,
    BetaBrowserKeyConfig,
    BetaBrowserKeyConfigParam,
    BetaBrowserLeftClickConfig,
    BetaBrowserLeftClickConfigParam,
    BetaBrowserLeftClickDragConfig,
    BetaBrowserLeftClickDragConfigParam,
    BetaBrowserLeftMouseDownConfig,
    BetaBrowserLeftMouseDownConfigParam,
    BetaBrowserLeftMouseUpConfig,
    BetaBrowserLeftMouseUpConfigParam,
    BetaBrowserListTabsConfig,
    BetaBrowserListTabsConfigParam,
    BetaBrowserMiddleClickConfig,
    BetaBrowserMiddleClickConfigParam,
    BetaBrowserMouseMoveConfig,
    BetaBrowserMouseMoveConfigParam,
    BetaBrowserNavigateConfig,
    BetaBrowserNavigateConfigParam,
    BetaBrowserNewTabConfig,
    BetaBrowserNewTabConfigParam,
    BetaBrowserReadConsoleConfig,
    BetaBrowserReadConsoleConfigParam,
    BetaBrowserReadNetworkConfig,
    BetaBrowserReadNetworkConfigParam,
    BetaBrowserReadPageConfig,
    BetaBrowserReadPageConfigParam,
    BetaBrowserRightClickConfig,
    BetaBrowserRightClickConfigParam,
    BetaBrowserScreenshotConfig,
    BetaBrowserScreenshotConfigParam,
    BetaBrowserScrollConfig,
    BetaBrowserScrollConfigParam,
    BetaBrowserScrollToConfig,
    BetaBrowserScrollToConfigParam,
    BetaBrowserStateBlockParam,
    BetaBrowserStateChangeParam,
    BetaBrowserStateChangeDownloadCompletedParam,
    BetaBrowserStateChangeDownloadFailedParam,
    BetaBrowserStateChangeDownloadStartedParam,
    BetaBrowserStateChangeTabOpenedParam,
    BetaBrowserStateTabEntryParam,
    BetaBrowserSwitchTabConfig,
    BetaBrowserSwitchTabConfigParam,
    BetaBrowserToolset20260801,
    BetaBrowserToolset20260801Param,
    BetaBrowserToolsetConfigs,
    BetaBrowserToolsetConfigsParam,
    BetaBrowserTripleClickConfig,
    BetaBrowserTripleClickConfigParam,
    BetaBrowserTypeConfig,
    BetaBrowserTypeConfigParam,
    BetaBrowserWaitConfig,
    BetaBrowserWaitConfigParam,
    BetaBrowserZoomConfig,
    BetaBrowserZoomConfigParam,
    BetaCacheControlEphemeral,
    BetaCacheControlEphemeralParam,
    BetaCacheCreation,
    BetaCacheMissMessagesChanged,
    BetaCacheMissModelChanged,
    BetaCacheMissPreviousMessageNotFound,
    BetaCacheMissReason,
    BetaCacheMissSystemChanged,
    BetaCacheMissToolsChanged,
    BetaCacheMissUnavailable,
    BetaCitationCharLocation,
    BetaCitationCharLocationParam,
    BetaCitationConfig,
    BetaCitationContentBlockLocation,
    BetaCitationContentBlockLocationParam,
    BetaCitationPageLocation,
    BetaCitationPageLocationParam,
    BetaCitationSearchResultLocation,
    BetaCitationSearchResultLocationParam,
    BetaCitationWebSearchResultLocationParam,
    BetaCitationsConfigParam,
    BetaCitationsConfigParamParam,
    BetaCitationsDelta,
    BetaCitationsWebSearchResultLocation,
    BetaClearThinking20251015EditParam,
    BetaClearThinking20251015EditResponse,
    BetaClearToolUses20250919EditParam,
    BetaClearToolUses20250919EditResponse,
    BetaCodeExecutionOutputBlock,
    BetaCodeExecutionOutputBlockParam,
    BetaCodeExecutionResultBlock,
    BetaCodeExecutionResultBlockParam,
    BetaCodeExecutionTool20250522,
    BetaCodeExecutionTool20250522Param,
    BetaCodeExecutionTool20250825,
    BetaCodeExecutionTool20250825Param,
    BetaCodeExecutionTool20260120,
    BetaCodeExecutionTool20260120Param,
    BetaCodeExecutionTool20260521,
    BetaCodeExecutionTool20260521Param,
    BetaCodeExecutionToolResultBlock,
    BetaCodeExecutionToolResultBlockContent,
    BetaCodeExecutionToolResultBlockParam,
    BetaCodeExecutionToolResultBlockParamContentParam,
    BetaCodeExecutionToolResultError,
    BetaCodeExecutionToolResultErrorCode,
    BetaCodeExecutionToolResultErrorParam,
    BetaCompact20260112EditParam,
    BetaCompactionBlock,
    BetaCompactionBlockParam,
    BetaCompactionConfigParam,
    BetaCompactionContentBlockDelta,
    BetaCompactionIterationUsage,
    BetaComputerCursorPositionConfig,
    BetaComputerCursorPositionConfigParam,
    BetaComputerDoubleClickConfig,
    BetaComputerDoubleClickConfigParam,
    BetaComputerHoldKeyConfig,
    BetaComputerHoldKeyConfigParam,
    BetaComputerKeyConfig,
    BetaComputerKeyConfigParam,
    BetaComputerLeftClickConfig,
    BetaComputerLeftClickConfigParam,
    BetaComputerLeftClickDragConfig,
    BetaComputerLeftClickDragConfigParam,
    BetaComputerLeftMouseDownConfig,
    BetaComputerLeftMouseDownConfigParam,
    BetaComputerLeftMouseUpConfig,
    BetaComputerLeftMouseUpConfigParam,
    BetaComputerMiddleClickConfig,
    BetaComputerMiddleClickConfigParam,
    BetaComputerMouseMoveConfig,
    BetaComputerMouseMoveConfigParam,
    BetaComputerRightClickConfig,
    BetaComputerRightClickConfigParam,
    BetaComputerScreenshotConfig,
    BetaComputerScreenshotConfigParam,
    BetaComputerScrollConfig,
    BetaComputerScrollConfigParam,
    BetaComputerToolset20260801,
    BetaComputerToolset20260801Param,
    BetaComputerToolsetConfigs,
    BetaComputerToolsetConfigsParam,
    BetaComputerTripleClickConfig,
    BetaComputerTripleClickConfigParam,
    BetaComputerTypeConfig,
    BetaComputerTypeConfigParam,
    BetaComputerWaitConfig,
    BetaComputerWaitConfigParam,
    BetaComputerZoomConfig,
    BetaComputerZoomConfigParam,
    BetaContainer,
    BetaContainerParams,
    BetaContainerSkill,
    BetaContainerUploadBlock,
    BetaContainerUploadBlockParam,
    BetaContentBlock,
    BetaContentBlockParam,
    BetaContentBlockSourceParam,
    BetaContentBlockSourceContentParam,
    BetaContextManagementConfigParam,
    BetaContextManagementResponse,
    BetaCountTokensContextManagementResponse,
    BetaDiagnostics,
    BetaDiagnosticsParam,
    BetaDirectCaller,
    BetaDirectCallerParam,
    BetaDocumentBlock,
    BetaEncryptedCodeExecutionResultBlock,
    BetaEncryptedCodeExecutionResultBlockParam,
    BetaFallbackBlock,
    BetaFallbackBlockParam,
    BetaFallbackCreditNotApplied,
    BetaFallbackCreditRedeemed,
    BetaFallbackCreditTokenParam,
    BetaFallbackCreditUsage,
    BetaFallbackInfo,
    BetaFallbackInfoParam,
    BetaFallbackMessageIterationUsage,
    BetaFallbackParam,
    BetaFallbackRefusalTrigger,
    BetaFallbacksParam,
    BetaFileDocumentSourceParam,
    BetaFileImageSourceParam,
    BetaImageBlockParam,
    BetaImageTransformationsParam,
    BetaInputJSONDelta,
    BetaInputTokensClearAtLeastParam,
    BetaInputTokensTriggerParam,
    BetaInputTransformation,
    BetaIterationsUsage,
    BetaJSONOutputFormatParam,
    BetaMCPTool,
    BetaMCPToolConfig,
    BetaMCPToolConfigParam,
    BetaMCPToolDefaultConfig,
    BetaMCPToolDefaultConfigParam,
    BetaMCPToolListingBlock,
    BetaMCPToolListingBlockParam,
    BetaMCPToolParam,
    BetaMCPToolParamParam,
    BetaMCPToolResultBlock,
    BetaMCPToolUseBlock,
    BetaMCPToolUseBlockParam,
    BetaMCPToolset,
    BetaMCPToolsetParam,
    BetaMemoryTool20250818,
    BetaMemoryTool20250818Param,
    BetaMemoryTool20250818Command,
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
    BetaMemoryTool20250818ViewCommand,
    BetaMessage,
    BetaMessageDeltaUsage,
    BetaMessageIterationUsage,
    BetaMessageParam,
    BetaMessageTokensCount,
    BetaMetadataParam,
    BetaOutputConfigParam,
    BetaOutputTokensDetails,
    BetaPlainTextSource,
    BetaPlainTextSourceParam,
    BetaRawContentBlockDelta,
    BetaRawContentBlockDeltaEvent,
    BetaRawContentBlockStartEvent,
    BetaRawContentBlockStopEvent,
    BetaRawMessageDeltaEvent,
    BetaRawMessageStartEvent,
    BetaRawMessageStopEvent,
    BetaRawMessageStreamEvent,
    BetaRedactedThinkingBlock,
    BetaRedactedThinkingBlockParam,
    BetaRefusalStopDetails,
    BetaRequestDocumentBlockParam,
    BetaRequestMCPServerToolConfigurationParam,
    BetaRequestMCPServerURLDefinitionParam,
    BetaRequestMCPToolResultBlockParam,
    BetaRequestToolAdditionBlockParam,
    BetaRequestToolRemovalBlockParam,
    BetaResponseTool,
    BetaResponseToolAdditionBlock,
    BetaResponseToolChangeMCPToolReference,
    BetaResponseToolChangeMCPToolsetReference,
    BetaResponseToolChangeToolReference,
    BetaResponseToolInputSchema,
    BetaResponseToolRemovalBlock,
    BetaResponseToolUnion,
    BetaSearchResultBlockParam,
    BetaServerToolCaller,
    BetaServerToolCallerParam,
    BetaServerToolCaller20260120,
    BetaServerToolCaller20260120Param,
    BetaServerToolUsage,
    BetaServerToolUseBlock,
    BetaServerToolUseBlockParam,
    BetaSignatureDelta,
    BetaSkillParams,
    BetaStopReason,
    BetaSystemMessageOutputConfigParam,
    BetaTextBlock,
    BetaTextBlockParam,
    BetaTextCitation,
    BetaTextCitationParam,
    BetaTextDelta,
    BetaTextEditorCodeExecutionCreateResultBlock,
    BetaTextEditorCodeExecutionCreateResultBlockParam,
    BetaTextEditorCodeExecutionStrReplaceResultBlock,
    BetaTextEditorCodeExecutionStrReplaceResultBlockParam,
    BetaTextEditorCodeExecutionToolResultBlock,
    BetaTextEditorCodeExecutionToolResultBlockParam,
    BetaTextEditorCodeExecutionToolResultError,
    BetaTextEditorCodeExecutionToolResultErrorParam,
    BetaTextEditorCodeExecutionViewResultBlock,
    BetaTextEditorCodeExecutionViewResultBlockParam,
    BetaThinkingBlock,
    BetaThinkingBlockBindingParam,
    BetaThinkingBlockParam,
    BetaThinkingConfigAdaptiveParam,
    BetaThinkingConfigBetweenToolsParam,
    BetaThinkingConfigDisabledParam,
    BetaThinkingConfigEnabledParam,
    BetaThinkingConfigParam,
    BetaThinkingDelta,
    BetaThinkingDroppedInputTransformation,
    BetaThinkingMismatchAllowedInputTransformation,
    BetaThinkingPrefixMismatchBehavior,
    BetaThinkingTurnsParam,
    BetaTokenTaskBudgetParam,
    BetaToolParam,
    BetaToolBash20241022,
    BetaToolBash20241022Param,
    BetaToolBash20250124,
    BetaToolBash20250124Param,
    BetaToolChangeMCPToolReferenceParam,
    BetaToolChangeMCPToolsetReferenceParam,
    BetaToolChangeToolDefinition,
    BetaToolChangeToolDefinitionParam,
    BetaToolChangeToolReferenceParam,
    BetaToolChoiceParam,
    BetaToolChoiceAnyParam,
    BetaToolChoiceAutoParam,
    BetaToolChoiceNoneParam,
    BetaToolChoiceToolParam,
    BetaToolComputerUse20241022,
    BetaToolComputerUse20241022Param,
    BetaToolComputerUse20250124,
    BetaToolComputerUse20250124Param,
    BetaToolComputerUse20251124,
    BetaToolComputerUse20251124Param,
    BetaToolReferenceBlock,
    BetaToolReferenceBlockParam,
    BetaToolResultBlockParam,
    BetaToolSearchToolBm25_20251119,
    BetaToolSearchToolBm25_20251119Param,
    BetaToolSearchToolRegex20251119,
    BetaToolSearchToolRegex20251119Param,
    BetaToolSearchToolResultBlock,
    BetaToolSearchToolResultBlockParam,
    BetaToolSearchToolResultError,
    BetaToolSearchToolResultErrorParam,
    BetaToolSearchToolSearchResultBlock,
    BetaToolSearchToolSearchResultBlockParam,
    BetaToolTextEditor20241022,
    BetaToolTextEditor20241022Param,
    BetaToolTextEditor20250124,
    BetaToolTextEditor20250124Param,
    BetaToolTextEditor20250429,
    BetaToolTextEditor20250429Param,
    BetaToolTextEditor20250728,
    BetaToolTextEditor20250728Param,
    BetaToolUnionParam,
    BetaToolUseBlock,
    BetaToolUseBlockParam,
    BetaToolUsesKeepParam,
    BetaToolUsesTriggerParam,
    BetaURLImageSourceParam,
    BetaURLPDFSourceParam,
    BetaUsage,
    BetaUserLocation,
    BetaUserLocationParam,
    BetaWebFetchBlock,
    BetaWebFetchBlockParam,
    BetaWebFetchTool20250910,
    BetaWebFetchTool20250910Param,
    BetaWebFetchTool20260209,
    BetaWebFetchTool20260209Param,
    BetaWebFetchTool20260309,
    BetaWebFetchTool20260309Param,
    BetaWebFetchTool20260318,
    BetaWebFetchTool20260318Param,
    BetaWebFetchToolResultBlock,
    BetaWebFetchToolResultBlockParam,
    BetaWebFetchToolResultErrorBlock,
    BetaWebFetchToolResultErrorBlockParam,
    BetaWebFetchToolResultErrorCode,
    BetaWebFetchURLSourceAll,
    BetaWebFetchURLSourceAllParam,
    BetaWebFetchURLSourceExcept,
    BetaWebFetchURLSourceExceptParam,
    BetaWebFetchURLSourceNone,
    BetaWebFetchURLSourceNoneParam,
    BetaWebFetchURLSourceOnly,
    BetaWebFetchURLSourceOnlyParam,
    BetaWebFetchURLSourceToolReference,
    BetaWebFetchURLSourceToolReferenceParam,
    BetaWebFetchURLSources,
    BetaWebFetchURLSourcesParam,
    BetaWebSearchResultBlock,
    BetaWebSearchResultBlockParam,
    BetaWebSearchTool20250305,
    BetaWebSearchTool20250305Param,
    BetaWebSearchTool20260209,
    BetaWebSearchTool20260209Param,
    BetaWebSearchTool20260318,
    BetaWebSearchTool20260318Param,
    BetaWebSearchToolRequestErrorParam,
    BetaWebSearchToolResultBlock,
    BetaWebSearchToolResultBlockContent,
    BetaWebSearchToolResultBlockParam,
    BetaWebSearchToolResultBlockParamContentParam,
    BetaWebSearchToolResultError,
    BetaWebSearchToolResultErrorCode,
)
```

Methods:

- <code title="post /v1/messages?beta=true">client.beta.messages.<a href="./src/anthropic/resources/beta/messages/messages.py">create</a>(\*\*<a href="src/anthropic/types/beta/message_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_message.py">BetaMessage</a></code>
- <code title="post /v1/messages/count_tokens?beta=true">client.beta.messages.<a href="./src/anthropic/resources/beta/messages/messages.py">count_tokens</a>(\*\*<a href="src/anthropic/types/beta/message_count_tokens_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_message_tokens_count.py">BetaMessageTokensCount</a></code>

### Batches

Types:

```python
from anthropic.types.beta.messages import (
    BetaDeletedMessageBatch,
    BetaMessageBatch,
    BetaMessageBatchCanceledResult,
    BetaMessageBatchErroredResult,
    BetaMessageBatchExpiredResult,
    BetaMessageBatchIndividualResponse,
    BetaMessageBatchRequestCounts,
    BetaMessageBatchResult,
    BetaMessageBatchSucceededResult,
)
```

Methods:

- <code title="post /v1/messages/batches?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">create</a>(\*\*<a href="src/anthropic/types/beta/messages/batch_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">retrieve</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">list</a>(\*\*<a href="src/anthropic/types/beta/messages/batch_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">SyncPage[BetaMessageBatch]</a></code>
- <code title="delete /v1/messages/batches/{message_batch_id}?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">delete</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_deleted_message_batch.py">BetaDeletedMessageBatch</a></code>
- <code title="post /v1/messages/batches/{message_batch_id}/cancel?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">cancel</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch.py">BetaMessageBatch</a></code>
- <code title="get /v1/messages/batches/{message_batch_id}/results?beta=true">client.beta.messages.batches.<a href="./src/anthropic/resources/beta/messages/batches.py">results</a>(message_batch_id) -> <a href="./src/anthropic/types/beta/messages/beta_message_batch_individual_response.py">JSONLDecoder[BetaMessageBatchIndividualResponse]</a></code>

## Agents

Types:

```python
from anthropic.types.beta import (
    BetaManagedAgentsAdvisor,
    BetaManagedAgentsAgent,
    BetaManagedAgentsAgentReference,
    BetaManagedAgentsAgentToolConfig,
    BetaManagedAgentsAgentToolConfigParams,
    BetaManagedAgentsAgentToolsetDefaultConfig,
    BetaManagedAgentsAgentToolsetDefaultConfigParams,
    BetaManagedAgentsAgentToolset20260401,
    BetaManagedAgentsAgentToolset20260401BashInput,
    BetaManagedAgentsAgentToolset20260401EditInput,
    BetaManagedAgentsAgentToolset20260401GlobInput,
    BetaManagedAgentsAgentToolset20260401GrepInput,
    BetaManagedAgentsAgentToolset20260401Params,
    BetaManagedAgentsAgentToolset20260401ReadInput,
    BetaManagedAgentsAgentToolset20260401WriteInput,
    BetaManagedAgentsAlwaysAllowPolicy,
    BetaManagedAgentsAlwaysAllowPolicyParam,
    BetaManagedAgentsAlwaysAskPolicy,
    BetaManagedAgentsAlwaysAskPolicyParam,
    BetaManagedAgentsAnthropicSkill,
    BetaManagedAgentsAnthropicSkillParams,
    BetaManagedAgentsAutoPolicy,
    BetaManagedAgentsAutoPolicyParam,
    BetaManagedAgentsBashToolConfig,
    BetaManagedAgentsBashToolConfigParams,
    BetaManagedAgentsCustomSkill,
    BetaManagedAgentsCustomSkillParams,
    BetaManagedAgentsCustomTool,
    BetaManagedAgentsCustomToolInputSchema,
    BetaManagedAgentsCustomToolInputSchemaParam,
    BetaManagedAgentsCustomToolParams,
    BetaManagedAgentsEditToolConfig,
    BetaManagedAgentsEditToolConfigParams,
    BetaManagedAgentsEffortHigh,
    BetaManagedAgentsEffortHighParam,
    BetaManagedAgentsEffortLow,
    BetaManagedAgentsEffortLowParam,
    BetaManagedAgentsEffortMax,
    BetaManagedAgentsEffortMaxParam,
    BetaManagedAgentsEffortMedium,
    BetaManagedAgentsEffortMediumParam,
    BetaManagedAgentsEffortXhigh,
    BetaManagedAgentsEffortXhighParam,
    BetaManagedAgentsGlobToolConfig,
    BetaManagedAgentsGlobToolConfigParams,
    BetaManagedAgentsGrepToolConfig,
    BetaManagedAgentsGrepToolConfigParams,
    BetaManagedAgentsMCPServerURLDefinition,
    BetaManagedAgentsMCPToolConfig,
    BetaManagedAgentsMCPToolConfigParams,
    BetaManagedAgentsMCPToolset,
    BetaManagedAgentsMCPToolsetDefaultConfig,
    BetaManagedAgentsMCPToolsetDefaultConfigParams,
    BetaManagedAgentsMCPToolsetParams,
    BetaManagedAgentsModel,
    BetaManagedAgentsModelParam,
    BetaManagedAgentsModelConfig,
    BetaManagedAgentsModelConfigParams,
    BetaManagedAgentsMultiagentSelfParams,
    BetaManagedAgentsReadToolConfig,
    BetaManagedAgentsReadToolConfigParams,
    BetaManagedAgentsSessionThreadAgent,
    BetaManagedAgentsSkillParams,
    BetaManagedAgentsURLMCPServerParams,
    BetaManagedAgentsUserLocation,
    BetaManagedAgentsUserLocationParam,
    BetaManagedAgentsWebFetchToolConfig,
    BetaManagedAgentsWebFetchToolConfigParams,
    BetaManagedAgentsWebSearchToolConfig,
    BetaManagedAgentsWebSearchToolConfigParams,
    BetaManagedAgentsWriteToolConfig,
    BetaManagedAgentsWriteToolConfigParams,
)
```

Methods:

- <code title="post /v1/agents?beta=true">client.beta.agents.<a href="./src/anthropic/resources/beta/agents/agents.py">create</a>(\*\*<a href="src/anthropic/types/beta/agent_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_agent.py">BetaManagedAgentsAgent</a></code>
- <code title="get /v1/agents/{agent_id}?beta=true">client.beta.agents.<a href="./src/anthropic/resources/beta/agents/agents.py">retrieve</a>(agent_id, \*\*<a href="src/anthropic/types/beta/agent_retrieve_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_agent.py">BetaManagedAgentsAgent</a></code>
- <code title="post /v1/agents/{agent_id}?beta=true">client.beta.agents.<a href="./src/anthropic/resources/beta/agents/agents.py">update</a>(agent_id, \*\*<a href="src/anthropic/types/beta/agent_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_agent.py">BetaManagedAgentsAgent</a></code>
- <code title="get /v1/agents?beta=true">client.beta.agents.<a href="./src/anthropic/resources/beta/agents/agents.py">list</a>(\*\*<a href="src/anthropic/types/beta/agent_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_agent.py">SyncPageCursor[BetaManagedAgentsAgent]</a></code>
- <code title="post /v1/agents/{agent_id}/archive?beta=true">client.beta.agents.<a href="./src/anthropic/resources/beta/agents/agents.py">archive</a>(agent_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_agent.py">BetaManagedAgentsAgent</a></code>

### Versions

Methods:

- <code title="get /v1/agents/{agent_id}/versions?beta=true">client.beta.agents.versions.<a href="./src/anthropic/resources/beta/agents/versions.py">list</a>(agent_id, \*\*<a href="src/anthropic/types/beta/agents/version_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_agent.py">SyncPageCursor[BetaManagedAgentsAgent]</a></code>

## Environments

Types:

```python
from anthropic.types.beta import (
    BetaCloudConfig,
    BetaCloudConfigParams,
    BetaEnvironment,
    BetaEnvironmentDeleteResponse,
    BetaLimitedNetwork,
    BetaLimitedNetworkParams,
    BetaPackages,
    BetaPackagesParams,
    BetaSelfHostedConfig,
    BetaSelfHostedConfigParams,
    BetaUnrestrictedNetwork,
    BetaUnrestrictedNetworkParam,
)
```

Methods:

- <code title="post /v1/environments?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments/environments.py">create</a>(\*\*<a href="src/anthropic/types/beta/environment_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>
- <code title="get /v1/environments/{environment_id}?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments/environments.py">retrieve</a>(environment_id) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>
- <code title="post /v1/environments/{environment_id}?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments/environments.py">update</a>(environment_id, \*\*<a href="src/anthropic/types/beta/environment_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>
- <code title="get /v1/environments?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments/environments.py">list</a>(\*\*<a href="src/anthropic/types/beta/environment_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_environment.py">SyncPageCursor[BetaEnvironment]</a></code>
- <code title="delete /v1/environments/{environment_id}?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments/environments.py">delete</a>(environment_id) -> <a href="./src/anthropic/types/beta/beta_environment_delete_response.py">BetaEnvironmentDeleteResponse</a></code>
- <code title="post /v1/environments/{environment_id}/archive?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments/environments.py">archive</a>(environment_id) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>

### Work

Types:

```python
from anthropic.types.beta.environments import (
    BetaSelfHostedWork,
    BetaSelfHostedWorkHeartbeatResponse,
    BetaSelfHostedWorkListResponse,
    BetaSelfHostedWorkQueueStats,
    BetaSessionWorkData,
)
```

Methods:

- <code title="get /v1/environments/{environment_id}/work/{work_id}?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">retrieve</a>(work_id, \*, environment_id) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work.py">BetaSelfHostedWork</a></code>
- <code title="post /v1/environments/{environment_id}/work/{work_id}?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">update</a>(work_id, \*, environment_id, \*\*<a href="src/anthropic/types/beta/environments/work_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work.py">BetaSelfHostedWork</a></code>
- <code title="get /v1/environments/{environment_id}/work?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">list</a>(environment_id, \*\*<a href="src/anthropic/types/beta/environments/work_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work.py">SyncPageCursor[BetaSelfHostedWork]</a></code>
- <code title="post /v1/environments/{environment_id}/work/{work_id}/ack?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">ack</a>(work_id, \*, environment_id) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work.py">BetaSelfHostedWork</a></code>
- <code title="post /v1/environments/{environment_id}/work/{work_id}/heartbeat?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">heartbeat</a>(work_id, \*, environment_id, \*\*<a href="src/anthropic/types/beta/environments/work_heartbeat_params.py">params</a>) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work_heartbeat_response.py">BetaSelfHostedWorkHeartbeatResponse</a></code>
- <code title="get /v1/environments/{environment_id}/work/poll?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">poll</a>(environment_id, \*\*<a href="src/anthropic/types/beta/environments/work_poll_params.py">params</a>) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work.py">Optional[BetaSelfHostedWork]</a></code>
- <code title="get /v1/environments/{environment_id}/work/stats?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">stats</a>(environment_id) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work_queue_stats.py">BetaSelfHostedWorkQueueStats</a></code>
- <code title="post /v1/environments/{environment_id}/work/{work_id}/stop?beta=true">client.beta.environments.work.<a href="./src/anthropic/resources/beta/environments/work.py">stop</a>(work_id, \*, environment_id, \*\*<a href="src/anthropic/types/beta/environments/work_stop_params.py">params</a>) -> <a href="./src/anthropic/types/beta/environments/beta_self_hosted_work.py">BetaSelfHostedWork</a></code>

## Sessions

Types:

```python
from anthropic.types.beta import (
    BetaManagedAgentsAdvisorParams,
    BetaManagedAgentsAgentMessagePreview,
    BetaManagedAgentsAgentParams,
    BetaManagedAgentsAgentThinkingPreview,
    BetaManagedAgentsAgentWithOverridesParams,
    BetaManagedAgentsBranchCheckout,
    BetaManagedAgentsBranchCheckoutParam,
    BetaManagedAgentsBudgetLimit,
    BetaManagedAgentsBudgetLimitParam,
    BetaManagedAgentsCacheCreationUsage,
    BetaManagedAgentsCommitCheckout,
    BetaManagedAgentsCommitCheckoutParam,
    BetaManagedAgentsDeletedSession,
    BetaManagedAgentsDeltaContent,
    BetaManagedAgentsDeltaEvent,
    BetaManagedAgentsDeltaType,
    BetaManagedAgentsFileResourceParams,
    BetaManagedAgentsGitHubRepositoryResourceParams,
    BetaManagedAgentsMemoryStoreResourceParam,
    BetaManagedAgentsMultiagent,
    BetaManagedAgentsMultiagentParams,
    BetaManagedAgentsMultiagentRosterEntryParams,
    BetaManagedAgentsOutcomeEvaluationResource,
    BetaManagedAgentsServerToolUsage,
    BetaManagedAgentsSession,
    BetaManagedAgentsSessionAgent,
    BetaManagedAgentsSessionAgentUpdateParam,
    BetaManagedAgentsSessionMultiagentCoordinator,
    BetaManagedAgentsSessionStats,
    BetaManagedAgentsSessionUpdatedEvent,
    BetaManagedAgentsSessionUsage,
    BetaManagedAgentsSessionUsageEvent,
    BetaManagedAgentsStartEvent,
    BetaManagedAgentsStartEventPreview,
    BetaManagedAgentsSystemContentBlock,
    BetaManagedAgentsSystemContentBlockParam,
    BetaManagedAgentsSystemMessageEvent,
    BetaManagedAgentsUserToolResultEvent,
)
```

Methods:

- <code title="post /v1/sessions?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">create</a>(\*\*<a href="src/anthropic/types/beta/session_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>
- <code title="get /v1/sessions/{session_id}?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">retrieve</a>(session_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>
- <code title="post /v1/sessions/{session_id}?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">update</a>(session_id, \*\*<a href="src/anthropic/types/beta/session_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>
- <code title="get /v1/sessions?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">list</a>(\*\*<a href="src/anthropic/types/beta/session_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">SyncBidirectionalPageCursor[BetaManagedAgentsSession]</a></code>
- <code title="delete /v1/sessions/{session_id}?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">delete</a>(session_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deleted_session.py">BetaManagedAgentsDeletedSession</a></code>
- <code title="post /v1/sessions/{session_id}/archive?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">archive</a>(session_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>

### Events

Types:

```python
from anthropic.types.beta.sessions import (
    BetaManagedAgentsAgentAutoEvaluatedPermission,
    BetaManagedAgentsAgentAutoEvaluatedPermissionAllow,
    BetaManagedAgentsAgentAutoEvaluatedPermissionAsk,
    BetaManagedAgentsAgentAutoEvaluatedPermissionDeny,
    BetaManagedAgentsAgentCustomToolUseEvent,
    BetaManagedAgentsAgentEvaluatedPermission,
    BetaManagedAgentsAgentMCPToolResultEvent,
    BetaManagedAgentsAgentMCPToolUseEvent,
    BetaManagedAgentsAgentMessageEvent,
    BetaManagedAgentsAgentThinkingEvent,
    BetaManagedAgentsAgentThreadContextCompactedEvent,
    BetaManagedAgentsAgentThreadMessageReceivedEvent,
    BetaManagedAgentsAgentThreadMessageSentEvent,
    BetaManagedAgentsAgentToolEvaluation,
    BetaManagedAgentsAgentToolEvaluationAlwaysAllow,
    BetaManagedAgentsAgentToolEvaluationAlwaysAsk,
    BetaManagedAgentsAgentToolEvaluationAuto,
    BetaManagedAgentsAgentToolResultEvent,
    BetaManagedAgentsAgentToolUseEvent,
    BetaManagedAgentsBase64DocumentSource,
    BetaManagedAgentsBase64DocumentSourceParam,
    BetaManagedAgentsBase64ImageSource,
    BetaManagedAgentsBase64ImageSourceParam,
    BetaManagedAgentsBillingError,
    BetaManagedAgentsCredentialHostUnreachableError,
    BetaManagedAgentsDocumentBlock,
    BetaManagedAgentsDocumentBlockParam,
    BetaManagedAgentsEventParams,
    BetaManagedAgentsFileDocumentSource,
    BetaManagedAgentsFileDocumentSourceParam,
    BetaManagedAgentsFileImageSource,
    BetaManagedAgentsFileImageSourceParam,
    BetaManagedAgentsFileRubric,
    BetaManagedAgentsFileRubricParams,
    BetaManagedAgentsImageBlock,
    BetaManagedAgentsImageBlockParam,
    BetaManagedAgentsMCPAuthenticationFailedError,
    BetaManagedAgentsMCPConnectionFailedError,
    BetaManagedAgentsModelOverloadedError,
    BetaManagedAgentsModelRateLimitedError,
    BetaManagedAgentsModelRequestFailedError,
    BetaManagedAgentsPlainTextDocumentSource,
    BetaManagedAgentsPlainTextDocumentSourceParam,
    BetaManagedAgentsRedactedBlock,
    BetaManagedAgentsRedactedBlockParam,
    BetaManagedAgentsRetryStatusExhausted,
    BetaManagedAgentsRetryStatusRetrying,
    BetaManagedAgentsRetryStatusTerminal,
    BetaManagedAgentsSearchResultBlock,
    BetaManagedAgentsSearchResultBlockParam,
    BetaManagedAgentsSearchResultCitations,
    BetaManagedAgentsSearchResultCitationsParam,
    BetaManagedAgentsSearchResultContent,
    BetaManagedAgentsSearchResultContentParam,
    BetaManagedAgentsSendSessionEvents,
    BetaManagedAgentsSessionBudgetReached,
    BetaManagedAgentsSessionDeletedEvent,
    BetaManagedAgentsSessionEndTurn,
    BetaManagedAgentsSessionErrorEvent,
    BetaManagedAgentsSessionEvent,
    BetaManagedAgentsSessionEventType,
    BetaManagedAgentsSessionRequiresAction,
    BetaManagedAgentsSessionRetriesExhausted,
    BetaManagedAgentsSessionStatusIdleEvent,
    BetaManagedAgentsSessionStatusRescheduledEvent,
    BetaManagedAgentsSessionStatusRunningEvent,
    BetaManagedAgentsSessionStatusTerminatedEvent,
    BetaManagedAgentsSessionThreadCreatedEvent,
    BetaManagedAgentsSessionThreadStatusIdleEvent,
    BetaManagedAgentsSessionThreadStatusRescheduledEvent,
    BetaManagedAgentsSessionThreadStatusRunningEvent,
    BetaManagedAgentsSessionThreadStatusTerminatedEvent,
    BetaManagedAgentsSessionUsageSnapshot,
    BetaManagedAgentsSpanModelRequestEndEvent,
    BetaManagedAgentsSpanModelRequestStartEvent,
    BetaManagedAgentsSpanModelUsage,
    BetaManagedAgentsSpanOutcomeEvaluationEndEvent,
    BetaManagedAgentsSpanOutcomeEvaluationOngoingEvent,
    BetaManagedAgentsSpanOutcomeEvaluationStartEvent,
    BetaManagedAgentsStreamSessionEvents,
    BetaManagedAgentsSystemMessageEventParams,
    BetaManagedAgentsTextBlock,
    BetaManagedAgentsTextBlockParam,
    BetaManagedAgentsTextRubric,
    BetaManagedAgentsTextRubricParams,
    BetaManagedAgentsUnknownError,
    BetaManagedAgentsURLDocumentSource,
    BetaManagedAgentsURLDocumentSourceParam,
    BetaManagedAgentsURLImageSource,
    BetaManagedAgentsURLImageSourceParam,
    BetaManagedAgentsUserCustomToolResultEvent,
    BetaManagedAgentsUserCustomToolResultEventParams,
    BetaManagedAgentsUserDefineOutcomeEvent,
    BetaManagedAgentsUserDefineOutcomeEventParams,
    BetaManagedAgentsUserInterruptEvent,
    BetaManagedAgentsUserInterruptEventParams,
    BetaManagedAgentsUserMessageEvent,
    BetaManagedAgentsUserMessageEventParams,
    BetaManagedAgentsUserToolConfirmationEvent,
    BetaManagedAgentsUserToolConfirmationEventParams,
    BetaManagedAgentsUserToolResultEventParams,
)
```

Methods:

- <code title="get /v1/sessions/{session_id}/events?beta=true">client.beta.sessions.events.<a href="./src/anthropic/resources/beta/sessions/events.py">list</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/event_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_event.py">SyncPageCursor[BetaManagedAgentsSessionEvent]</a></code>
- <code title="post /v1/sessions/{session_id}/events?beta=true">client.beta.sessions.events.<a href="./src/anthropic/resources/beta/sessions/events.py">send</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/event_send_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_send_session_events.py">BetaManagedAgentsSendSessionEvents</a></code>
- <code title="get /v1/sessions/{session_id}/events/stream?beta=true">client.beta.sessions.events.<a href="./src/anthropic/resources/beta/sessions/events.py">stream</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/event_stream_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_stream_session_events.py">BetaManagedAgentsStreamSessionEvents</a></code>

### Resources

Types:

```python
from anthropic.types.beta.sessions import (
    BetaManagedAgentsDeleteSessionResource,
    BetaManagedAgentsFileResource,
    BetaManagedAgentsGitHubRepositoryResource,
    BetaManagedAgentsMemoryStoreResource,
    BetaManagedAgentsSessionResource,
    ResourceRetrieveResponse,
    ResourceUpdateResponse,
)
```

Methods:

- <code title="get /v1/sessions/{session_id}/resources/{resource_id}?beta=true">client.beta.sessions.resources.<a href="./src/anthropic/resources/beta/sessions/resources.py">retrieve</a>(resource_id, \*, session_id) -> <a href="./src/anthropic/types/beta/sessions/resource_retrieve_response.py">ResourceRetrieveResponse</a></code>
- <code title="post /v1/sessions/{session_id}/resources/{resource_id}?beta=true">client.beta.sessions.resources.<a href="./src/anthropic/resources/beta/sessions/resources.py">update</a>(resource_id, \*, session_id, \*\*<a href="src/anthropic/types/beta/sessions/resource_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/resource_update_response.py">ResourceUpdateResponse</a></code>
- <code title="get /v1/sessions/{session_id}/resources?beta=true">client.beta.sessions.resources.<a href="./src/anthropic/resources/beta/sessions/resources.py">list</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/resource_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_resource.py">SyncPageCursor[BetaManagedAgentsSessionResource]</a></code>
- <code title="delete /v1/sessions/{session_id}/resources/{resource_id}?beta=true">client.beta.sessions.resources.<a href="./src/anthropic/resources/beta/sessions/resources.py">delete</a>(resource_id, \*, session_id) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_delete_session_resource.py">BetaManagedAgentsDeleteSessionResource</a></code>
- <code title="post /v1/sessions/{session_id}/resources?beta=true">client.beta.sessions.resources.<a href="./src/anthropic/resources/beta/sessions/resources.py">add</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/resource_add_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_file_resource.py">BetaManagedAgentsFileResource</a></code>

### Threads

Types:

```python
from anthropic.types.beta.sessions import (
    BetaManagedAgentsSessionThread,
    BetaManagedAgentsSessionThreadStats,
    BetaManagedAgentsSessionThreadStatus,
    BetaManagedAgentsSessionThreadUsage,
    BetaManagedAgentsStreamSessionThreadEvents,
)
```

Methods:

- <code title="get /v1/sessions/{session_id}/threads/{thread_id}?beta=true">client.beta.sessions.threads.<a href="./src/anthropic/resources/beta/sessions/threads/threads.py">retrieve</a>(thread_id, \*, session_id) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_thread.py">BetaManagedAgentsSessionThread</a></code>
- <code title="get /v1/sessions/{session_id}/threads?beta=true">client.beta.sessions.threads.<a href="./src/anthropic/resources/beta/sessions/threads/threads.py">list</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/thread_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_thread.py">SyncPageCursor[BetaManagedAgentsSessionThread]</a></code>
- <code title="post /v1/sessions/{session_id}/threads/{thread_id}/archive?beta=true">client.beta.sessions.threads.<a href="./src/anthropic/resources/beta/sessions/threads/threads.py">archive</a>(thread_id, \*, session_id) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_thread.py">BetaManagedAgentsSessionThread</a></code>

#### Events

Methods:

- <code title="get /v1/sessions/{session_id}/threads/{thread_id}/events?beta=true">client.beta.sessions.threads.events.<a href="./src/anthropic/resources/beta/sessions/threads/events.py">list</a>(thread_id, \*, session_id, \*\*<a href="src/anthropic/types/beta/sessions/threads/event_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_event.py">SyncPageCursor[BetaManagedAgentsSessionEvent]</a></code>
- <code title="get /v1/sessions/{session_id}/threads/{thread_id}/stream?beta=true">client.beta.sessions.threads.events.<a href="./src/anthropic/resources/beta/sessions/threads/events.py">stream</a>(thread_id, \*, session_id, \*\*<a href="src/anthropic/types/beta/sessions/threads/event_stream_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_stream_session_thread_events.py">BetaManagedAgentsStreamSessionThreadEvents</a></code>

## Deployments

Types:

```python
from anthropic.types.beta import (
    BetaManagedAgentsAgentArchivedDeploymentPausedReasonError,
    BetaManagedAgentsDeployment,
    BetaManagedAgentsDeploymentInitialEvent,
    BetaManagedAgentsDeploymentInitialEventParams,
    BetaManagedAgentsDeploymentPausedReason,
    BetaManagedAgentsDeploymentPausedReasonError,
    BetaManagedAgentsDeploymentStatus,
    BetaManagedAgentsDeploymentSystemMessageEvent,
    BetaManagedAgentsDeploymentUserDefineOutcomeEvent,
    BetaManagedAgentsDeploymentUserMessageEvent,
    BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonError,
    BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonError,
    BetaManagedAgentsErrorDeploymentPausedReason,
    BetaManagedAgentsFileNotFoundDeploymentPausedReasonError,
    BetaManagedAgentsFileResourceConfig,
    BetaManagedAgentsGitHubRepositoryResourceConfig,
    BetaManagedAgentsManualDeploymentPausedReason,
    BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonError,
    BetaManagedAgentsMemoryStoreArchivedDeploymentPausedReasonError,
    BetaManagedAgentsMemoryStoreResourceConfig,
    BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonError,
    BetaManagedAgentsSchedule,
    BetaManagedAgentsScheduleParams,
    BetaManagedAgentsSelfHostedResourcesUnsupportedDeploymentPausedReasonError,
    BetaManagedAgentsSessionResourceConfig,
    BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonError,
    BetaManagedAgentsSkillNotFoundDeploymentPausedReasonError,
    BetaManagedAgentsUnknownDeploymentPausedReasonError,
    BetaManagedAgentsVaultArchivedDeploymentPausedReasonError,
    BetaManagedAgentsVaultNotFoundDeploymentPausedReasonError,
    BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonError,
)
```

Methods:

- <code title="post /v1/deployments?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">create</a>(\*\*<a href="src/anthropic/types/beta/deployment_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">BetaManagedAgentsDeployment</a></code>
- <code title="get /v1/deployments/{deployment_id}?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">retrieve</a>(deployment_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">BetaManagedAgentsDeployment</a></code>
- <code title="post /v1/deployments/{deployment_id}?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">update</a>(deployment_id, \*\*<a href="src/anthropic/types/beta/deployment_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">BetaManagedAgentsDeployment</a></code>
- <code title="get /v1/deployments?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">list</a>(\*\*<a href="src/anthropic/types/beta/deployment_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">SyncPageCursor[BetaManagedAgentsDeployment]</a></code>
- <code title="post /v1/deployments/{deployment_id}/archive?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">archive</a>(deployment_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">BetaManagedAgentsDeployment</a></code>
- <code title="post /v1/deployments/{deployment_id}/pause?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">pause</a>(deployment_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">BetaManagedAgentsDeployment</a></code>
- <code title="post /v1/deployments/{deployment_id}/run?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">run</a>(deployment_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment_run.py">BetaManagedAgentsDeploymentRun</a></code>
- <code title="post /v1/deployments/{deployment_id}/unpause?beta=true">client.beta.deployments.<a href="./src/anthropic/resources/beta/deployments.py">unpause</a>(deployment_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment.py">BetaManagedAgentsDeployment</a></code>

## DeploymentRuns

Types:

```python
from anthropic.types.beta import (
    BetaManagedAgentsAgentArchivedRunError,
    BetaManagedAgentsDeploymentRun,
    BetaManagedAgentsEnvironmentArchivedRunError,
    BetaManagedAgentsEnvironmentNotFoundRunError,
    BetaManagedAgentsFileNotFoundRunError,
    BetaManagedAgentsManualTriggerContext,
    BetaManagedAgentsMCPEgressBlockedRunError,
    BetaManagedAgentsMemoryStoreArchivedRunError,
    BetaManagedAgentsOrganizationDisabledRunError,
    BetaManagedAgentsScheduleTriggerContext,
    BetaManagedAgentsSelfHostedResourcesUnsupportedRunError,
    BetaManagedAgentsSessionCreationRejectedRunError,
    BetaManagedAgentsSessionRateLimitedRunError,
    BetaManagedAgentsSessionResourceNotFoundRunError,
    BetaManagedAgentsSkillNotFoundRunError,
    BetaManagedAgentsTriggerContext,
    BetaManagedAgentsTriggerType,
    BetaManagedAgentsUnknownRunError,
    BetaManagedAgentsVaultArchivedRunError,
    BetaManagedAgentsVaultNotFoundRunError,
    BetaManagedAgentsWorkspaceArchivedRunError,
)
```

Methods:

- <code title="get /v1/deployment_runs/{deployment_run_id}?beta=true">client.beta.deployment_runs.<a href="./src/anthropic/resources/beta/deployment_runs.py">retrieve</a>(deployment_run_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment_run.py">BetaManagedAgentsDeploymentRun</a></code>
- <code title="get /v1/deployment_runs?beta=true">client.beta.deployment_runs.<a href="./src/anthropic/resources/beta/deployment_runs.py">list</a>(\*\*<a href="src/anthropic/types/beta/deployment_run_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deployment_run.py">SyncPageCursor[BetaManagedAgentsDeploymentRun]</a></code>

## Vaults

Types:

```python
from anthropic.types.beta import BetaManagedAgentsDeletedVault, BetaManagedAgentsVault
```

Methods:

- <code title="post /v1/vaults?beta=true">client.beta.vaults.<a href="./src/anthropic/resources/beta/vaults/vaults.py">create</a>(\*\*<a href="src/anthropic/types/beta/vault_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_vault.py">BetaManagedAgentsVault</a></code>
- <code title="get /v1/vaults/{vault_id}?beta=true">client.beta.vaults.<a href="./src/anthropic/resources/beta/vaults/vaults.py">retrieve</a>(vault_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_vault.py">BetaManagedAgentsVault</a></code>
- <code title="post /v1/vaults/{vault_id}?beta=true">client.beta.vaults.<a href="./src/anthropic/resources/beta/vaults/vaults.py">update</a>(vault_id, \*\*<a href="src/anthropic/types/beta/vault_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_vault.py">BetaManagedAgentsVault</a></code>
- <code title="get /v1/vaults?beta=true">client.beta.vaults.<a href="./src/anthropic/resources/beta/vaults/vaults.py">list</a>(\*\*<a href="src/anthropic/types/beta/vault_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_vault.py">SyncPageCursor[BetaManagedAgentsVault]</a></code>
- <code title="delete /v1/vaults/{vault_id}?beta=true">client.beta.vaults.<a href="./src/anthropic/resources/beta/vaults/vaults.py">delete</a>(vault_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deleted_vault.py">BetaManagedAgentsDeletedVault</a></code>
- <code title="post /v1/vaults/{vault_id}/archive?beta=true">client.beta.vaults.<a href="./src/anthropic/resources/beta/vaults/vaults.py">archive</a>(vault_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_vault.py">BetaManagedAgentsVault</a></code>

### Credentials

Types:

```python
from anthropic.types.beta.vaults import (
    BetaManagedAgentsCredential,
    BetaManagedAgentsCredentialNetworkingParams,
    BetaManagedAgentsCredentialValidation,
    BetaManagedAgentsCredentialValidationStatus,
    BetaManagedAgentsDeletedCredential,
    BetaManagedAgentsEnvironmentVariableAuthResponse,
    BetaManagedAgentsEnvironmentVariableCreateParams,
    BetaManagedAgentsEnvironmentVariableUpdateParams,
    BetaManagedAgentsInjectionLocationParams,
    BetaManagedAgentsInjectionLocationResponse,
    BetaManagedAgentsInjectionLocationUpdateParams,
    BetaManagedAgentsLimitedCredentialNetworkingParams,
    BetaManagedAgentsLimitedCredentialNetworkingResponse,
    BetaManagedAgentsMCPOAuthAuthResponse,
    BetaManagedAgentsMCPOAuthCreateParams,
    BetaManagedAgentsMCPOAuthRefreshParams,
    BetaManagedAgentsMCPOAuthRefreshResponse,
    BetaManagedAgentsMCPOAuthRefreshUpdateParams,
    BetaManagedAgentsMCPOAuthUpdateParams,
    BetaManagedAgentsMCPProbe,
    BetaManagedAgentsRefreshHTTPResponse,
    BetaManagedAgentsRefreshObject,
    BetaManagedAgentsStaticBearerAuthResponse,
    BetaManagedAgentsStaticBearerCreateParams,
    BetaManagedAgentsStaticBearerUpdateParams,
    BetaManagedAgentsTokenEndpointAuthBasicParam,
    BetaManagedAgentsTokenEndpointAuthBasicResponse,
    BetaManagedAgentsTokenEndpointAuthBasicUpdateParam,
    BetaManagedAgentsTokenEndpointAuthNoneParam,
    BetaManagedAgentsTokenEndpointAuthNoneResponse,
    BetaManagedAgentsTokenEndpointAuthPostParam,
    BetaManagedAgentsTokenEndpointAuthPostResponse,
    BetaManagedAgentsTokenEndpointAuthPostUpdateParam,
    BetaManagedAgentsUnrestrictedCredentialNetworkingParams,
    BetaManagedAgentsUnrestrictedCredentialNetworkingResponse,
)
```

Methods:

- <code title="post /v1/vaults/{vault_id}/credentials?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">create</a>(vault_id, \*\*<a href="src/anthropic/types/beta/vaults/credential_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_credential.py">BetaManagedAgentsCredential</a></code>
- <code title="get /v1/vaults/{vault_id}/credentials/{credential_id}?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">retrieve</a>(credential_id, \*, vault_id) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_credential.py">BetaManagedAgentsCredential</a></code>
- <code title="post /v1/vaults/{vault_id}/credentials/{credential_id}?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">update</a>(credential_id, \*, vault_id, \*\*<a href="src/anthropic/types/beta/vaults/credential_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_credential.py">BetaManagedAgentsCredential</a></code>
- <code title="get /v1/vaults/{vault_id}/credentials?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">list</a>(vault_id, \*\*<a href="src/anthropic/types/beta/vaults/credential_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_credential.py">SyncPageCursor[BetaManagedAgentsCredential]</a></code>
- <code title="delete /v1/vaults/{vault_id}/credentials/{credential_id}?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">delete</a>(credential_id, \*, vault_id) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_deleted_credential.py">BetaManagedAgentsDeletedCredential</a></code>
- <code title="post /v1/vaults/{vault_id}/credentials/{credential_id}/archive?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">archive</a>(credential_id, \*, vault_id) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_credential.py">BetaManagedAgentsCredential</a></code>
- <code title="post /v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate?beta=true">client.beta.vaults.credentials.<a href="./src/anthropic/resources/beta/vaults/credentials.py">mcp_oauth_validate</a>(credential_id, \*, vault_id) -> <a href="./src/anthropic/types/beta/vaults/beta_managed_agents_credential_validation.py">BetaManagedAgentsCredentialValidation</a></code>

## MemoryStores

Types:

```python
from anthropic.types.beta import BetaManagedAgentsDeletedMemoryStore, BetaManagedAgentsMemoryStore
```

Methods:

- <code title="post /v1/memory_stores?beta=true">client.beta.memory_stores.<a href="./src/anthropic/resources/beta/memory_stores/memory_stores.py">create</a>(\*\*<a href="src/anthropic/types/beta/memory_store_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_memory_store.py">BetaManagedAgentsMemoryStore</a></code>
- <code title="get /v1/memory_stores/{memory_store_id}?beta=true">client.beta.memory_stores.<a href="./src/anthropic/resources/beta/memory_stores/memory_stores.py">retrieve</a>(memory_store_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_memory_store.py">BetaManagedAgentsMemoryStore</a></code>
- <code title="post /v1/memory_stores/{memory_store_id}?beta=true">client.beta.memory_stores.<a href="./src/anthropic/resources/beta/memory_stores/memory_stores.py">update</a>(memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_store_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_memory_store.py">BetaManagedAgentsMemoryStore</a></code>
- <code title="get /v1/memory_stores?beta=true">client.beta.memory_stores.<a href="./src/anthropic/resources/beta/memory_stores/memory_stores.py">list</a>(\*\*<a href="src/anthropic/types/beta/memory_store_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_memory_store.py">SyncPageCursor[BetaManagedAgentsMemoryStore]</a></code>
- <code title="delete /v1/memory_stores/{memory_store_id}?beta=true">client.beta.memory_stores.<a href="./src/anthropic/resources/beta/memory_stores/memory_stores.py">delete</a>(memory_store_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deleted_memory_store.py">BetaManagedAgentsDeletedMemoryStore</a></code>
- <code title="post /v1/memory_stores/{memory_store_id}/archive?beta=true">client.beta.memory_stores.<a href="./src/anthropic/resources/beta/memory_stores/memory_stores.py">archive</a>(memory_store_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_memory_store.py">BetaManagedAgentsMemoryStore</a></code>

### Memories

Types:

```python
from anthropic.types.beta.memory_stores import (
    BetaManagedAgentsDeletedMemory,
    BetaManagedAgentsMemory,
    BetaManagedAgentsMemoryListItem,
    BetaManagedAgentsMemoryPrefix,
    BetaManagedAgentsMemoryView,
    BetaManagedAgentsPreconditionParam,
)
```

Methods:

- <code title="post /v1/memory_stores/{memory_store_id}/memories?beta=true">client.beta.memory_stores.memories.<a href="./src/anthropic/resources/beta/memory_stores/memories.py">create</a>(memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory.py">BetaManagedAgentsMemory</a></code>
- <code title="get /v1/memory_stores/{memory_store_id}/memories/{memory_id}?beta=true">client.beta.memory_stores.memories.<a href="./src/anthropic/resources/beta/memory_stores/memories.py">retrieve</a>(memory_id, \*, memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_retrieve_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory.py">BetaManagedAgentsMemory</a></code>
- <code title="post /v1/memory_stores/{memory_store_id}/memories/{memory_id}?beta=true">client.beta.memory_stores.memories.<a href="./src/anthropic/resources/beta/memory_stores/memories.py">update</a>(memory_id, \*, memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory.py">BetaManagedAgentsMemory</a></code>
- <code title="get /v1/memory_stores/{memory_store_id}/memories?beta=true">client.beta.memory_stores.memories.<a href="./src/anthropic/resources/beta/memory_stores/memories.py">list</a>(memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory_list_item.py">SyncPageCursor[BetaManagedAgentsMemoryListItem]</a></code>
- <code title="delete /v1/memory_stores/{memory_store_id}/memories/{memory_id}?beta=true">client.beta.memory_stores.memories.<a href="./src/anthropic/resources/beta/memory_stores/memories.py">delete</a>(memory_id, \*, memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_delete_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_deleted_memory.py">BetaManagedAgentsDeletedMemory</a></code>

### MemoryVersions

Types:

```python
from anthropic.types.beta.memory_stores import (
    BetaManagedAgentsActor,
    BetaManagedAgentsAPIActor,
    BetaManagedAgentsMemoryVersion,
    BetaManagedAgentsMemoryVersionOperation,
    BetaManagedAgentsServiceAccountActor,
    BetaManagedAgentsSessionActor,
    BetaManagedAgentsUserActor,
)
```

Methods:

- <code title="get /v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}?beta=true">client.beta.memory_stores.memory_versions.<a href="./src/anthropic/resources/beta/memory_stores/memory_versions.py">retrieve</a>(memory_version_id, \*, memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_version_retrieve_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory_version.py">BetaManagedAgentsMemoryVersion</a></code>
- <code title="get /v1/memory_stores/{memory_store_id}/memory_versions?beta=true">client.beta.memory_stores.memory_versions.<a href="./src/anthropic/resources/beta/memory_stores/memory_versions.py">list</a>(memory_store_id, \*\*<a href="src/anthropic/types/beta/memory_stores/memory_version_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory_version.py">SyncPageCursor[BetaManagedAgentsMemoryVersion]</a></code>
- <code title="post /v1/memory_stores/{memory_store_id}/memory_versions/{memory_version_id}/redact?beta=true">client.beta.memory_stores.memory_versions.<a href="./src/anthropic/resources/beta/memory_stores/memory_versions.py">redact</a>(memory_version_id, \*, memory_store_id) -> <a href="./src/anthropic/types/beta/memory_stores/beta_managed_agents_memory_version.py">BetaManagedAgentsMemoryVersion</a></code>

## Files

Types:

```python
from anthropic.types.beta import BetaDeletedFile, BetaFileMetadata, BetaFileScope
```

Methods:

- <code title="get /v1/files?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">list</a>(\*\*<a href="src/anthropic/types/beta/file_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_file_metadata.py">SyncPageCursor[BetaFileMetadata]</a></code>
- <code title="delete /v1/files/{file_id}?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">delete</a>(file_id) -> <a href="./src/anthropic/types/beta/beta_deleted_file.py">BetaDeletedFile</a></code>
- <code title="get /v1/files/{file_id}/content?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">download</a>(file_id) -> BinaryAPIResponse</code>
- <code title="get /v1/files/{file_id}?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">retrieve_metadata</a>(file_id) -> <a href="./src/anthropic/types/beta/beta_file_metadata.py">BetaFileMetadata</a></code>
- <code title="post /v1/files?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">upload</a>(\*\*<a href="src/anthropic/types/beta/file_upload_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_file_metadata.py">BetaFileMetadata</a></code>

## Skills

Types:

```python
from anthropic.types.beta import BetaDeletedSkill, BetaSkill, BetaSkillSource
```

Methods:

- <code title="post /v1/skills?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">create</a>(\*\*<a href="src/anthropic/types/beta/skill_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_skill.py">BetaSkill</a></code>
- <code title="get /v1/skills/{skill_id}?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">retrieve</a>(skill_id) -> <a href="./src/anthropic/types/beta/beta_skill.py">BetaSkill</a></code>
- <code title="get /v1/skills?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">list</a>(\*\*<a href="src/anthropic/types/beta/skill_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_skill.py">SyncPageCursor[BetaSkill]</a></code>
- <code title="delete /v1/skills/{skill_id}?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">delete</a>(skill_id) -> <a href="./src/anthropic/types/beta/beta_deleted_skill.py">BetaDeletedSkill</a></code>

### Versions

Types:

```python
from anthropic.types.beta.skills import BetaDeletedSkillVersion, BetaSkillVersion
```

Methods:

- <code title="post /v1/skills/{skill_id}/versions?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">create</a>(skill_id, \*\*<a href="src/anthropic/types/beta/skills/version_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/skills/beta_skill_version.py">BetaSkillVersion</a></code>
- <code title="get /v1/skills/{skill_id}/versions/{version}?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">retrieve</a>(version, \*, skill_id) -> <a href="./src/anthropic/types/beta/skills/beta_skill_version.py">BetaSkillVersion</a></code>
- <code title="get /v1/skills/{skill_id}/versions?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">list</a>(skill_id, \*\*<a href="src/anthropic/types/beta/skills/version_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/skills/beta_skill_version.py">SyncPageCursor[BetaSkillVersion]</a></code>
- <code title="delete /v1/skills/{skill_id}/versions/{version}?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">delete</a>(version, \*, skill_id) -> <a href="./src/anthropic/types/beta/skills/beta_deleted_skill_version.py">BetaDeletedSkillVersion</a></code>
- <code title="get /v1/skills/{skill_id}/versions/{version}/content?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">download</a>(version, \*, skill_id) -> BinaryAPIResponse</code>

## Webhooks

Types:

```python
from anthropic.types.beta import (
    BetaWebhookAgentArchivedEventData,
    BetaWebhookAgentCreatedEventData,
    BetaWebhookAgentDeletedEventData,
    BetaWebhookAgentUpdatedEventData,
    BetaWebhookDeploymentArchivedEventData,
    BetaWebhookDeploymentCreatedEventData,
    BetaWebhookDeploymentDeletedEventData,
    BetaWebhookDeploymentPausedEventData,
    BetaWebhookDeploymentRunFailedEventData,
    BetaWebhookDeploymentRunStartedEventData,
    BetaWebhookDeploymentRunSucceededEventData,
    BetaWebhookDeploymentUnpausedEventData,
    BetaWebhookDeploymentUpdatedEventData,
    BetaWebhookEnvironmentArchivedEventData,
    BetaWebhookEnvironmentCreatedEventData,
    BetaWebhookEnvironmentDeletedEventData,
    BetaWebhookEnvironmentUpdatedEventData,
    BetaWebhookEvent,
    BetaWebhookEventData,
    BetaWebhookMemoryStoreArchivedEventData,
    BetaWebhookMemoryStoreCreatedEventData,
    BetaWebhookMemoryStoreDeletedEventData,
    BetaWebhookSessionArchivedEventData,
    BetaWebhookSessionBudgetReachedEventData,
    BetaWebhookSessionCreatedEventData,
    BetaWebhookSessionDeletedEventData,
    BetaWebhookSessionIdledEventData,
    BetaWebhookSessionOutcomeEvaluationEndedEventData,
    BetaWebhookSessionPendingEventData,
    BetaWebhookSessionRequiresActionEventData,
    BetaWebhookSessionRunningEventData,
    BetaWebhookSessionStatusIdledEventData,
    BetaWebhookSessionStatusRescheduledEventData,
    BetaWebhookSessionStatusRunStartedEventData,
    BetaWebhookSessionStatusTerminatedEventData,
    BetaWebhookSessionThreadCreatedEventData,
    BetaWebhookSessionThreadIdledEventData,
    BetaWebhookSessionThreadTerminatedEventData,
    BetaWebhookSessionUpdatedEventData,
    BetaWebhookVaultArchivedEventData,
    BetaWebhookVaultCreatedEventData,
    BetaWebhookVaultCredentialArchivedEventData,
    BetaWebhookVaultCredentialCreatedEventData,
    BetaWebhookVaultCredentialDeletedEventData,
    BetaWebhookVaultCredentialRefreshFailedEventData,
    BetaWebhookVaultDeletedEventData,
    UnwrapWebhookEvent,
)
```

## UserProfiles

Types:

```python
from anthropic.types.beta import (
    BetaUserProfile,
    BetaUserProfileEnrollmentURL,
    BetaUserProfileExternalUserDetails,
    BetaUserProfileExternalUserDetailsParams,
    BetaUserProfileTrustGrant,
)
```

Methods:

- <code title="post /v1/user_profiles?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">create</a>(\*\*<a href="src/anthropic/types/beta/user_profile_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">BetaUserProfile</a></code>
- <code title="get /v1/user_profiles/{user_profile_id}?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">retrieve</a>(user_profile_id) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">BetaUserProfile</a></code>
- <code title="post /v1/user_profiles/{user_profile_id}?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">update</a>(user_profile_id, \*\*<a href="src/anthropic/types/beta/user_profile_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">BetaUserProfile</a></code>
- <code title="get /v1/user_profiles?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">list</a>(\*\*<a href="src/anthropic/types/beta/user_profile_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">SyncPageCursor[BetaUserProfile]</a></code>
- <code title="post /v1/user_profiles/{user_profile_id}/enrollment_url?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">create_enrollment_url</a>(user_profile_id) -> <a href="./src/anthropic/types/beta/beta_user_profile_enrollment_url.py">BetaUserProfileEnrollmentURL</a></code>

## Dreams

Types:

```python
from anthropic.types.beta import (
    BetaDream,
    BetaDreamError,
    BetaDreamInput,
    BetaDreamInputParam,
    BetaDreamMemoryStoreInput,
    BetaDreamMemoryStoreInputParam,
    BetaDreamModelConfig,
    BetaDreamModelConfigParam,
    BetaDreamOutput,
    BetaDreamSessionsInput,
    BetaDreamSessionsInputParam,
    BetaDreamStatus,
    BetaDreamUsage,
    BetaOutputBehavior,
    BetaOutputBehaviorParam,
    BetaOutputBehaviorCreateNew,
    BetaOutputBehaviorCreateNewParam,
    BetaOutputBehaviorUpdateExisting,
    BetaOutputBehaviorUpdateExistingParam,
)
```

Methods:

- <code title="post /v1/dreams?beta=true">client.beta.dreams.<a href="./src/anthropic/resources/beta/dreams.py">create</a>(\*\*<a href="src/anthropic/types/beta/dream_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_dream.py">BetaDream</a></code>
- <code title="get /v1/dreams/{dream_id}?beta=true">client.beta.dreams.<a href="./src/anthropic/resources/beta/dreams.py">retrieve</a>(dream_id) -> <a href="./src/anthropic/types/beta/beta_dream.py">BetaDream</a></code>
- <code title="get /v1/dreams?beta=true">client.beta.dreams.<a href="./src/anthropic/resources/beta/dreams.py">list</a>(\*\*<a href="src/anthropic/types/beta/dream_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_dream.py">SyncPageCursor[BetaDream]</a></code>
- <code title="post /v1/dreams/{dream_id}/archive?beta=true">client.beta.dreams.<a href="./src/anthropic/resources/beta/dreams.py">archive</a>(dream_id) -> <a href="./src/anthropic/types/beta/beta_dream.py">BetaDream</a></code>
- <code title="post /v1/dreams/{dream_id}/cancel?beta=true">client.beta.dreams.<a href="./src/anthropic/resources/beta/dreams.py">cancel</a>(dream_id) -> <a href="./src/anthropic/types/beta/beta_dream.py">BetaDream</a></code>

## Tunnels

Types:

```python
from anthropic.types.beta import BetaTunnel, BetaTunnelToken
```

Methods:

- <code title="post /v1/tunnels?beta=true">client.beta.tunnels.<a href="./src/anthropic/resources/beta/tunnels/tunnels.py">create</a>(\*\*<a href="src/anthropic/types/beta/tunnel_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_tunnel.py">BetaTunnel</a></code>
- <code title="get /v1/tunnels/{tunnel_id}?beta=true">client.beta.tunnels.<a href="./src/anthropic/resources/beta/tunnels/tunnels.py">retrieve</a>(tunnel_id) -> <a href="./src/anthropic/types/beta/beta_tunnel.py">BetaTunnel</a></code>
- <code title="get /v1/tunnels?beta=true">client.beta.tunnels.<a href="./src/anthropic/resources/beta/tunnels/tunnels.py">list</a>(\*\*<a href="src/anthropic/types/beta/tunnel_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_tunnel.py">SyncPageCursor[BetaTunnel]</a></code>
- <code title="post /v1/tunnels/{tunnel_id}/archive?beta=true">client.beta.tunnels.<a href="./src/anthropic/resources/beta/tunnels/tunnels.py">archive</a>(tunnel_id) -> <a href="./src/anthropic/types/beta/beta_tunnel.py">BetaTunnel</a></code>
- <code title="post /v1/tunnels/{tunnel_id}/reveal_token?beta=true">client.beta.tunnels.<a href="./src/anthropic/resources/beta/tunnels/tunnels.py">reveal_token</a>(tunnel_id) -> <a href="./src/anthropic/types/beta/beta_tunnel_token.py">BetaTunnelToken</a></code>
- <code title="post /v1/tunnels/{tunnel_id}/rotate_token?beta=true">client.beta.tunnels.<a href="./src/anthropic/resources/beta/tunnels/tunnels.py">rotate_token</a>(tunnel_id, \*\*<a href="src/anthropic/types/beta/tunnel_rotate_token_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_tunnel_token.py">BetaTunnelToken</a></code>

### Certificates

Types:

```python
from anthropic.types.beta.tunnels import BetaTunnelCertificate
```

Methods:

- <code title="post /v1/tunnels/{tunnel_id}/certificates?beta=true">client.beta.tunnels.certificates.<a href="./src/anthropic/resources/beta/tunnels/certificates.py">create</a>(tunnel_id, \*\*<a href="src/anthropic/types/beta/tunnels/certificate_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/tunnels/beta_tunnel_certificate.py">BetaTunnelCertificate</a></code>
- <code title="get /v1/tunnels/{tunnel_id}/certificates/{certificate_id}?beta=true">client.beta.tunnels.certificates.<a href="./src/anthropic/resources/beta/tunnels/certificates.py">retrieve</a>(certificate_id, \*, tunnel_id) -> <a href="./src/anthropic/types/beta/tunnels/beta_tunnel_certificate.py">BetaTunnelCertificate</a></code>
- <code title="get /v1/tunnels/{tunnel_id}/certificates?beta=true">client.beta.tunnels.certificates.<a href="./src/anthropic/resources/beta/tunnels/certificates.py">list</a>(tunnel_id, \*\*<a href="src/anthropic/types/beta/tunnels/certificate_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/tunnels/beta_tunnel_certificate.py">SyncPageCursor[BetaTunnelCertificate]</a></code>
- <code title="post /v1/tunnels/{tunnel_id}/certificates/{certificate_id}/archive?beta=true">client.beta.tunnels.certificates.<a href="./src/anthropic/resources/beta/tunnels/certificates.py">archive</a>(certificate_id, \*, tunnel_id) -> <a href="./src/anthropic/types/beta/tunnels/beta_tunnel_certificate.py">BetaTunnelCertificate</a></code>

## Organization

Types:

```python
from anthropic.types.beta import BetaOrganization, BetaOrganizationRole
```

Methods:

- <code title="get /v1/organizations/me?beta=true">client.beta.organization.<a href="./src/anthropic/resources/beta/organization/organization.py">retrieve</a>() -> <a href="./src/anthropic/types/beta/beta_organization.py">BetaOrganization</a></code>

### APIKeys

Types:

```python
from anthropic.types.beta.organization import (
    BetaAPIKey,
    BetaAPIKeyCreatedBy,
    BetaAPIKeyOrganizationScope,
    BetaAPIKeyServiceAccountActor,
    BetaAPIKeyUserActor,
    BetaAPIKeyWorkspaceScope,
)
```

Methods:

- <code title="get /v1/organizations/api_keys/{api_key_id}?beta=true">client.beta.organization.api_keys.<a href="./src/anthropic/resources/beta/organization/api_keys.py">retrieve</a>(api_key_id) -> <a href="./src/anthropic/types/beta/organization/beta_api_key.py">BetaAPIKey</a></code>
- <code title="post /v1/organizations/api_keys/{api_key_id}?beta=true">client.beta.organization.api_keys.<a href="./src/anthropic/resources/beta/organization/api_keys.py">update</a>(api_key_id, \*\*<a href="src/anthropic/types/beta/organization/api_key_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_api_key.py">BetaAPIKey</a></code>
- <code title="get /v1/organizations/api_keys?beta=true">client.beta.organization.api_keys.<a href="./src/anthropic/resources/beta/organization/api_keys.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/api_key_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_api_key.py">SyncPage[BetaAPIKey]</a></code>

### ExternalKeys

Types:

```python
from anthropic.types.beta.organization import (
    BetaAWSExternalKeyConfig,
    BetaAWSExternalKeyConfigParam,
    BetaAzureExternalKeyConfig,
    BetaAzureExternalKeyConfigParam,
    BetaExternalKey,
    BetaExternalKeyAttachedAttachment,
    BetaExternalKeyUnattachedAttachment,
    BetaGCPExternalKeyConfig,
    BetaGCPExternalKeyConfigParam,
    ExternalKeyDeleteResponse,
    ExternalKeyValidateResponse,
)
```

Methods:

- <code title="post /v1/organizations/external_keys?beta=true">client.beta.organization.external_keys.<a href="./src/anthropic/resources/beta/organization/external_keys.py">create</a>(\*\*<a href="src/anthropic/types/beta/organization/external_key_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_external_key.py">BetaExternalKey</a></code>
- <code title="get /v1/organizations/external_keys/{external_key_id}?beta=true">client.beta.organization.external_keys.<a href="./src/anthropic/resources/beta/organization/external_keys.py">retrieve</a>(external_key_id) -> <a href="./src/anthropic/types/beta/organization/beta_external_key.py">BetaExternalKey</a></code>
- <code title="post /v1/organizations/external_keys/{external_key_id}?beta=true">client.beta.organization.external_keys.<a href="./src/anthropic/resources/beta/organization/external_keys.py">update</a>(external_key_id, \*\*<a href="src/anthropic/types/beta/organization/external_key_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_external_key.py">BetaExternalKey</a></code>
- <code title="get /v1/organizations/external_keys?beta=true">client.beta.organization.external_keys.<a href="./src/anthropic/resources/beta/organization/external_keys.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/external_key_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_external_key.py">SyncPageCursor[BetaExternalKey]</a></code>
- <code title="delete /v1/organizations/external_keys/{external_key_id}?beta=true">client.beta.organization.external_keys.<a href="./src/anthropic/resources/beta/organization/external_keys.py">delete</a>(external_key_id) -> <a href="./src/anthropic/types/beta/organization/external_key_delete_response.py">ExternalKeyDeleteResponse</a></code>
- <code title="post /v1/organizations/external_keys/{external_key_id}/validate?beta=true">client.beta.organization.external_keys.<a href="./src/anthropic/resources/beta/organization/external_keys.py">validate</a>(external_key_id) -> <a href="./src/anthropic/types/beta/organization/external_key_validate_response.py">ExternalKeyValidateResponse</a></code>

### Federation

#### Issuers

Types:

```python
from anthropic.types.beta.organization.federation import (
    BetaFederationIssuer,
    BetaFederationIssuerPollStatus,
    BetaJWKSDiscovery,
    BetaJWKSDiscoveryParam,
    BetaJWKSExplicitURL,
    BetaJWKSExplicitURLParam,
    BetaJWKSInline,
    BetaJWKSInlineParam,
)
```

Methods:

- <code title="post /v1/organizations/federation_issuers?beta=true">client.beta.organization.federation.issuers.<a href="./src/anthropic/resources/beta/organization/federation/issuers.py">create</a>(\*\*<a href="src/anthropic/types/beta/organization/federation/issuer_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_issuer.py">BetaFederationIssuer</a></code>
- <code title="get /v1/organizations/federation_issuers/{federation_issuer_id}?beta=true">client.beta.organization.federation.issuers.<a href="./src/anthropic/resources/beta/organization/federation/issuers.py">retrieve</a>(federation_issuer_id) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_issuer.py">BetaFederationIssuer</a></code>
- <code title="post /v1/organizations/federation_issuers/{federation_issuer_id}?beta=true">client.beta.organization.federation.issuers.<a href="./src/anthropic/resources/beta/organization/federation/issuers.py">update</a>(federation_issuer_id, \*\*<a href="src/anthropic/types/beta/organization/federation/issuer_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_issuer.py">BetaFederationIssuer</a></code>
- <code title="get /v1/organizations/federation_issuers?beta=true">client.beta.organization.federation.issuers.<a href="./src/anthropic/resources/beta/organization/federation/issuers.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/federation/issuer_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_issuer.py">SyncPageCursor[BetaFederationIssuer]</a></code>
- <code title="post /v1/organizations/federation_issuers/{federation_issuer_id}/archive?beta=true">client.beta.organization.federation.issuers.<a href="./src/anthropic/resources/beta/organization/federation/issuers.py">archive</a>(federation_issuer_id) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_issuer.py">BetaFederationIssuer</a></code>

#### Rules

Types:

```python
from anthropic.types.beta.organization.federation import (
    BetaFederationRule,
    BetaFederationRuleMatch,
    BetaFederationRuleMatchParam,
    BetaFederationRuleWorkspace,
    BetaServiceAccountTarget,
    BetaServiceAccountTargetParam,
)
```

Methods:

- <code title="post /v1/organizations/federation_rules?beta=true">client.beta.organization.federation.rules.<a href="./src/anthropic/resources/beta/organization/federation/rules/rules.py">create</a>(\*\*<a href="src/anthropic/types/beta/organization/federation/rule_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule.py">BetaFederationRule</a></code>
- <code title="get /v1/organizations/federation_rules/{federation_rule_id}?beta=true">client.beta.organization.federation.rules.<a href="./src/anthropic/resources/beta/organization/federation/rules/rules.py">retrieve</a>(federation_rule_id) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule.py">BetaFederationRule</a></code>
- <code title="post /v1/organizations/federation_rules/{federation_rule_id}?beta=true">client.beta.organization.federation.rules.<a href="./src/anthropic/resources/beta/organization/federation/rules/rules.py">update</a>(federation_rule_id, \*\*<a href="src/anthropic/types/beta/organization/federation/rule_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule.py">BetaFederationRule</a></code>
- <code title="get /v1/organizations/federation_rules?beta=true">client.beta.organization.federation.rules.<a href="./src/anthropic/resources/beta/organization/federation/rules/rules.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/federation/rule_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule.py">SyncPageCursor[BetaFederationRule]</a></code>
- <code title="post /v1/organizations/federation_rules/{federation_rule_id}/archive?beta=true">client.beta.organization.federation.rules.<a href="./src/anthropic/resources/beta/organization/federation/rules/rules.py">archive</a>(federation_rule_id) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule.py">BetaFederationRule</a></code>

##### Workspaces

Types:

```python
from anthropic.types.beta.organization.federation.rules import WorkspaceRemoveResponse
```

Methods:

- <code title="get /v1/organizations/federation_rules/{federation_rule_id}/workspaces?beta=true">client.beta.organization.federation.rules.workspaces.<a href="./src/anthropic/resources/beta/organization/federation/rules/workspaces.py">list</a>(federation_rule_id, \*\*<a href="src/anthropic/types/beta/organization/federation/rules/workspace_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule_workspace.py">SyncPageCursor[BetaFederationRuleWorkspace]</a></code>
- <code title="post /v1/organizations/federation_rules/{federation_rule_id}/workspaces?beta=true">client.beta.organization.federation.rules.workspaces.<a href="./src/anthropic/resources/beta/organization/federation/rules/workspaces.py">add</a>(federation_rule_id, \*\*<a href="src/anthropic/types/beta/organization/federation/rules/workspace_add_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/federation/beta_federation_rule_workspace.py">BetaFederationRuleWorkspace</a></code>
- <code title="delete /v1/organizations/federation_rules/{federation_rule_id}/workspaces/{workspace_id}?beta=true">client.beta.organization.federation.rules.workspaces.<a href="./src/anthropic/resources/beta/organization/federation/rules/workspaces.py">remove</a>(workspace_id, \*, federation_rule_id) -> <a href="./src/anthropic/types/beta/organization/federation/rules/workspace_remove_response.py">WorkspaceRemoveResponse</a></code>

### Invites

Types:

```python
from anthropic.types.beta.organization import BetaOrganizationInvite, InviteDeleteResponse
```

Methods:

- <code title="post /v1/organizations/invites?beta=true">client.beta.organization.invites.<a href="./src/anthropic/resources/beta/organization/invites.py">create</a>(\*\*<a href="src/anthropic/types/beta/organization/invite_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_organization_invite.py">BetaOrganizationInvite</a></code>
- <code title="get /v1/organizations/invites/{invite_id}?beta=true">client.beta.organization.invites.<a href="./src/anthropic/resources/beta/organization/invites.py">retrieve</a>(invite_id) -> <a href="./src/anthropic/types/beta/organization/beta_organization_invite.py">BetaOrganizationInvite</a></code>
- <code title="get /v1/organizations/invites?beta=true">client.beta.organization.invites.<a href="./src/anthropic/resources/beta/organization/invites.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/invite_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_organization_invite.py">SyncPage[BetaOrganizationInvite]</a></code>
- <code title="delete /v1/organizations/invites/{invite_id}?beta=true">client.beta.organization.invites.<a href="./src/anthropic/resources/beta/organization/invites.py">delete</a>(invite_id) -> <a href="./src/anthropic/types/beta/organization/invite_delete_response.py">InviteDeleteResponse</a></code>

### ServiceAccounts

Types:

```python
from anthropic.types.beta.organization import BetaServiceAccount, BetaServiceAccountWorkspaceMember
```

Methods:

- <code title="post /v1/organizations/service_accounts?beta=true">client.beta.organization.service_accounts.<a href="./src/anthropic/resources/beta/organization/service_accounts/service_accounts.py">create</a>(\*\*<a href="src/anthropic/types/beta/organization/service_account_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account.py">BetaServiceAccount</a></code>
- <code title="get /v1/organizations/service_accounts/{service_account_id}?beta=true">client.beta.organization.service_accounts.<a href="./src/anthropic/resources/beta/organization/service_accounts/service_accounts.py">retrieve</a>(service_account_id) -> <a href="./src/anthropic/types/beta/organization/beta_service_account.py">BetaServiceAccount</a></code>
- <code title="post /v1/organizations/service_accounts/{service_account_id}?beta=true">client.beta.organization.service_accounts.<a href="./src/anthropic/resources/beta/organization/service_accounts/service_accounts.py">update</a>(service_account_id, \*\*<a href="src/anthropic/types/beta/organization/service_account_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account.py">BetaServiceAccount</a></code>
- <code title="get /v1/organizations/service_accounts?beta=true">client.beta.organization.service_accounts.<a href="./src/anthropic/resources/beta/organization/service_accounts/service_accounts.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/service_account_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account.py">SyncPageCursor[BetaServiceAccount]</a></code>
- <code title="post /v1/organizations/service_accounts/{service_account_id}/archive?beta=true">client.beta.organization.service_accounts.<a href="./src/anthropic/resources/beta/organization/service_accounts/service_accounts.py">archive</a>(service_account_id) -> <a href="./src/anthropic/types/beta/organization/beta_service_account.py">BetaServiceAccount</a></code>

#### Workspaces

Types:

```python
from anthropic.types.beta.organization.service_accounts import WorkspaceRemoveResponse
```

Methods:

- <code title="get /v1/organizations/service_accounts/{service_account_id}/workspaces?beta=true">client.beta.organization.service_accounts.workspaces.<a href="./src/anthropic/resources/beta/organization/service_accounts/workspaces.py">list</a>(service_account_id, \*\*<a href="src/anthropic/types/beta/organization/service_accounts/workspace_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account_workspace_member.py">SyncPageCursor[BetaServiceAccountWorkspaceMember]</a></code>
- <code title="post /v1/organizations/service_accounts/{service_account_id}/workspaces?beta=true">client.beta.organization.service_accounts.workspaces.<a href="./src/anthropic/resources/beta/organization/service_accounts/workspaces.py">add</a>(service_account_id, \*\*<a href="src/anthropic/types/beta/organization/service_accounts/workspace_add_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account_workspace_member.py">BetaServiceAccountWorkspaceMember</a></code>
- <code title="delete /v1/organizations/service_accounts/{service_account_id}/workspaces/{workspace_id}?beta=true">client.beta.organization.service_accounts.workspaces.<a href="./src/anthropic/resources/beta/organization/service_accounts/workspaces.py">remove</a>(workspace_id, \*, service_account_id) -> <a href="./src/anthropic/types/beta/organization/service_accounts/workspace_remove_response.py">WorkspaceRemoveResponse</a></code>

### Users

Types:

```python
from anthropic.types.beta.organization import BetaOrganizationUser, UserRemoveResponse
```

Methods:

- <code title="get /v1/organizations/users/{user_id}?beta=true">client.beta.organization.users.<a href="./src/anthropic/resources/beta/organization/users.py">retrieve</a>(user_id) -> <a href="./src/anthropic/types/beta/organization/beta_organization_user.py">BetaOrganizationUser</a></code>
- <code title="post /v1/organizations/users/{user_id}?beta=true">client.beta.organization.users.<a href="./src/anthropic/resources/beta/organization/users.py">update</a>(user_id, \*\*<a href="src/anthropic/types/beta/organization/user_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_organization_user.py">BetaOrganizationUser</a></code>
- <code title="get /v1/organizations/users?beta=true">client.beta.organization.users.<a href="./src/anthropic/resources/beta/organization/users.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/user_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_organization_user.py">SyncPage[BetaOrganizationUser]</a></code>
- <code title="delete /v1/organizations/users/{user_id}?beta=true">client.beta.organization.users.<a href="./src/anthropic/resources/beta/organization/users.py">remove</a>(user_id) -> <a href="./src/anthropic/types/beta/organization/user_remove_response.py">UserRemoveResponse</a></code>

### Workspaces

Types:

```python
from anthropic.types.beta.organization import (
    BetaAllowedInferenceGeo,
    BetaDataResidency,
    BetaDataResidencyCreateConfigParam,
    BetaDataResidencyUpdateConfigParam,
    BetaNoBillingWorkspaceRole,
    BetaWorkspace,
    BetaWorkspaceMember,
    BetaWorkspaceRole,
)
```

Methods:

- <code title="post /v1/organizations/workspaces?beta=true">client.beta.organization.workspaces.<a href="./src/anthropic/resources/beta/organization/workspaces/workspaces.py">create</a>(\*\*<a href="src/anthropic/types/beta/organization/workspace_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_workspace.py">BetaWorkspace</a></code>
- <code title="get /v1/organizations/workspaces/{workspace_id}?beta=true">client.beta.organization.workspaces.<a href="./src/anthropic/resources/beta/organization/workspaces/workspaces.py">retrieve</a>(workspace_id) -> <a href="./src/anthropic/types/beta/organization/beta_workspace.py">BetaWorkspace</a></code>
- <code title="post /v1/organizations/workspaces/{workspace_id}?beta=true">client.beta.organization.workspaces.<a href="./src/anthropic/resources/beta/organization/workspaces/workspaces.py">update</a>(workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspace_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_workspace.py">BetaWorkspace</a></code>
- <code title="get /v1/organizations/workspaces?beta=true">client.beta.organization.workspaces.<a href="./src/anthropic/resources/beta/organization/workspaces/workspaces.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/workspace_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_workspace.py">SyncPage[BetaWorkspace]</a></code>
- <code title="post /v1/organizations/workspaces/{workspace_id}/archive?beta=true">client.beta.organization.workspaces.<a href="./src/anthropic/resources/beta/organization/workspaces/workspaces.py">archive</a>(workspace_id) -> <a href="./src/anthropic/types/beta/organization/beta_workspace.py">BetaWorkspace</a></code>

#### RateLimits

Types:

```python
from anthropic.types.beta.organization.workspaces import (
    BetaWorkspaceRateLimit,
    BetaWorkspaceRateLimitOrganizationSource,
    BetaWorkspaceRateLimitValue,
    BetaWorkspaceRateLimitWorkspaceSource,
)
```

Methods:

- <code title="get /v1/organizations/workspaces/{workspace_id}/rate_limits?beta=true">client.beta.organization.workspaces.rate_limits.<a href="./src/anthropic/resources/beta/organization/workspaces/rate_limits.py">list</a>(workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/rate_limit_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/workspaces/beta_workspace_rate_limit.py">SyncPageCursor[BetaWorkspaceRateLimit]</a></code>

#### Members

Types:

```python
from anthropic.types.beta.organization.workspaces import MemberRemoveResponse
```

Methods:

- <code title="get /v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true">client.beta.organization.workspaces.members.<a href="./src/anthropic/resources/beta/organization/workspaces/members.py">retrieve</a>(user_id, \*, workspace_id) -> <a href="./src/anthropic/types/beta/organization/beta_workspace_member.py">BetaWorkspaceMember</a></code>
- <code title="post /v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true">client.beta.organization.workspaces.members.<a href="./src/anthropic/resources/beta/organization/workspaces/members.py">update</a>(user_id, \*, workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/member_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_workspace_member.py">BetaWorkspaceMember</a></code>
- <code title="get /v1/organizations/workspaces/{workspace_id}/members?beta=true">client.beta.organization.workspaces.members.<a href="./src/anthropic/resources/beta/organization/workspaces/members.py">list</a>(workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/member_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_workspace_member.py">SyncPage[BetaWorkspaceMember]</a></code>
- <code title="post /v1/organizations/workspaces/{workspace_id}/members?beta=true">client.beta.organization.workspaces.members.<a href="./src/anthropic/resources/beta/organization/workspaces/members.py">add</a>(workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/member_add_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_workspace_member.py">BetaWorkspaceMember</a></code>
- <code title="delete /v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true">client.beta.organization.workspaces.members.<a href="./src/anthropic/resources/beta/organization/workspaces/members.py">remove</a>(user_id, \*, workspace_id) -> <a href="./src/anthropic/types/beta/organization/workspaces/member_remove_response.py">MemberRemoveResponse</a></code>

#### ServiceAccounts

Types:

```python
from anthropic.types.beta.organization.workspaces import ServiceAccountRemoveResponse
```

Methods:

- <code title="get /v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true">client.beta.organization.workspaces.service_accounts.<a href="./src/anthropic/resources/beta/organization/workspaces/service_accounts.py">retrieve</a>(service_account_id, \*, workspace_id) -> <a href="./src/anthropic/types/beta/organization/beta_service_account_workspace_member.py">BetaServiceAccountWorkspaceMember</a></code>
- <code title="post /v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true">client.beta.organization.workspaces.service_accounts.<a href="./src/anthropic/resources/beta/organization/workspaces/service_accounts.py">update</a>(service_account_id, \*, workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/service_account_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account_workspace_member.py">BetaServiceAccountWorkspaceMember</a></code>
- <code title="get /v1/organizations/workspaces/{workspace_id}/service_accounts?beta=true">client.beta.organization.workspaces.service_accounts.<a href="./src/anthropic/resources/beta/organization/workspaces/service_accounts.py">list</a>(workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/service_account_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account_workspace_member.py">SyncPageCursor[BetaServiceAccountWorkspaceMember]</a></code>
- <code title="post /v1/organizations/workspaces/{workspace_id}/service_accounts?beta=true">client.beta.organization.workspaces.service_accounts.<a href="./src/anthropic/resources/beta/organization/workspaces/service_accounts.py">add</a>(workspace_id, \*\*<a href="src/anthropic/types/beta/organization/workspaces/service_account_add_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_service_account_workspace_member.py">BetaServiceAccountWorkspaceMember</a></code>
- <code title="delete /v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true">client.beta.organization.workspaces.service_accounts.<a href="./src/anthropic/resources/beta/organization/workspaces/service_accounts.py">remove</a>(service_account_id, \*, workspace_id) -> <a href="./src/anthropic/types/beta/organization/workspaces/service_account_remove_response.py">ServiceAccountRemoveResponse</a></code>

### RateLimits

Types:

```python
from anthropic.types.beta.organization import (
    BetaOrganizationRateLimit,
    BetaOrganizationRateLimitBatchGroup,
    BetaOrganizationRateLimitFilesGroup,
    BetaOrganizationRateLimitModelGroup,
    BetaOrganizationRateLimitSkillsGroup,
    BetaOrganizationRateLimitTokenCountGroup,
    BetaOrganizationRateLimitValue,
    BetaOrganizationRateLimitWebSearchGroup,
)
```

Methods:

- <code title="get /v1/organizations/rate_limits?beta=true">client.beta.organization.rate_limits.<a href="./src/anthropic/resources/beta/organization/rate_limits.py">list</a>(\*\*<a href="src/anthropic/types/beta/organization/rate_limit_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_organization_rate_limit.py">SyncPageCursor[BetaOrganizationRateLimit]</a></code>

### ComplianceSettings

Types:

```python
from anthropic.types.beta.organization import (
    BetaComplianceSettings,
    BetaComplianceSettingsState,
    BetaComplianceSettingsStateDisabled,
    BetaComplianceSettingsStateDisabledParam,
    BetaComplianceSettingsStateEnabled,
    BetaComplianceSettingsStateEnabledParam,
    BetaComplianceSettingsStateParam,
)
```

Methods:

- <code title="get /v1/organizations/compliance_settings?beta=true">client.beta.organization.compliance_settings.<a href="./src/anthropic/resources/beta/organization/compliance_settings.py">retrieve</a>() -> <a href="./src/anthropic/types/beta/organization/beta_compliance_settings.py">BetaComplianceSettings</a></code>
- <code title="post /v1/organizations/compliance_settings?beta=true">client.beta.organization.compliance_settings.<a href="./src/anthropic/resources/beta/organization/compliance_settings.py">update</a>(\*\*<a href="src/anthropic/types/beta/organization/compliance_setting_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/organization/beta_compliance_settings.py">BetaComplianceSettings</a></code>
