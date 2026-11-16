chore(docs): note that a plugin scan's reason also covers errored scans

`content_scan.reason` on an errored scan now says why there is no verdict. It is not a security finding, so code that treats any `reason` as a concern should also check `status`.
