import requests
from tokenizers import Tokenizer

CLAUDE_TOKENIZER_REMOTE_FILE = "https://public-json-tokenization-0d8763e8-0d7e-441b-a1e2-1c73b8e79dc3.storage.googleapis.com/claude-v1-tokenization.json"

claude_tokenizer = None

def get_tokenizer() -> Tokenizer:
    global claude_tokenizer

    if not claude_tokenizer:
        tokenizer_data = requests.get(CLAUDE_TOKENIZER_REMOTE_FILE)
        claude_tokenizer = Tokenizer.from_str(tokenizer_data.text)

    return claude_tokenizer

def count_tokens(text: str) -> int:
    tokenizer = get_tokenizer()
    encoded_text = tokenizer.encode(text)
    return len(encoded_text.ids)
