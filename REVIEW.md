# Review instructions

## Report these as Important, as well as functional bugs

- A violation of this repository's `CLAUDE.md`. Quote the rule
- A new public name, parameter or option that the PR description does not list
- A behavior change that still applies with the PR's feature switched off
- A client-side copy of validation that the API does
- A new runtime check of an API response, including a model's tool input, or a
  new runtime type check of input the caller's types cover, even in a language
  that doesn't enforce them, where the code could go on without it. A clearer
  error for a value that would fail anyway isn't a reason, and neither is being
  more idiomatic or more robust. This rule doesn't cover a null check on an
  optional value, a value that decides a security or permission question, a tool
  runner parsing a model's tool input into the tool's declared type, or reading
  into an error body that may not be an object, where that read would otherwise
  throw, though the fields it reads still pass through as-is
- Code that validates, reorders, defaults or drops part of a request the caller
  built
- Code that fails on an enum member, union variant or field this version does
  not know
- A fix made to one copy of logic that exists more than once
- A behavior change with no test that fails before it and passes after
- A hand-written list of fields, variants or names that generated code also
  carries, where a missed member would cause a bug, with no tripwire test
- A comment that restates the code, or that runs past three lines on a symbol
  that is not public

## Don't report these

- A missing runtime check of an API response, a missing runtime type check of
  input the caller's types cover, or missing client-side validation. Don't
  suggest one as an idiom or for robustness. The exceptions are a value that
  decides a security or permission question, and reading into an error body that
  may not be an object, where that read would otherwise throw, though the fields
  it reads still pass through as-is
- What an application can do to its own process, credentials or telemetry

## This repository's own rules

The generator writes the rest of this file. Rules for reviewing this
repository's hand-written code go in this section, and a change anywhere else in
the file belongs in the generator.

### Report these as Important, as well as functional bugs

- A new public method on `Messages` or `AsyncMessages` in
  `src/anthropic/resources/beta/messages/messages.py` that
  `src/anthropic/lib/bedrock/_beta_messages.py` or
  `src/anthropic/lib/vertex/_beta_messages.py` does not assign. An endpoint the
  platform does not serve may be left off
- A hand-written method that repeats a generated method's parameters, as
  `stream` and `parse` repeat `create`, with no `assert_signatures_in_sync` or
  `assert_overloads_in_sync` test
- Code that drops keys a model does not declare from tool input Claude wrote
- An `isinstance`, `None` or `callable` check for a case the value's type
  already rules out, where the diff widens the annotation or adds a
  `reportUnnecessaryIsInstance` or `reportUnnecessaryComparison` suppression to
  keep it, unless a wrong value would be a security problem
- A blocking subprocess, request-signing or credential-refresh call in an
  `async def`, outside `asyncify` (from `_utils`) or `anyio.to_thread.run_sync`
- A `TypeAlias`, plain assignment or empty `BaseModel` subclass that only
  renames an existing type, unless it keeps an old public name importable
- An error exported from `src/anthropic/tools/browser.py` or
  `src/anthropic/tools/computer.py` that is not specific to that toolset.
  `src/anthropic/tools/__init__.py` exports shared errors
- A `*Param(...)` constructor in a Markdown doc or `examples/`, where request
  params are dict literals
- Code that `./scripts/format` would change, such as missing blank lines between
  tests. CI does not check formatting

### Don't report these

- A platform client constructor argument left out of `copy()` when `__init__`
  only uses it to derive another argument, such as `base_url`
- `Args:` in an `__init__` docstring that repeats the async twin's `__init__`
- Keys a parsed model does not declare, which stay on the parsed object
- `from anthropic` in a docstring's example code
