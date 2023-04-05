import os
import tempfile

import httpx
from tokenizers import Tokenizer

CLAUDE_TOKENIZER_REMOTE_FILE = "https://public-json-tokenization-0d8763e8-0d7e-441b-a1e2-1c73b8e79dc3.storage.googleapis.com/claude-v1-tokenization.json"

claude_tokenizer = None

class TokenizerException(Exception):
    pass

def _get_tokenizer_filename() -> str:
    cache_dir = os.path.join(tempfile.gettempdir(), "anthropic")
    os.makedirs(cache_dir, exist_ok=True)
    tokenizer_file = os.path.join(cache_dir, 'claude_tokenizer.json')
    return tokenizer_file

def _get_cached_tokenizer_file_as_str() -> str:
    tokenizer_file = _get_tokenizer_filename()
    if not os.path.exists(tokenizer_file):
        response = httpx.get(CLAUDE_TOKENIZER_REMOTE_FILE)
        response.raise_for_status()
        with open(tokenizer_file, 'w', encoding="utf-8") as f:
            f.write(response.text)

    with open(tokenizer_file, 'r', encoding="utf-8") as f:
        return f.read()

def get_tokenizer() -> Tokenizer:
    global claude_tokenizer

    if not claude_tokenizer:
        try:
            tokenizer_data = _get_cached_tokenizer_file_as_str()
        except httpx.HTTPError as e:
            raise TokenizerException(f'Failed to download tokenizer: {e}')
        try:
            claude_tokenizer = Tokenizer.from_str(tokenizer_data)
        except Exception as e:
            # If the tokenizer file is unparseable, let's delete it here and clean things up
            try:
                os.remove(_get_tokenizer_filename())
            except FileNotFoundError:
                pass
            raise TokenizerException(f'Failed to load tokenizer: {e}')

    return claude_tokenizer

def count_tokens(text: str) -> int:
    tokenizer = get_tokenizer()
    encoded_text = tokenizer.encode(text)
    return len(encoded_text.ids)
