from __future__ import annotations

from typing import cast
from pathlib import Path

from anyio import Path as AsyncPath

# tokenizers is untyped, https://github.com/huggingface/tokenizers/issues/811
# note: this comment affects the entire file
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
from tokenizers import Tokenizer  # type: ignore[import]


def _get_tokenizer_cache_path() -> Path:
    return Path(__file__).parent / "tokenizer.json"


_tokenizer: Tokenizer | None = None


def _load_tokenizer(raw: str) -> Tokenizer:
    global _tokenizer

    _tokenizer = cast(Tokenizer, Tokenizer.from_str(raw))
    return _tokenizer


def sync_get_tokenizer() -> Tokenizer:
    if _tokenizer is not None:
        return _tokenizer

    tokenizer_path = _get_tokenizer_cache_path()
    text = tokenizer_path.read_text(encoding="utf-8")
    return _load_tokenizer(text)


async def async_get_tokenizer() -> Tokenizer:
    if _tokenizer is not None:
        return _tokenizer

    tokenizer_path = AsyncPath(_get_tokenizer_cache_path())
    text = await tokenizer_path.read_text(encoding="utf-8")
    return _load_tokenizer(text)
