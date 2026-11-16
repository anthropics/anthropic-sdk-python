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
- **Integrity:** the hashes of the files in that sdist are
  `__init__.py` sha256 `f1925ca049c372847b66b7842408ba7dd603751ccf07a3af97cc19e1f4a72aa5` (305 bytes),
  `client.py` sha256 `c7f6cb750732322ef8bbc18ae129d74076e45b0245ebfb09ce2425d2b1461fa8` (1,805 bytes),
  `transport.py` sha256 `d87ff5540bd66964700e29c1e69ca0c0cdef9780facf530c17050f22d564f93c` (7,109 bytes).
  Below the header added at the top of each, `__init__.py` and `client.py` are
  byte-identical to them, and `transport.py` differs only as listed under
  Modifications.
- **Modifications:** Anthropic PBC added a provenance header to each file in 2026,
  and changed two entries of `AIOHTTP_EXC_MAP` in `transport.py`, so that a
  connection that fails without timing out is not reported as a timeout:
  - `aiohttp.ClientConnectionError` maps to `httpx.ConnectError` (upstream:
    `httpx.ConnectTimeout`).
  - `aiohttp.ConnectionTimeoutError` maps to `httpx.ConnectTimeout` (upstream has no
    entry), so that a connect timeout keeps the type upstream gives it.

The code is vendored rather than depended on so the `aiohttp` extra resolves from
any package index. It is excluded from this SDK's own linting and type-checking
(see the `_vendor` entries in `pyproject.toml`) so it stays easy to compare with
upstream. To update, re-copy from upstream and re-apply any modification above
that upstream still lacks. Record any other edit under Modifications.

Attribution here records provenance only. Nothing in this SDK is endorsed or
promoted by the authors of httpx-aiohttp.
