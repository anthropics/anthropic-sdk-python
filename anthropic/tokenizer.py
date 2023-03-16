import os
import tempfile

import httpx
from tokenizers import Tokenizer

CLAUDE_TOKENIZER_REMOTE_FILE = "https://public-json-tokenization-0d8763e8-0d7e-441b-a1e2-1c73b8e79dc3.storage.googleapis.com/claude-v1-tokenization.json"

claude_tokenizer = None

def _get_cached_tokenizer_file_as_str() -> str:
    cache_dir = os.path.join(tempfile.gettempdir(), "anthropic")

    tokenizer_file = os.path.join(cache_dir, 'claude_tokenizer_file.json')
    if not os.path.exists(tokenizer_file):
        os.makedirs(cache_dir, exist_ok=True)
        response = httpx.get(CLAUDE_TOKENIZER_REMOTE_FILE)
        with open(tokenizer_file, 'w') as f:
            f.write(response.text)

    with open(tokenizer_file, 'r') as f:
        return f.read()

def get_tokenizer() -> Tokenizer:
    global claude_tokenizer

    if not claude_tokenizer:
        tokenizer_data = _get_cached_tokenizer_file_as_str()
        claude_tokenizer = Tokenizer.from_str(tokenizer_data)

    return claude_tokenizer

def count_tokens(text: str) -> int:
    tokenizer = get_tokenizer()
    encoded_text = tokenizer.encode(text)
    return len(encoded_text.ids)
