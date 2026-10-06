# Review instructions

## Report these as Important, as well as functional bugs

- A violation of this repository's `CLAUDE.md`. Quote the rule
- A new public name, parameter or option that the PR description does not list
- A behavior change that still applies with the PR's feature switched off
- A new runtime check of an API response, or a client-side copy of validation
  that the API does
- Code that validates, reorders, defaults or drops part of a request the caller
  built
- Code that fails on an enum member, union variant or field this version does
  not know
- A fix made to one copy of logic that exists more than once
- A behavior change with no test that fails before it and passes after
- A hand-written list of fields, variants or names that generated code also
  carries, with no tripwire test
- A comment that restates the code, or that runs past three lines on a symbol
  that is not public

## Don't report these

- A missing runtime check of an API response, or missing client-side validation
- What an application can do to its own process, credentials or telemetry
