fix(tools): look for ripgrep only in absolute `PATH` entries in the agent toolset's grep tool

The tool no longer runs an `rg` from a relative or empty `PATH` entry or, on Windows, from the current directory. On Windows it looks for `rg.exe`, so an `rg.cmd`, `rg.bat` or `rg.com` is no longer used. With no other `rg` on `PATH`, the tool uses its built-in search.
