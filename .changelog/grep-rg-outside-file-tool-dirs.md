fix(tools): pass over an rg inside the directories the agent toolset's file tools can write

`grep` passes over an `rg` that resolves to somewhere inside `workdir` or `allowed_roots`, whatever the letter case of the names. It uses the next `rg` on `PATH`, or the built-in search when there is none. With a `workdir` that holds every `rg` on the host, such as `/`, every search is a built-in search. `rg` no longer gets the `ANTHROPIC_*` variables of the process, like the shell of `bash`.
