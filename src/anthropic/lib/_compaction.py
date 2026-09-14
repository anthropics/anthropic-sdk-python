"""Request-side handling of compaction content blocks.

Response compaction blocks include ``encrypted_content``, but the Messages API
rejects that field on request blocks (``Extra inputs are not permitted``). The
documented round-trip is ``messages.append(response.content)``, so the SDK
omits ``encrypted_content`` from compaction blocks while serializing requests.

This module is not Stainless-generated; keep request-only behavior here so it
survives OpenAPI regenerations of the TypedDicts.
"""

from __future__ import annotations

from typing import Any, TypeVar, cast

_T = TypeVar("_T")


def omit_compaction_encrypted_content(data: _T) -> _T:
    """Drop ``encrypted_content`` from compaction blocks in a request payload.

    Other block types that legitimately send ``encrypted_content`` (web search
    results, advisor redacted results) are left unchanged. Objects that do not
    contain a compaction block are returned unchanged so request transform
    identity optimizations keep working.
    """
    return cast(_T, _omit_compaction_encrypted_content(data))


def _omit_compaction_encrypted_content(data: object) -> Any:
    if isinstance(data, list):
        items = cast("list[object]", data)
        new_items: list[object] = [_omit_compaction_encrypted_content(item) for item in items]
        if all(new is old for new, old in zip(new_items, items)):
            return cast(Any, data)
        return cast(Any, new_items)
    if isinstance(data, tuple):
        tuple_items = cast("tuple[object, ...]", data)
        new_tuple = tuple(_omit_compaction_encrypted_content(item) for item in tuple_items)
        if all(new is old for new, old in zip(new_tuple, tuple_items)):
            return cast(Any, data)
        return cast(Any, new_tuple)
    if not isinstance(data, dict):
        return data

    mapping = cast("dict[str, object]", data)
    nested: dict[str, object] = {key: _omit_compaction_encrypted_content(value) for key, value in mapping.items()}
    changed = any(nested[key] is not value for key, value in mapping.items())
    if mapping.get("type") == "compaction" and "encrypted_content" in mapping:
        if not changed:
            nested = dict(mapping)
        nested.pop("encrypted_content", None)
        return cast(Any, nested)
    if changed:
        return cast(Any, nested)
    return cast(Any, data)
