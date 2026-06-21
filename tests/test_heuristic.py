import pytest

from anthropic import Anthropic
from src.anthropic.patch_anthropic import patch_anthropic_client

@pytest.fixture(autouse=True)
def setup_patch():
    patch_anthropic_client()

def test_heuristic_block_garbage_prompt():
    client = Anthropic(api_key="sk-ant-fake")
    with pytest.raises(ValueError, match="BLOCKED"):
        client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=100,
            messages=[{"role": "user", "content": "asdf"}]  # vrai bruit, S≈0.12
        )

def test_heuristic_allows_short_request_now():
    # documente le comportement élargi : "fais truc" passe désormais (S≈0.62)
    client = Anthropic(api_key="sk-ant-fake")
    response_attempted = False
    try:
        client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=100,
            messages=[{"role": "user", "content": "fais truc"}]
        )
    except ValueError:
        response_attempted = True
    assert not response_attempted