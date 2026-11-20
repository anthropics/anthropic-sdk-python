# Persistent memory with Loom

`AsyncLoomMemoryTool` implements the SDK's `BetaAsyncAbstractMemoryTool` interface. It stores memory files as documents in a self-hosted [Loom](https://github.com/ClickHouse/loom) server. The example passes it directly to `AsyncAnthropic.beta.messages.tool_runner`; it does not use an MCP connection or local memory files.

The standalone script uses Python 3.11+, `anthropic==2.11.0` and the `claude-memory` extra from [pinned Loom source](https://github.com/ClickHouse/loom/tree/8157a0415d8e8d1d072d87ddef9b8cde652fa6c7/sdk/python). That source declares `anthropic>=2.11,<2.12`. Run it with its inline dependencies. A direct Python 3.10 invocation exits with a version message before importing Loom.

## Configure

Use a Loom server and an existing token that can read and write knowledge documents in the selected organization and namespace. The adapter uses `knowledge.get`, `knowledge.list`, `knowledge.upsert` and `knowledge.bulk_delete`. Select a dedicated example namespace and store: Claude can create, modify, rename and delete documents in that store through the memory tool.

Set these variables in your shell without committing their values:

```sh
export LOOM_BASE_URL='https://your-loom-server.example'
export LOOM_ORG='your-org'
export LOOM_NAMESPACE='your-example-namespace'
export LOOM_MEMORY_STORE='preferences-demo'
export ANTHROPIC_MODEL='your-memory-tool-compatible-model'
read -r -s -p 'Loom token: ' LOOM_API_KEY; export LOOM_API_KEY; printf '\n'
read -r -s -p 'Anthropic API key: ' ANTHROPIC_API_KEY; export ANTHROPIC_API_KEY; printf '\n'
```

The token must authorize the selected scope; constructor values do not grant access. A store is a document grouping within a namespace, not a user authorization boundary. Use separately authorized namespaces for users who must not read each other's documents. Other callers authorized to read the same namespace may read these documents.

## Run two separate conversations

With [uv](https://docs.astral.sh/uv/) installed, run:

```sh
uv run --script examples/memory/loom_memory.py 'Remember that I prefer tea to coffee.'
uv run --script examples/memory/loom_memory.py 'Which drink do I prefer? Check your memory.'
```

Each command starts with a new message history. Reusing the server, namespace and store lets the second process read the first process's documents. Model tool selection is probabilistic: inspect the model's response and the stored document rather than assuming it wrote a file. Each invocation requests at most four model replies, with `max_tokens=1024` per reply. Reaching that limit can leave a request unfinished.

Both clients close when the asynchronous context exits. Documents remain on the server after the process ends. Delete only the example store's files through the memory tool when you no longer need them; this example does not automatically delete persisted data.

Requests use your Anthropic account and may incur API charges. Memory content returned by the tool is sent to Anthropic as tool results. Loom may also send ingested documents to the embedding or extraction providers configured by the server operator. Use synthetic data unless those processing arrangements are appropriate for your content.
