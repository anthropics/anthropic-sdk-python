fix(tools): read only regular files in the grep tool's built-in search

The built-in search of `grep` passes over a FIFO or a device in the directory it walks, as ripgrep does. Reading one could block the search, and the event loop with it, forever.
