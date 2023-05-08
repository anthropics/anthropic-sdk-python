import pytest
import anthropic
from anthropic import api, ApiException

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
