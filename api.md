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
    Base64ImageSource,
    Base64PDFSource,
    BashCodeExecutionOutputBlock,
    BashCodeExecutionOutputBlockParam,
    BashCodeExecutionResultBlock,
    BashCodeExecutionResultBlockParam,
    BashCodeExecutionToolResultBlock,
    BashCodeExecutionToolResultBlockParam,
    BashCodeExecutionToolResultError,
    BashCodeExecutionToolResultErrorCode,
    BashCodeExecutionToolResultErrorParam,
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
    CitationsConfig,
    CitationsConfigParam,
    CitationsDelta,
    CitationsSearchResultLocation,
    CitationsWebSearchResultLocation,
    CodeExecutionOutputBlock,
    CodeExecutionOutputBlockParam,
    CodeExecutionResultBlock,
    CodeExecutionResultBlockParam,
    CodeExecutionTool20250522,
    CodeExecutionTool20250825,
    CodeExecutionTool20260120,
    CodeExecutionToolResultBlock,
    CodeExecutionToolResultBlockContent,
    CodeExecutionToolResultBlockParam,
    CodeExecutionToolResultBlockParamContent,
    CodeExecutionToolResultError,
    CodeExecutionToolResultErrorCode,
    CodeExecutionToolResultErrorParam,
    Container,
    ContainerUploadBlock,
    ContainerUploadBlockParam,
    ContentBlock,
    ContentBlockParam,
    ContentBlockSource,
    ContentBlockSourceContent,
    DirectCaller,
    DocumentBlock,
    DocumentBlockParam,
    EncryptedCodeExecutionResultBlock,
    EncryptedCodeExecutionResultBlockParam,
    ImageBlockParam,
    InputJSONDelta,
    JSONOutputFormat,
    MemoryTool20250818,
    Message,
    MessageCountTokensTool,
    MessageDeltaUsage,
    MessageParam,
    MessageTokensCount,
    Metadata,
    Model,
    OutputConfig,
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
    RefusalStopDetails,
    SearchResultBlockParam,
    ServerToolCaller,
    ServerToolCaller20260120,
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
    ThinkingConfigAdaptive,
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
    ToolReferenceBlock,
    ToolReferenceBlockParam,
    ToolResultBlockParam,
    ToolSearchToolBm25_20251119,
    ToolSearchToolRegex20251119,
    ToolSearchToolResultBlock,
    ToolSearchToolResultBlockParam,
    ToolSearchToolResultError,
    ToolSearchToolResultErrorCode,
    ToolSearchToolResultErrorParam,
    ToolSearchToolSearchResultBlock,
    ToolSearchToolSearchResultBlockParam,
    ToolTextEditor20250124,
    ToolTextEditor20250429,
    ToolTextEditor20250728,
    ToolUnion,
    ToolUseBlock,
    ToolUseBlockParam,
    URLImageSource,
    URLPDFSource,
    Usage,
    UserLocation,
    WebFetchBlock,
    WebFetchBlockParam,
    WebFetchTool20250910,
    WebFetchTool20260209,
    WebFetchTool20260309,
    WebFetchToolResultBlock,
    WebFetchToolResultBlockParam,
    WebFetchToolResultErrorBlock,
    WebFetchToolResultErrorBlockParam,
    WebFetchToolResultErrorCode,
    WebSearchResultBlock,
    WebSearchResultBlockParam,
    WebSearchTool20250305,
    WebSearchTool20260209,
    WebSearchToolRequestError,
    WebSearchToolResultBlock,
    WebSearchToolResultBlockContent,
    WebSearchToolResultBlockParam,
    WebSearchToolResultBlockParamContent,
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
from anthropic.types.beta import (
    BetaCapabilitySupport,
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
    BetaAdvisorToolResultBlock,
    BetaAdvisorToolResultBlockParam,
    BetaAdvisorToolResultError,
    BetaAdvisorToolResultErrorParam,
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
    BetaCodeExecutionTool20260120,
    BetaCodeExecutionToolResultBlock,
    BetaCodeExecutionToolResultBlockContent,
    BetaCodeExecutionToolResultBlockParam,
    BetaCodeExecutionToolResultBlockParamContent,
    BetaCodeExecutionToolResultError,
    BetaCodeExecutionToolResultErrorCode,
    BetaCodeExecutionToolResultErrorParam,
    BetaCompact20260112Edit,
    BetaCompactionBlock,
    BetaCompactionBlockParam,
    BetaCompactionContentBlockDelta,
    BetaCompactionIterationUsage,
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
    BetaDirectCaller,
    BetaDocumentBlock,
    BetaEncryptedCodeExecutionResultBlock,
    BetaEncryptedCodeExecutionResultBlockParam,
    BetaFileDocumentSource,
    BetaFileImageSource,
    BetaImageBlockParam,
    BetaInputJSONDelta,
    BetaInputTokensClearAtLeast,
    BetaInputTokensTrigger,
    BetaIterationsUsage,
    BetaJSONOutputFormat,
    BetaMCPToolConfig,
    BetaMCPToolDefaultConfig,
    BetaMCPToolResultBlock,
    BetaMCPToolUseBlock,
    BetaMCPToolUseBlockParam,
    BetaMCPToolset,
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
    BetaMessageIterationUsage,
    BetaMessageParam,
    BetaMessageTokensCount,
    BetaMetadata,
    BetaOutputConfig,
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
    BetaRefusalStopDetails,
    BetaRequestDocumentBlock,
    BetaRequestMCPServerToolConfiguration,
    BetaRequestMCPServerURLDefinition,
    BetaRequestMCPToolResultBlockParam,
    BetaSearchResultBlockParam,
    BetaServerToolCaller,
    BetaServerToolCaller20260120,
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
    BetaThinkingConfigAdaptive,
    BetaThinkingConfigDisabled,
    BetaThinkingConfigEnabled,
    BetaThinkingConfigParam,
    BetaThinkingDelta,
    BetaThinkingTurns,
    BetaTokenTaskBudget,
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
    BetaToolComputerUse20251124,
    BetaToolReferenceBlock,
    BetaToolReferenceBlockParam,
    BetaToolResultBlockParam,
    BetaToolSearchToolBm25_20251119,
    BetaToolSearchToolRegex20251119,
    BetaToolSearchToolResultBlock,
    BetaToolSearchToolResultBlockParam,
    BetaToolSearchToolResultError,
    BetaToolSearchToolResultErrorParam,
    BetaToolSearchToolSearchResultBlock,
    BetaToolSearchToolSearchResultBlockParam,
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
    BetaUserLocation,
    BetaWebFetchBlock,
    BetaWebFetchBlockParam,
    BetaWebFetchTool20250910,
    BetaWebFetchTool20260209,
    BetaWebFetchTool20260309,
    BetaWebFetchToolResultBlock,
    BetaWebFetchToolResultBlockParam,
    BetaWebFetchToolResultErrorBlock,
    BetaWebFetchToolResultErrorBlockParam,
    BetaWebFetchToolResultErrorCode,
    BetaWebSearchResultBlock,
    BetaWebSearchResultBlockParam,
    BetaWebSearchTool20250305,
    BetaWebSearchTool20260209,
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

## Agents

Types:

```python
from anthropic.types.beta import (
    BetaManagedAgentsAgent,
    BetaManagedAgentsAgentReference,
    BetaManagedAgentsAgentToolConfig,
    BetaManagedAgentsAgentToolConfigParams,
    BetaManagedAgentsAgentToolsetDefaultConfig,
    BetaManagedAgentsAgentToolsetDefaultConfigParams,
    BetaManagedAgentsAgentToolset20260401,
    BetaManagedAgentsAgentToolset20260401Params,
    BetaManagedAgentsAlwaysAllowPolicy,
    BetaManagedAgentsAlwaysAskPolicy,
    BetaManagedAgentsAnthropicSkill,
    BetaManagedAgentsAnthropicSkillParams,
    BetaManagedAgentsCustomSkill,
    BetaManagedAgentsCustomSkillParams,
    BetaManagedAgentsCustomTool,
    BetaManagedAgentsCustomToolInputSchema,
    BetaManagedAgentsCustomToolParams,
    BetaManagedAgentsMCPServerURLDefinition,
    BetaManagedAgentsMCPToolConfig,
    BetaManagedAgentsMCPToolConfigParams,
    BetaManagedAgentsMCPToolset,
    BetaManagedAgentsMCPToolsetDefaultConfig,
    BetaManagedAgentsMCPToolsetDefaultConfigParams,
    BetaManagedAgentsMCPToolsetParams,
    BetaManagedAgentsModel,
    BetaManagedAgentsModelConfig,
    BetaManagedAgentsModelConfigParams,
    BetaManagedAgentsMultiagentCoordinator,
    BetaManagedAgentsMultiagentCoordinatorParams,
    BetaManagedAgentsMultiagentSelfParams,
    BetaManagedAgentsSkillParams,
    BetaManagedAgentsURLMCPServerParams,
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
    BetaUnrestrictedNetwork,
)
```

Methods:

- <code title="post /v1/environments?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments.py">create</a>(\*\*<a href="src/anthropic/types/beta/environment_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>
- <code title="get /v1/environments/{environment_id}?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments.py">retrieve</a>(environment_id) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>
- <code title="post /v1/environments/{environment_id}?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments.py">update</a>(environment_id, \*\*<a href="src/anthropic/types/beta/environment_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>
- <code title="get /v1/environments?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments.py">list</a>(\*\*<a href="src/anthropic/types/beta/environment_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_environment.py">SyncPageCursor[BetaEnvironment]</a></code>
- <code title="delete /v1/environments/{environment_id}?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments.py">delete</a>(environment_id) -> <a href="./src/anthropic/types/beta/beta_environment_delete_response.py">BetaEnvironmentDeleteResponse</a></code>
- <code title="post /v1/environments/{environment_id}/archive?beta=true">client.beta.environments.<a href="./src/anthropic/resources/beta/environments.py">archive</a>(environment_id) -> <a href="./src/anthropic/types/beta/beta_environment.py">BetaEnvironment</a></code>

## Sessions

Types:

```python
from anthropic.types.beta import (
    BetaManagedAgentsAgentParams,
    BetaManagedAgentsBranchCheckout,
    BetaManagedAgentsCacheCreationUsage,
    BetaManagedAgentsCommitCheckout,
    BetaManagedAgentsDeletedSession,
    BetaManagedAgentsFileResourceParams,
    BetaManagedAgentsGitHubRepositoryResourceParams,
    BetaManagedAgentsMemoryStoreResourceParam,
    BetaManagedAgentsMultiagent,
    BetaManagedAgentsMultiagentParams,
    BetaManagedAgentsMultiagentRosterEntryParams,
    BetaManagedAgentsOutcomeEvaluationResource,
    BetaManagedAgentsSession,
    BetaManagedAgentsSessionAgent,
    BetaManagedAgentsSessionMultiagentCoordinator,
    BetaManagedAgentsSessionStats,
    BetaManagedAgentsSessionUsage,
)
```

Methods:

- <code title="post /v1/sessions?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">create</a>(\*\*<a href="src/anthropic/types/beta/session_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>
- <code title="get /v1/sessions/{session_id}?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">retrieve</a>(session_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>
- <code title="post /v1/sessions/{session_id}?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">update</a>(session_id, \*\*<a href="src/anthropic/types/beta/session_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>
- <code title="get /v1/sessions?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">list</a>(\*\*<a href="src/anthropic/types/beta/session_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">SyncPageCursor[BetaManagedAgentsSession]</a></code>
- <code title="delete /v1/sessions/{session_id}?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">delete</a>(session_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_deleted_session.py">BetaManagedAgentsDeletedSession</a></code>
- <code title="post /v1/sessions/{session_id}/archive?beta=true">client.beta.sessions.<a href="./src/anthropic/resources/beta/sessions/sessions.py">archive</a>(session_id) -> <a href="./src/anthropic/types/beta/beta_managed_agents_session.py">BetaManagedAgentsSession</a></code>

### Events

Types:

```python
from anthropic.types.beta.sessions import (
    BetaManagedAgentsAgentCustomToolUseEvent,
    BetaManagedAgentsAgentMCPToolResultEvent,
    BetaManagedAgentsAgentMCPToolUseEvent,
    BetaManagedAgentsAgentMessageEvent,
    BetaManagedAgentsAgentThinkingEvent,
    BetaManagedAgentsAgentThreadContextCompactedEvent,
    BetaManagedAgentsAgentThreadMessageReceivedEvent,
    BetaManagedAgentsAgentThreadMessageSentEvent,
    BetaManagedAgentsAgentToolResultEvent,
    BetaManagedAgentsAgentToolUseEvent,
    BetaManagedAgentsBase64DocumentSource,
    BetaManagedAgentsBase64ImageSource,
    BetaManagedAgentsBillingError,
    BetaManagedAgentsDocumentBlock,
    BetaManagedAgentsEventParams,
    BetaManagedAgentsFileDocumentSource,
    BetaManagedAgentsFileImageSource,
    BetaManagedAgentsFileRubric,
    BetaManagedAgentsFileRubricParams,
    BetaManagedAgentsImageBlock,
    BetaManagedAgentsMCPAuthenticationFailedError,
    BetaManagedAgentsMCPConnectionFailedError,
    BetaManagedAgentsModelOverloadedError,
    BetaManagedAgentsModelRateLimitedError,
    BetaManagedAgentsModelRequestFailedError,
    BetaManagedAgentsPlainTextDocumentSource,
    BetaManagedAgentsRetryStatusExhausted,
    BetaManagedAgentsRetryStatusRetrying,
    BetaManagedAgentsRetryStatusTerminal,
    BetaManagedAgentsSendSessionEvents,
    BetaManagedAgentsSessionDeletedEvent,
    BetaManagedAgentsSessionEndTurn,
    BetaManagedAgentsSessionErrorEvent,
    BetaManagedAgentsSessionEvent,
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
    BetaManagedAgentsSpanModelRequestEndEvent,
    BetaManagedAgentsSpanModelRequestStartEvent,
    BetaManagedAgentsSpanModelUsage,
    BetaManagedAgentsSpanOutcomeEvaluationEndEvent,
    BetaManagedAgentsSpanOutcomeEvaluationOngoingEvent,
    BetaManagedAgentsSpanOutcomeEvaluationStartEvent,
    BetaManagedAgentsStreamSessionEvents,
    BetaManagedAgentsTextBlock,
    BetaManagedAgentsTextRubric,
    BetaManagedAgentsTextRubricParams,
    BetaManagedAgentsUnknownError,
    BetaManagedAgentsURLDocumentSource,
    BetaManagedAgentsURLImageSource,
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
)
```

Methods:

- <code title="get /v1/sessions/{session_id}/events?beta=true">client.beta.sessions.events.<a href="./src/anthropic/resources/beta/sessions/events.py">list</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/event_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_session_event.py">SyncPageCursor[BetaManagedAgentsSessionEvent]</a></code>
- <code title="post /v1/sessions/{session_id}/events?beta=true">client.beta.sessions.events.<a href="./src/anthropic/resources/beta/sessions/events.py">send</a>(session_id, \*\*<a href="src/anthropic/types/beta/sessions/event_send_params.py">params</a>) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_send_session_events.py">BetaManagedAgentsSendSessionEvents</a></code>
- <code title="get /v1/sessions/{session_id}/events/stream?beta=true">client.beta.sessions.events.<a href="./src/anthropic/resources/beta/sessions/events.py">stream</a>(session_id) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_stream_session_events.py">BetaManagedAgentsStreamSessionEvents</a></code>

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
    BetaManagedAgentsSessionThreadAgent,
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
- <code title="get /v1/sessions/{session_id}/threads/{thread_id}/stream?beta=true">client.beta.sessions.threads.events.<a href="./src/anthropic/resources/beta/sessions/threads/events.py">stream</a>(thread_id, \*, session_id) -> <a href="./src/anthropic/types/beta/sessions/beta_managed_agents_stream_session_thread_events.py">BetaManagedAgentsStreamSessionThreadEvents</a></code>

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
    BetaManagedAgentsCredentialValidation,
    BetaManagedAgentsCredentialValidationStatus,
    BetaManagedAgentsDeletedCredential,
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
    BetaManagedAgentsConflictError,
    BetaManagedAgentsContentSha256Precondition,
    BetaManagedAgentsDeletedMemory,
    BetaManagedAgentsError,
    BetaManagedAgentsMemory,
    BetaManagedAgentsMemoryListItem,
    BetaManagedAgentsMemoryPathConflictError,
    BetaManagedAgentsMemoryPreconditionFailedError,
    BetaManagedAgentsMemoryPrefix,
    BetaManagedAgentsMemoryView,
    BetaManagedAgentsPrecondition,
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
from anthropic.types.beta import BetaFileScope, DeletedFile, FileMetadata
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

## Webhooks

Types:

```python
from anthropic.types.beta import (
    BetaWebhookEvent,
    BetaWebhookEventData,
    BetaWebhookSessionArchivedEventData,
    BetaWebhookSessionCreatedEventData,
    BetaWebhookSessionDeletedEventData,
    BetaWebhookSessionIdledEventData,
    BetaWebhookSessionOutcomeEvaluationEndedEventData,
    BetaWebhookSessionPendingEventData,
    BetaWebhookSessionRequiresActionEventData,
    BetaWebhookSessionRunningEventData,
    BetaWebhookSessionStatusIdledEventData,
    BetaWebhookSessionStatusRunStartedEventData,
    BetaWebhookSessionStatusScheduledEventData,
    BetaWebhookSessionStatusTerminatedEventData,
    BetaWebhookSessionThreadCreatedEventData,
    BetaWebhookSessionThreadIdledEventData,
    BetaWebhookSessionThreadTerminatedEventData,
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
    BetaUserProfileTrustGrant,
)
```

Methods:

- <code title="post /v1/user_profiles?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">create</a>(\*\*<a href="src/anthropic/types/beta/user_profile_create_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">BetaUserProfile</a></code>
- <code title="get /v1/user_profiles/{user_profile_id}?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">retrieve</a>(user_profile_id) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">BetaUserProfile</a></code>
- <code title="post /v1/user_profiles/{user_profile_id}?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">update</a>(user_profile_id, \*\*<a href="src/anthropic/types/beta/user_profile_update_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">BetaUserProfile</a></code>
- <code title="get /v1/user_profiles?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">list</a>(\*\*<a href="src/anthropic/types/beta/user_profile_list_params.py">params</a>) -> <a href="./src/anthropic/types/beta/beta_user_profile.py">SyncPageCursor[BetaUserProfile]</a></code>
- <code title="post /v1/user_profiles/{user_profile_id}/enrollment_url?beta=true">client.beta.user_profiles.<a href="./src/anthropic/resources/beta/user_profiles.py">create_enrollment_url</a>(user_profile_id) -> <a href="./src/anthropic/types/beta/beta_user_profile_enrollment_url.py">BetaUserProfileEnrollmentURL</a></code>
