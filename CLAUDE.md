# Working in this repository

Context for contributors (human or AI) on how this SDK is put together, plus the things reviews most often come back to. Setup instructions live in [CONTRIBUTING.md](CONTRIBUTING.md).

## Overview

The official Python SDK for the Claude API (`anthropic` on PyPI). This is the v1 line: it is built on `httpx2` and needs Python 3.10 or later (`requires-python` in `pyproject.toml`).

Most of it is generated from the OpenAPI spec. Hand-written helpers, tool runners, credentials, middleware, and platform clients sit on top.

### Who owns which files

- **`src/anthropic/lib/`, `examples/`, and `tests/lib/` are hand-written.** The generator never touches them.
- **Everything else comes from the generator, with custom code mixed in.** Generated files carry no marker comment. Hand-written methods, imports, and whole blocks sit inside many of them, including core modules such as `_client.py` and `_base_client.py`. So a file's location doesn't tell you who owns a given line. The next section says how to tell.
- **`.stats.yml` and `.github/workflows` are generator-owned too.** Avoid editing them, because the next codegen push rewrites them and a change tends to conflict.
- **`src/anthropic/_vendor/` is vendored.** Re-copy it from upstream rather than editing it.
- **Release-please writes `src/anthropic/_version.py`, `.release-please-manifest.json`, and `CHANGELOG.md`.** It rewrites them in each release PR, so a manual edit is overwritten or conflicts with it.

### Editing generated files

- **Check whether a line is generated before you change it.** Every commit the generator produced carries a `Stainless-Generated-From: <sha>` trailer, and a hand-written commit has none. The SHA is the generator's own output for that commit, with no custom code in it.
  - Find the latest one with `git log -1 --grep='Stainless-Generated-From' --format='%(trailers:key=Stainless-Generated-From,valueonly)'`.
  - Fetch it with `git fetch origin <sha>`, then diff a file against it: `git diff <sha> -- src/anthropic/resources/messages/messages.py`.
  - Lines that appear only on your side are custom code. If the line you want to change is in the generated commit, the fix probably belongs in the generator (see below).
- **Where the lines go matters, not how many.** Edits to generated files survive regeneration, because new generator output is merged with them, but the merge can conflict.
  - Changing lines the generator writes, such as a method's parameters or the way it builds the request, is likely to conflict the next time the spec changes.
  - Adding lines of your own, such as a new method or a block inside a method body, is usually fine, even a large one. `AsyncWork.poller` and `AsyncWork.worker` in `resources/beta/environments/work.py` are whole methods added after the generated ones, with their `lib/` imports inside the method body.
- **No provenance comments.** Don't add a comment that marks code as hand-written or mentions Stainless, and remove one from a block you are already editing.
- **Fix generator-owned behaviour upstream.**
  - Broken generated plumbing (retries, SSE parsing, serialization) is a generator bug.
  - A real response the generated types can't parse is a spec bug.
  - The model name in `tests/api_resources/` comes from the spec's `example`.

### Branches

- **PRs target the repository's default branch.** In the public repository that is `main`. Elsewhere don't assume its name. `gh repo view --json defaultBranchRef` shows it.
- **Don't merge into `next`.** `next` is a release branch in the public repository, and only automation writes to it: release-please runs there and merges `next` into `main` at a release. Don't open a PR against `next`, and don't merge or push to it by hand.
- **An unreleased API feature has its own branch.** Hand-written work for that feature targets the feature's branch instead of the default branch. Those branches get force-pushed, so rebase with `git rebase --onto <new-base> <old-base-sha>`.

## Build, test, lint

The entry points are `./scripts/{bootstrap,format,lint,test}`. Always use them to format, lint, and run the tests, and pass pytest arguments through `./scripts/test`. They run through `uv`, but call `uv` yourself only to add a dependency or to run an ad hoc script, never to format, lint, or test.

| Script | What it does |
| --- | --- |
| `./scripts/lint` | Runs ruff, a dependency-cap check, pyright in strict mode, mypy, and an `import anthropic` smoke test. |
| `./scripts/format` | Runs `ruff format` and `ruff check --fix`, and formats the code blocks in `README.md` and `api.md`. |
| `./scripts/test` | Runs the suite. Starts a Steady mock server on port 4010 unless `TEST_API_BASE_URL` is set. |

### Test matrix

- **Python and Pydantic versions.** `./scripts/test` runs the suite on the oldest and newest supported Python under Pydantic v2, and again under Pydantic v1 on the oldest only, because Pydantic v1 doesn't support the newest. On the newest it also runs the MCP tests against `mcp>=2`. Set `UV_PYTHON` to run one version.
- **Code must work under Pydantic v1.** Read fields with `anthropic._compat.get_model_fields`, and route other v1/v2 differences through `_compat.py` or `_models.py`.
- **No live tests run by default.** Nothing in a default run calls a real endpoint. The tests that do are skipped, so set `ANTHROPIC_LIVE=1` when you want to run them.

### pytest

- **Warnings are errors.** pytest runs with `filterwarnings = error`, so a new warning fails the suite.
- **Snapshots need `-n0`.** The suite runs under xdist, so refresh snapshots with `./scripts/test --inline-snapshot=fix -n0`. Add `--http-record` to refresh HTTP snapshots.
- **`httpx` is aliased in tests only.** `tests/_alias_httpx.py` makes `import httpx` resolve to `httpx2` so that `respx` can mock the client. Everywhere else, write `import httpx2`. Only the vendored files alias it.

### Ruff

Ruff's `select` list is short.

- `T201` bans `print` outside `tests/`, `examples/`, `scripts/`, and `bin/`.
- `TID251` bans `functools.lru_cache`. Use `lru_cache` from `_utils`.
- A `noqa` for a rule that isn't selected does nothing, so don't add one.
- **Rarely silence a checker.** In this SDK a `# noqa`, `# pyright: ignore`, or `# type: ignore` usually means the code is doing something wrong. Fix the code or its types first. Suppress only when the checker is the one that is wrong, and follow the rules under Typing when you do.

### Dependencies

- **Extras are for users.** User-facing optional dependencies are extras under `[project.optional-dependencies]`. `[dependency-groups]` is for development only.
- **Missing extras raise a helpful error.** Code that needs an extra raises an error naming `pip install anthropic[<extra>]` (`MissingDependencyError`).

### Breaking changes

- **Anything importable without an underscore is public,** documented or not. So new modules, attributes, and parameters start private and are made public on purpose.
- **Don't make something public unless users need it.** Every public name has to be supported from then on. A helper, constant, or parameter stays private when only the SDK uses it, even if exposing it would be convenient.
- **Runtime behaviour is the contract.** A change only a type checker notices isn't breaking. A subtle change in what the code does at runtime is, even when every signature stays the same.
- **Keep old code working.** A rename or removal keeps an alias. A behaviour change users could depend on waits for a deprecation cycle or the next major. New implicit behaviour ships with a way to turn it off.
- **A major version is rare and a maintainer's call.** A small, technically breaking change doesn't warrant one. Describe the compatibility impact in the PR instead.

CI runs two checks. Both compare against a base: the `breaking-change-baseline` tag when the repository has one, otherwise `main`. With neither, the job skips.

- `scripts/detect-breaking-changes.py` flags public symbols removed since the base.
- `scripts/detect-breaking-changes` checks out the base's `tests/api_resources`, `tests/test_client.py`, and `tests/test_response.py`, then runs `./scripts/lint` to see whether the old tests still type-check against your branch.
- Neither sees a changed signature in a hand-written helper, so call that out yourself.

### Examples

Each example is a runnable script under `examples/` against a real backend.

- Use current model IDs.
- Read configuration from the environment.
- Stay on public API.
- Leave out debug prints and workarounds.

## Sync and async

- **Two classes, same shape.** Sync and async are separate classes: `Anthropic` and `AsyncAnthropic`, `BetaFunctionTool` and `BetaAsyncFunctionTool`. Don't write one function that checks `inspect.isawaitable` or a mode flag. Share the pure logic and write two thin wrappers.
- **A fix to one twin goes to the other.** The same holds for stable and beta: `lib/streaming/_messages.py` and `_beta_messages.py`, `resources/messages/` and `resources/beta/messages/`.
- **`create` has siblings.** Behaviour added to `create`, such as the `DEPRECATED_MODELS` warning, also goes on `stream`, `parse`, and `tool_runner`.
- **Async-only helpers live on the async class only.** A helper that only works async goes on the `Async*` resource only, as `AsyncWork.worker` does. Don't add a sync method that casts the client.
- **Use `anyio`, not `asyncio`.** Async helpers use `anyio`, including `anyio.Path` and `anyio.to_thread.run_sync`, so they work under any event loop the client supports. Don't call `asyncio` directly or block on `pathlib` I/O.

### Naming the async twin

- **Methods keep the sync name.** A method on an `Async*` class keeps the sync method's name: `AsyncAnthropic.close()`, not `aclose()`. Don't use the `a<name>` pattern.
- **`aclose` is for outside protocols.** It appears only where an outside protocol names it, such as `httpx2.AsyncByteStream`.
- **Functions get an `async_` prefix.** When a sync function and its async twin sit side by side, the twin is `async_<name>`, as `to_httpx_files` and `async_to_httpx_files` in `_files.py` are.

## Platform clients

- **Where they live.** Platform clients live in `lib/{aws,bedrock,vertex,google_cloud}/` and `lib/foundry.py`. A new one gets its own package with `_client.py` and an `__init__.py` that exports only the client classes.
- **Override `copy()`.** Each platform client overrides `copy()`, sets `with_options = copy`, and builds the copy with `self.__class__(...)`, or with `super().copy(...)`, which does the same, as `AnthropicAWS` does. This is how its own auth survives a copy. A new client or a new constructor argument needs the same treatment.
- **`_is_base_client()`** keeps subclasses of `Anthropic` (`AnthropicAWS`, `AnthropicFoundry`, `AnthropicGoogleCloud`) off the first-party credential chain, because they have their own auth.

### Auth and headers

- **Arguments beat environment variables.** An explicit constructor argument beats an environment variable. Read the variable only when the argument is `None`.
- **Bearer auth uses a scoped sub-client.** A helper that authenticates with a bearer token uses a scoped sub-client from `_copy_client_with_bearer_auth`, not per-call `extra_headers`.
- **Helper telemetry headers.**
  - `x-stainless-helper` values come from `helper_header("<tag>")`, whose `StainlessHelperHeaderValue` Literal is shared with the other SDKs.
  - Combine header layers with `merge_headers`, which appends helper tags instead of overwriting them.
  - New tags are hyphenated lowercase.
  - Don't rename an existing tag, because telemetry matches on it.
- **Beta headers are added at the method level.**
  - A method for a beta API adds that API's `anthropic-beta` value by default. It is joined with the caller's `betas`, and the caller's `extra_headers` override it.
  - A helper that uses a feature behind a beta adds the value the same way, merged with the caller's.
  - Don't opt the caller into a beta the call doesn't need, because a beta changes how the API behaves.
  - Bedrock copies `anthropic-beta` into the body as `anthropic_beta`.

## Code organization

### Layout

- **`src/anthropic/lib/` holds the hand-written code.** The helper packages are `streaming/`, `tools/`, `credentials/`, `environments/`, `middleware/`, `sessions/`, `_parse/`, and `_extras/`. The platform clients sit beside them. The shared modules are `_files.py`, `_retry.py`, `_scoped_client.py`, and `_stainless_helpers.py`.
- **Shared code goes in a shared module.** Code used by several tools goes in a module such as `lib/tools/_files.py`, not in a private class in one tool's file.
- **Order a file by importance.** The classes a reader came for go at the top, and small internal helpers go at the bottom.

### Public surface

- **Explicit `__init__.py` files.** A package `__init__.py` imports each public name explicitly, either re-exported as `from ._client import Foo as Foo` or listed in `__all__`, so the public surface is visible in review. Both forms are in use. Don't add star imports.
- **Re-export what users see.** Re-export every type that appears in a public signature. Keep internal helpers out of the public package.
- **One way to do each thing.** Don't add a second public function or parameter that does what an existing one already does.
- **Take the object, not its id.** When a helper needs data the caller already holds as an object, the parameter is that object. Taking only the id forces the helper to fetch the same thing again.
- **Don't remove or rename an exported symbol.** Users import it by name, so their import would fail. When something is renamed, keep the old name as an alias of the new one, as `UserLocation = UserLocationParam` does in `types/web_search_tool_20250305_param.py`.
- **Settle parameter names before a helper ships.** Keyword names are part of the public contract.
- **Retiring a parameter before a major version:**
  1. Keep it in the signature, and keep it working.
  2. Emit a `DeprecationWarning` when it's passed, with a `stacklevel` that points at the caller's line.
  3. Add a `@deprecated` overload, so type checkers flag the call too.
  4. Remove it at the next major and record the removal in `MIGRATION.md`.
- **Raise instead of warning only when the old behaviour can't be honoured at all.** `reject_unrestricted_paths` in `lib/tools/_deprecations.py` raises `TypeError`, because neither behaviour the flag used to choose between exists any more. The message says what to pass instead.

### Underscore prefixes

Underscore prefixes are for public modules only.

- **In a module users import from,** such as `lib/tools/mcp.py`, only the names that make up the public API are spelled without an underscore, and `__all__` lists them. Everything else defined at module level there gets a `_` prefix: helpers, constants, and TypeVars. Imported names are the exception and keep their own spelling.
- **In a file whose own name starts with `_`,** no function, class, or constant gets an underscore prefix, because the file name already marks it private. A second underscore adds nothing and makes pyright's `reportUnusedFunction` fire on helpers used from other modules.
- **TypeVars always keep the `_T` spelling.**

### Imports

- **Relative imports inside `src/anthropic`.** Always write `from ..._models import BaseModel`, never `from anthropic... import`.
- **Imports go at the top of the module.** A lazy import needs a comment saying why, for example that it keeps an optional or host-only dependency out of `import anthropic`.
- **Group imports from the parent package.**
  - Before writing several deep imports, one module per name (`from ...types.beta.beta_stop_reason import BetaStopReason`), check whether a parent package already re-exports the names.
  - If it does, import them together from there (`from ...types.beta import BetaMessage, BetaStopReason`). `types/` and `types/beta/` re-export almost every generated model and param.
  - Go deep only for a name the parent doesn't export, such as `ParsedBetaMessage`, or when importing the parent would create a cycle.

### Data and types

- **`BaseModel` everywhere, no dataclasses.** Structured data is a `BaseModel` from `anthropic._models` everywhere, internal-only records included. Don't use `@dataclass`.
- **`construct()` skips validation.** So don't write a lenient copy of a model to hold unvalidated data. Just use `BaseModel.construct()` instead.
- **Prefer generated types to hand-written copies.**
  - Derive lists from generated types and pin them with a tripwire test (see Tests), as `test_binary_media_types_track_generated_api_types` does.
  - A helper returns the concrete generated param type (`to_dict() -> BetaToolParam`), so a spec change becomes a type error.
- **Mark discriminated unions with `UnionDiscriminator`,** as the generated models do.

### Functions and methods

- **A function with one primary object is a method.** A function with one clear primary argument that is an instance of one of our classes is a method on that class: `tool.to_dict()`, not `tool_to_dict(tool)`.
- **Shared helpers go on the shared base.** A helper called only from classes that share a base is a private method on that base.
- **Build objects in `__init__`.** Logic that only ever builds one object goes in that object's `__init__`, not in a separate `resolve_*()` function, unless something rebuilds instances elsewhere. Less indirection is the point.

### Matching the other SDKs

- **Try to match the TypeScript and Go SDKs** on helper and option names, defaults, telemetry tags, model-visible strings, and environment variables.
- **Idiom wins over parity.** When parity and Python idiom conflict, idiom wins (a context manager over a `close` hook). Say so in the PR.
- **Keep it out of comments.** Don't write "matches the Go SDK" notes in code comments.

## Errors

### The hierarchy

`_exceptions.py` defines it.

- `AnthropicError` is the root.
- `APIStatusError` has one subclass per status and takes `.type` from the response body.
- `APIConnectionError` and `APITimeoutError` cover transport failures.
- Raising `RetryableError` opts a request into the retry policy.

### Raising

- **`AnthropicError` for SDK logic, builtins where plain Python would raise them.**
  - An error caused by logic specific to this SDK or the API is an `AnthropicError` subclass: credentials, a region, or a project that can't be resolved from the arguments, the environment, and cloud config, a failed token exchange, a missing extra.
  - An error that any Python library would raise the same way is the builtin: `TypeError` for an argument of the wrong type, `ValueError` for a value that is out of range or for arguments that can't be combined.
- **In-flight errors derive from `AnthropicError`.** That covers anything raised while a request is in flight: credential providers, auth flows, middleware, transports. The send loop wraps any other exception as `APIConnectionError`, which gets retried.
- **A family of errors gets its own subclass,** such as `WorkloadIdentityError`.
- **Repeated errors get named subclasses.** An error raised from more than one place gets a named subclass (of `ToolError` for tools), one per failure. Don't pair a message-format constant with a `make_error()` helper. A message used once can stay inline where it is raised.
- **Tools raise `ToolError`** for an expected failure. The runner sends it to the model as an `is_error` result.
- **Conflicting parameters raise, not warn.** A warning is easy to miss. Warn only when you are not also raising.
- **One message per failed check.** Include the actual value or type, so the reader can tell which check failed.

### Retrying and secrets

- **Catch `TRANSIENT_ERRORS`, not `Exception`.** Retry loops in helpers catch `TRANSIENT_ERRORS` from `lib/_retry.py`. Catching `Exception` would also retry programming errors.
- **Keep secrets out of exceptions, logs, and reprs.** Redact token-endpoint bodies with `_redact_body`, and hold tokens in `SecretStr`.

## Common mistakes

### Validation and safety

- **Validating what the API validates.** Let the server reject media types and lengths. If the client needs a cap for its own safety, make it configurable, as `AgentToolContext.max_image_base64_bytes` is. `None` is the only off-switch.
- **Working around a missing type checker.** Assume callers use one, so don't scatter runtime validation around. Don't quietly coerce a value the types already forbid, such as reading an explicit `None` as "unset" for a parameter whose type doesn't allow `None`. Drop the workaround. Where a wrong value would be a security problem, validate explicitly instead and reject anything unknown.
- **Failing open on unknown values.** A permission or security decision treats an unrecognized value as a denial. Data is different: accumulators match the event types they know and return everything else unchanged, as `lib/sessions/_accumulate.py` does.
- **Careless file I/O in tools.**
  - Read and write exact bytes.
  - Create files with `_FILE_CREATE_MODE` and directories with `_DIR_CREATE_MODE`. Memory files hold private data, and container umasks are often permissive.
  - Call `os.fsync(fd)`, not `os.sync()`.
  - In async paths, move blocking work to a thread with `run_sync`.

### Streaming accumulators

- **Merging a delta that replaces.** A field on `message_delta` replaces the snapshot's value whenever it is present, even as `[]`. Guard with `is not None`, not truthiness. A `signature_delta` also replaces.
- **Hand-listing fields with no tripwire.** `test_message_delta_fields_are_all_accumulated` and the `TRACKS_TOOL_INPUT` exhaustiveness test fail when codegen adds something the accumulator misses. Keep both the beta and stable versions passing, and add a tripwire for any new hand-written list (see Tests).

### Design

- **Matching the text of an error.** Never tell cases apart by matching text in a `TypeError` or any other exception. That text changes without notice.
- **Reading a signature when a type would do.** Prefer typing the input and branching on the type. Reading a callable's signature is sometimes needed for backwards compatibility, such as a callback written before a parameter existed, as `accepts_force_refresh` in `lib/credentials/_cache.py` does. Use `signature_without_evaluating_annotations` from `_utils` for it, not `inspect.signature`.
- **A parameter that does nothing on one path.** Don't expose it there. Callers will assume it works.
- **Defensive copies with no reason.** Check whether a copy is needed before making one. Keep it only when you can name the mutation it prevents, and pin that with a test.
- **Passing the subclass into `super().__init__()`.** To learn which members a subclass overrode, mark the base implementations with a small decorator or a private attribute and filter on that.

## Style notes

### Modern syntax and names

New code uses modern syntax and names.

- **Unions:** write `X | None` and `X | Y`, not `Optional[X]` or `Union[X, Y]`.
- **Generics:** write the builtins `list[str]`, `dict[str, Any]`, `tuple[int, ...]`, `set[str]`, and `type[T]`, not `List`, `Dict`, `Tuple`, `Set`, or `Type` from `typing`.
- **ABCs:** import `Iterable`, `Iterator`, `Callable`, `Mapping`, and the other ABCs from `collections.abc`.
- Don't churn existing code just to convert it.

### Typing

- **Use precise types.** Avoid `Any`, `object`, and `cast(Any, ...)` unless absolutely necessary. Describe an accepted shape with a Protocol.
- **Bound your TypeVars.** Give every TypeVar a `bound=` unless it is meant to be fully generic, like `_T`.
- **Exhaustive dispatch.** End the chain with `if TYPE_CHECKING: assert_never(x)`, so a new variant is a type error for us and does nothing at runtime. Don't call `assert_never` outside `TYPE_CHECKING`, because a value this SDK version doesn't know yet would then raise in the user's code. Use a tuple with `isinstance` for multi-type checks.
- **Suppressions name their rule** (`# pyright: ignore[reportX]`) and have an obvious reason. Don't add file-wide pyright pragmas.
- **`TYPE_CHECKING` imports are for real cycles.** Put an import under `TYPE_CHECKING`, or quote an annotation, only for a real import cycle or an optional dependency.
- **Backports over version gates.** Prefer `typing_extensions` backports to code gated on the Python version. A version gate is easy to miss when the floor moves.

### Classes

- **`BaseX`, not `XBase`.** Base classes are named like `BaseClient` and `BaseAPIResponse`.
- **Real abstract methods.** Declare an abstract member with `@abstractmethod`, not a body that raises `NotImplementedError`.
- **Public classes declare attribute types above `__init__`.** An internal class can just assign them in `__init__`.
- **Keyword-only constructors.** Constructors of internal helpers with several arguments are keyword-only, so arguments can't be swapped by position.

### Naming and helpers

- **Name things for what they mean,** not how they are built: `TRANSIENT_ERRORS`, not `RETRYABLE_EXCEPTION_TUPLE`.
- **Inline a helper that has one caller.** Keep one helper when the same logic appears twice.
- **Use the named constant.** A default that appears in a signature or docstring uses the named constant, not a copy of its value.

### Comments and docstrings

- **Write no comment by default.** When one is needed, keep it to a line or two stating a non-obvious why. Prefer a clearer name to a comment.
- **Docstrings use plain, complete sentences.**
- **Non-obvious attributes get a docstring.** An attribute whose use isn't obvious, such as a lock or a completion flag, gets a short `"""` docstring under it saying what it is for.
- **Document constructor arguments in `__init__`.** Put them in the `__init__` docstring, even when that repeats the class docstring, so that IDEs show them.
- **Link, don't name a file.** A docstring points users at a docs page or a file's GitHub URL, not at a bare repository file name such as `tools.md`.
- **Keep docs accurate.** Keep docstrings, `helpers.md`, and `tools.md` accurate when the API changes. Public docs are for users: call the package "Claude SDK for Python" and leave out internal layout.

### Markdown, not reStructuredText

Docstrings and comments are Markdown, to match the generated docstrings, which come from the Markdown descriptions in the OpenAPI spec.

- **Do:** put identifiers and literals in single backticks, examples in fenced code blocks, links as `[text](url)`, and arguments under an `Args:` heading.
- **Don't:** write reST roles (`:class:`, `:func:`, `:meth:`), double-backtick literals, `:param x:` fields, or directives such as `.. warning::`.
- Convert the reST in a docstring you are already editing. Don't churn the rest.

## Tests

### What to test

- **Fail before, pass after.** A behaviour change comes with a test that fails before it and passes after. Cover the negative branch too, so that a wrong implementation fails.
- **Cover every twin.** Cover the sync and async clients and the beta and stable modules.
- **One test per method, not a new file.** When a change adds the same support to several methods, extend one existing test per method. Don't add a new file that re-tests everything.

### Tripwire tests

A tripwire test asserts no behaviour. It compares a hand-written list with the generated type it was derived from, and goes red when the spec changes one without the other.

- **Required for anything hand-listed from generated code.** That covers the fields an accumulator folds, the union members a tuple tracks, and the literals a map covers. Without one, a new field or variant is dropped silently.
- **The failure says what to update.** Name the hand-written code to change in the assertion message or a comment, as `test_tracks_tool_input_type_alias_is_up_to_date` does.
- **The existing ones** are `test_message_delta_fields_are_all_accumulated` and `test_tracks_tool_input_type_alias_is_up_to_date`, each in a stable and a beta version, and `test_binary_media_types_track_generated_api_types`.
- **They are a stopgap.** The goal is for the generator to emit anything that depends on generated output, so that a spec change updates it directly. Each tripwire goes away once the generator produces the code it guards. Until then, write them.

### How to test

- **Go through the public API.** Mock HTTP with `respx` or an `httpx2.MockTransport`, and assert on the wire request and headers. Don't use `MagicMock` or call private methods, because those tests keep passing when the wire behaviour breaks.
- **Use the shared fixtures.** Use the `client` and `async_client` fixtures from `tests/conftest.py`. They point at `TEST_API_BASE_URL` and accept a strict-validation parameter. Build your own client only when the test needs specific client arguments.
- **Use pytest tools:** `monkeypatch.setenv`, `pytest.mark.parametrize`, and `pytest.mark.skipif`.
- **Streaming cases go in the fixture-based tests.** Add them to `tests/lib/streaming/`, which replays recorded responses from `fixtures/`. Don't start a new test file for them.

## Commits and pull requests

### Commits

- **Conventional Commits with a scope** drive release-please (`feat(tools):`, `fix(client):`, `chore(internal):`). The changelog sections drop untyped subjects.
- **User-visible changes get a changelog note,** even when they fix a bug. A different exception type is one such change.
- **Don't commit generator-owned files.** Don't commit `.stats.yml` or other generator-owned files from a feature branch. They conflict with the next codegen push.

### Pull requests

- **Target the default branch, never `next`.** The default branch is `main` in the public repository. See Branches.
- **One logical change per PR.** Unrelated fixes, formatting, and incidental `uv.lock` changes go elsewhere.
- **Port behaviour changes to the other SDKs,** and link the sibling PRs.
- **The description says:**
  - what was wrong, with a before-and-after example,
  - what changed,
  - how you know it works.
- **Call out** behaviour changes, wire-level changes, and cross-SDK divergence.
- **Keep it current.** Update the description when later commits change the scope.
