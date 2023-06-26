from pathlib import Path
from functools import lru_cache

from anyio import Path as AsyncPath

# tokenizers is untyped, https://github.com/huggingface/tokenizers/issues/811
# note: this comment affects the entire file
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
from tokenizers import Tokenizer  # type: ignore[import]


def _get_tokenizer_cache_path() -> Path:
    return Path(__file__).parent / "tokenizer.json"


@lru_cache(maxsize=None)
def sync_get_tokenizer() -> Tokenizer:
    tokenizer_path = _get_tokenizer_cache_path()
    text = tokenizer_path.read_text()
    return Tokenizer.from_str(text)


@lru_cache(maxsize=None)
async def async_get_tokenizer() -> Tokenizer:
    tokenizer_path = AsyncPath(_get_tokenizer_cache_path())
    text = await tokenizer_path.read_text()
    return Tokenizer.from_str(text)
