import pytest
import anthropic
from anthropic import api, ApiException, tokenizer
import os

def test_prompt_validator():
    # No exceptions expected
    api._validate_request({"max_tokens_to_sample": 1, "prompt": f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT}"})
    api._validate_request({"max_tokens_to_sample": 1, "prompt": f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT} First answer{anthropic.HUMAN_PROMPT} Try again{anthropic.AI_PROMPT}"})
    with pytest.raises(ApiException):
        api._validate_request({"max_tokens_to_sample": 1, "prompt": f"{anthropic.HUMAN_PROMPT} Hello"})
    with pytest.raises(ApiException):
        api._validate_request({"max_tokens_to_sample": 1, "prompt": f"{anthropic.AI_PROMPT} "})
    with pytest.raises(ApiException):
        api._validate_request({"max_tokens_to_sample": 1, "prompt": f"Human: Hello{anthropic.AI_PROMPT}"})

def test_sample_length():
    # No exceptions expected
    good_request = {"max_tokens_to_sample": 1, "prompt": f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT}"}
    api._validate_request(good_request)
    bad_request = good_request.copy()
    bad_request["max_tokens_to_sample"] = 10000
    with pytest.raises(ApiException):
        api._validate_request(bad_request)

    bad_request = good_request.copy()
    bad_request["prompt"] = bad_request["prompt"] * 2000
    with pytest.raises(ApiException):
        api._validate_request(bad_request)

def test_prompt_validator_fail(monkeypatch):
    # Ensure we don't have any tokenizer loaded or saved
    monkeypatch.setattr(tokenizer, "CLAUDE_TOKENIZER_REMOTE_FILE", tokenizer.CLAUDE_TOKENIZER_REMOTE_FILE + '-but-nonexistent')
    tokenizer.claude_tokenizer = None
    os.remove(tokenizer._get_tokenizer_filename())
    # Now verify a good request fails open
    api._validate_prompt_length({"max_tokens_to_sample": 1, "prompt": f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT}"})
    # And now verify a bad request fails open too
    api._validate_prompt_length({"max_tokens_to_sample": 100000, "prompt": f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT}"})

