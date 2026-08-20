# Vendored from httpx-aiohttp v0.2.0 (BSD-3-Clause), src/httpx_aiohttp/httpx2/client.py.
# Copyright (c) 2025, Karen Petrosyan. Licence text and provenance: LICENSE and
# NOTICE.md in this directory.
# The code below is verbatim; only this header was added, by Anthropic PBC (2026).
# Do not edit by hand; re-copy from upstream to update.
from __future__ import annotations

import ssl
import typing as t

import httpx2 as httpx

SOCKET_OPTION = t.Union[
    t.Tuple[int, int, int],
    t.Tuple[int, int, t.Union[bytes, bytearray]],
    t.Tuple[int, int, None, int],
]


class Httpx2AiohttpClient(httpx.AsyncClient):
    def _init_transport(
        self,
        verify: ssl.SSLContext | str | bool = True,
        cert: t.Union[str, t.Tuple[str, str], t.Tuple[str, str, str], None] = None,
        trust_env: bool = True,
        http1: bool = True,
        http2: bool = False,
        limits: httpx.Limits = httpx.Limits(max_connections=100, max_keepalive_connections=20),
        transport: httpx.AsyncBaseTransport | None = None,
        **kwargs: t.Any,
    ) -> httpx.AsyncBaseTransport:
        from .transport import AiohttpTransport

        if transport is not None:
            return transport

        return AiohttpTransport(
            verify=verify,
            cert=cert,
            trust_env=trust_env,
            http1=http1,
            http2=http2,
            limits=limits,
        )

    def _init_proxy_transport(
        self,
        proxy: httpx.Proxy,
        verify: ssl.SSLContext | str | bool = True,
        cert: t.Union[str, t.Tuple[str, str], t.Tuple[str, str, str], None] = None,
        trust_env: bool = True,
        http1: bool = True,
        http2: bool = False,
        limits: httpx.Limits = httpx.Limits(max_connections=100, max_keepalive_connections=20),
        **kwargs: t.Any,
    ) -> httpx.AsyncBaseTransport:
        from .transport import AiohttpTransport

        return AiohttpTransport(
            verify=verify,
            cert=cert,
            trust_env=trust_env,
            http1=http1,
            http2=http2,
            limits=limits,
            proxy=proxy,
        )
