# Shared Types

```python
from anthropic.types import (
    APIErrorObject,
    AuthenticationError,
    BillingError,
    ErrorObject,
    ErrorResponse,
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
    Base64ImageSource,
    Base64PDFSource,
    CacheControlEphemeral,
    CacheCreation,
    CitationCharLocation,
    CitationCharLocationParam,
    CitationContentBlockLocation,
    CitationContentBlockLocationParam,
    CitationPageLocation,
    CitationPageLocationParam,
    CitationSearchResultLocationParam,
    CitationWebSearchResultLocationParam,
    CitationsConfigParam,
    CitationsDelta,
    CitationsSearchResultLocation,
    CitationsWebSearchResultLocation,
    ContentBlock,
    ContentBlockParam,
    ContentBlockSource,
    ContentBlockSourceContent,
    DocumentBlockParam,
    ImageBlockParam,
    InputJSONDelta,
    Message,
    MessageCountTokensTool,
    MessageDeltaUsage,
    MessageParam,
    MessageTokensCount,
    Metadata,
    Model,
    PlainTextSource,
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
    SearchResultBlockParam,
    ServerToolUsage,
    ServerToolUseBlock,
    ServerToolUseBlockParam,
    SignatureDelta,
    StopReason,
    TextBlock,
    TextBlockParam,
    TextCitation,
    TextCitationParam,
    TextDelta,
    ThinkingBlock,
    ThinkingBlockParam,
    ThinkingConfigDisabled,
    ThinkingConfigEnabled,
    ThinkingConfigParam,
    ThinkingDelta,
    Tool,
    ToolBash20250124,
    ToolChoice,
    ToolChoiceAny,
    ToolChoiceAuto,
    ToolChoiceNone,
    ToolChoiceTool,
    ToolResultBlockParam,
    ToolTextEditor20250124,
    ToolTextEditor20250429,
    ToolTextEditor20250728,
    ToolUnion,
    ToolUseBlock,
    ToolUseBlockParam,
    URLImageSource,
    URLPDFSource,
    Usage,
    WebSearchResultBlock,
    WebSearchResultBlockParam,
    WebSearchTool20250305,
    WebSearchToolRequestError,
    WebSearchToolResultBlock,
    WebSearchToolResultBlockContent,
    WebSearchToolResultBlockParam,
    WebSearchToolResultBlockParamContent,
    WebSearchToolResultError,
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
from anthropic.types import ModelInfo
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/anthropic/resources/models.py">retrieve</a>(model_id) -> <a href="./src/anthropic/types/model_info.py">ModelInfo</a></code>
- <code title="get /v1/models">client.models.<a href="./src/anthropic/resources/models.py">list</a>(\*\*<a href="src/anthropic/types/model_list_params.py">params</a>) -> <a href="./src/anthropic/types/model_info.py">SyncPage[ModelInfo]</a></code>

# Beta

Types:

```python
from anthropic.types import (
    AnthropicBeta,
    BetaAPIError,
    BetaAuthenticationError,
    BetaBillingError,
    BetaError,
    BetaErrorResponse,
    BetaGatewayTimeoutError,
    BetaInvalidRequestError,
    BetaNotFoundError,
    BetaOverloadedError,
    BetaPermissionError,
    BetaRateLimitError,
)
```

## Models

Types:

```python
from anthropic.types.beta import BetaModelInfo
```

Methods:

- <code title="get /v1/models/{model_id}?beta=true">client.beta.models.<a href="./src/anthropic/resources/beta/models.py">retrieve</a>(model_id) -> <a href="./src/anthropic/types/beta/beta_model_info.py">BetaModelInfo</a></code>
- <code title="get /v1/models?beta=true">client.beta.models.<a href="./src/anthropic/resources/beta/models.py">list</a>(\*\*<a href="src/anthropic/types/beta/model_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_model_info.py">SyncPage[BetaModelInfo]</a></code>

## Messages

Types:

```python
from anthropic.types.beta import (
    BetaAllThinkingTurns,
    BetaBase64ImageSource,
    BetaBase64PDFSource,
    BetaBashCodeExecutionOutputBlock,
    BetaBashCodeExecutionOutputBlockParam,
    BetaBashCodeExecutionResultBlock,
    BetaBashCodeExecutionResultBlockParam,
    BetaBashCodeExecutionToolResultBlock,
    BetaBashCodeExecutionToolResultBlockParam,
    BetaBashCodeExecutionToolResultError,
    BetaBashCodeExecutionToolResultErrorParam,
    BetaCacheControlEphemeral,
    BetaCacheCreation,
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
    BetaCitationsDelta,
    BetaCitationsWebSearchResultLocation,
    BetaClearThinking20251015Edit,
    BetaClearThinking20251015EditResponse,
    BetaClearToolUses20250919Edit,
    BetaClearToolUses20250919EditResponse,
    BetaCodeExecutionOutputBlock,
    BetaCodeExecutionOutputBlockParam,
    BetaCodeExecutionResultBlock,
    BetaCodeExecutionResultBlockParam,
    BetaCodeExecutionTool20250522,
    BetaCodeExecutionTool20250825,
    BetaCodeExecutionToolResultBlock,
    BetaCodeExecutionToolResultBlockContent,
    BetaCodeExecutionToolResultBlockParam,
    BetaCodeExecutionToolResultBlockParamContent,
    BetaCodeExecutionToolResultError,
    BetaCodeExecutionToolResultErrorCode,
    BetaCodeExecutionToolResultErrorParam,
    BetaContainer,
    BetaContainerParams,
    BetaContainerUploadBlock,
    BetaContainerUploadBlockParam,
    BetaContentBlock,
    BetaContentBlockParam,
    BetaContentBlockSource,
    BetaContentBlockSourceContent,
    BetaContextManagementConfig,
    BetaContextManagementResponse,
    BetaCountTokensContextManagementResponse,
    BetaDocumentBlock,
    BetaFileDocumentSource,
    BetaFileImageSource,
    BetaImageBlockParam,
    BetaInputJSONDelta,
    BetaInputTokensClearAtLeast,
    BetaInputTokensTrigger,
    BetaMCPToolResultBlock,
    BetaMCPToolUseBlock,
    BetaMCPToolUseBlockParam,
    BetaMemoryTool20250818,
    BetaMemoryTool20250818Command,
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
    BetaMemoryTool20250818ViewCommand,
    BetaMessage,
    BetaMessageDeltaUsage,
    BetaMessageParam,
    BetaMessageTokensCount,
    BetaMetadata,
    BetaPlainTextSource,
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
    BetaRequestDocumentBlock,
    BetaRequestMCPServerToolConfiguration,
    BetaRequestMCPServerURLDefinition,
    BetaRequestMCPToolResultBlockParam,
    BetaSearchResultBlockParam,
    BetaServerToolUsage,
    BetaServerToolUseBlock,
    BetaServerToolUseBlockParam,
    BetaSignatureDelta,
    BetaSkill,
    BetaSkillParams,
    BetaStopReason,
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
    BetaThinkingBlockParam,
    BetaThinkingConfigDisabled,
    BetaThinkingConfigEnabled,
    BetaThinkingConfigParam,
    BetaThinkingDelta,
    BetaThinkingTurns,
    BetaTool,
    BetaToolBash20241022,
    BetaToolBash20250124,
    BetaToolChoice,
    BetaToolChoiceAny,
    BetaToolChoiceAuto,
    BetaToolChoiceNone,
    BetaToolChoiceTool,
    BetaToolComputerUse20241022,
    BetaToolComputerUse20250124,
    BetaToolResultBlockParam,
    BetaToolTextEditor20241022,
    BetaToolTextEditor20250124,
    BetaToolTextEditor20250429,
    BetaToolTextEditor20250728,
    BetaToolUnion,
    BetaToolUseBlock,
    BetaToolUseBlockParam,
    BetaToolUsesKeep,
    BetaToolUsesTrigger,
    BetaURLImageSource,
    BetaURLPDFSource,
    BetaUsage,
    BetaWebFetchBlock,
    BetaWebFetchBlockParam,
    BetaWebFetchTool20250910,
    BetaWebFetchToolResultBlock,
    BetaWebFetchToolResultBlockParam,
    BetaWebFetchToolResultErrorBlock,
    BetaWebFetchToolResultErrorBlockParam,
    BetaWebFetchToolResultErrorCode,
    BetaWebSearchResultBlock,
    BetaWebSearchResultBlockParam,
    BetaWebSearchTool20250305,
    BetaWebSearchToolRequestError,
    BetaWebSearchToolResultBlock,
    BetaWebSearchToolResultBlockContent,
    BetaWebSearchToolResultBlockParam,
    BetaWebSearchToolResultBlockParamContent,
    BetaWebSearchToolResultError,
    BetaWebSearchToolResultErrorCode,
    BetaBase64PDFBlock,
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

## Files

Types:

```python
from anthropic.types.beta import DeletedFile, FileMetadata
```

Methods:

- <code title="get /v1/files?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">list</a>(\*\*<a href="src/anthropic/types/beta/file_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/file_metadata.py">SyncPage[FileMetadata]</a></code>
- <code title="delete /v1/files/{file_id}?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">delete</a>(file_id) -> <a href="./src/anthropic/types/beta/deleted_file.py">DeletedFile</a></code>
- <code title="get /v1/files/{file_id}/content?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">download</a>(file_id) -> BinaryAPIResponse</code>
- <code title="get /v1/files/{file_id}?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">retrieve_metadata</a>(file_id) -> <a href="./src/anthropic/types/beta/file_metadata.py">FileMetadata</a></code>
- <code title="post /v1/files?beta=true">client.beta.files.<a href="./src/anthropic/resources/beta/files.py">upload</a>(\*\*<a href="src/anthropic/types/beta/file_upload_params.py">params</a>) -> <a href="./src/anthropic/types/beta/file_metadata.py">FileMetadata</a></code>

## Skills

Types:

```python
from anthropic.types.beta import (
    SkillCreateResponse,
    SkillRetrieveResponse,
    SkillListResponse,
    SkillDeleteResponse,
)
```

Methods:

- <code title="post /v1/skills?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">create</a>(\*\*<a href="src/anthropic/types/beta/skill_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/skill_create_response.py">SkillCreateResponse</a></code>
- <code title="get /v1/skills/{skill_id}?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">retrieve</a>(skill_id) -> <a href="./src/anthropic/types/beta/skill_retrieve_response.py">SkillRetrieveResponse</a></code>
- <code title="get /v1/skills?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">list</a>(\*\*<a href="src/anthropic/types/beta/skill_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/skill_list_response.py">SyncPageCursor[SkillListResponse]</a></code>
- <code title="delete /v1/skills/{skill_id}?beta=true">client.beta.skills.<a href="./src/anthropic/resources/beta/skills/skills.py">delete</a>(skill_id) -> <a href="./src/anthropic/types/beta/skill_delete_response.py">SkillDeleteResponse</a></code>

### Versions

Types:

```python
from anthropic.types.beta.skills import (
    VersionCreateResponse,
    VersionRetrieveResponse,
    VersionListResponse,
    VersionDeleteResponse,
)
```

Methods:

- <code title="post /v1/skills/{skill_id}/versions?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">create</a>(skill_id, \*\*<a href="src/anthropic/types/beta/skills/version_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/skills/version_create_response.py">VersionCreateResponse</a></code>
- <code title="get /v1/skills/{skill_id}/versions/{version}?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">retrieve</a>(version, \*, skill_id) -> <a href="./src/anthropic/types/beta/skills/version_retrieve_response.py">VersionRetrieveResponse</a></code>
- <code title="get /v1/skills/{skill_id}/versions?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">list</a>(skill_id, \*\*<a href="src/anthropic/types/beta/skills/version_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/skills/version_list_response.py">SyncPageCursor[VersionListResponse]</a></code>
- <code title="delete /v1/skills/{skill_id}/versions/{version}?beta=true">client.beta.skills.versions.<a href="./src/anthropic/resources/beta/skills/versions.py">delete</a>(version, \*, skill_id) -> <a href="./src/anthropic/types/beta/skills/version_delete_response.py">VersionDeleteResponse</a></code>
