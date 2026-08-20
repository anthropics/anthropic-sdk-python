# Vendored from httpx-aiohttp v0.2.0 (BSD-3-Clause), src/httpx_aiohttp/httpx2/__init__.py.
# Copyright (c) 2025, Karen Petrosyan. Licence text and provenance: LICENSE and
# NOTICE.md in this directory.
# The code below is verbatim; only this header was added, by Anthropic PBC (2026).
# Do not edit by hand; re-copy from upstream to update.
"""Variant of httpx_aiohttp for `httpx2 <https://github.com/pydantic/httpx2>`_.

Requires the optional ``httpx2`` dependency: ``pip install httpx-aiohttp[httpx2]``.
"""

from .client import Httpx2AiohttpClient
from .transport import AiohttpTransport

__all__ = ["AiohttpTransport", "Httpx2AiohttpClient"]
