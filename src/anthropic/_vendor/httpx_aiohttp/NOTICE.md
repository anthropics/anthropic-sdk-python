# httpx_aiohttp (vendored)

This directory contains a vendored copy of **httpx-aiohttp**, which provides the
aiohttp-backed transport behind this SDK's `DefaultAioHttpClient`.

- **Library:** httpx-aiohttp (<https://github.com/karpetrosyan/httpx-aiohttp>)
- **Version:** 0.2.0
- **Copyright:** © 2025, Karen Petrosyan
- **License:** BSD-3-Clause — full text in `LICENSE` in this directory
- **Source:** the `httpx2` variant only — `src/httpx_aiohttp/httpx2/{__init__,client,transport}.py`
  from the published `httpx_aiohttp-0.2.0.tar.gz` sdist
  (sha256 `d4796b981f04734f1d1db9b4d9326ea16bc994f126460b93b69036262cd4a9d8`).
  The upstream package's httpx-1.x variant is not vendored.
- **Integrity:** the copied files are byte-identical to that sdist apart from the
  attribution header added at the top of each —
  `__init__.py` sha256 `f1925ca049c372847b66b7842408ba7dd603751ccf07a3af97cc19e1f4a72aa5` (305 bytes),
  `client.py` sha256 `c7f6cb750732322ef8bbc18ae129d74076e45b0245ebfb09ce2425d2b1461fa8` (1,805 bytes),
  `transport.py` sha256 `d87ff5540bd66964700e29c1e69ca0c0cdef9780facf530c17050f22d564f93c` (7,109 bytes).
- **Modifications:** none to the code. Anthropic PBC added a provenance header to
  each file in 2026; no other change was made.

The code is vendored rather than depended on so the `aiohttp` extra resolves from
any package index. It is excluded from this SDK's own linting and type-checking
(see the `_vendor` entries in `pyproject.toml`) so it stays byte-comparable with
upstream. Do not edit these files by hand — re-copy from upstream to update.

Attribution here records provenance only. Nothing in this SDK is endorsed or
promoted by the authors of httpx-aiohttp.
