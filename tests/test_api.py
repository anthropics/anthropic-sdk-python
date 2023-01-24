import pytest
import anthropic
from anthropic import api

def test_prompt_validator():
    # No exceptions expected
    api._validate_prompt(f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT}")
    api._validate_prompt(f"{anthropic.HUMAN_PROMPT} Hello{anthropic.AI_PROMPT} First answer{anthropic.HUMAN_PROMPT} Try again{anthropic.AI_PROMPT}")
    with pytest.raises(ValueError):
        api._validate_prompt(f"{anthropic.HUMAN_PROMPT} Hello")
    with pytest.raises(ValueError):
        api._validate_prompt(f"{anthropic.AI_PROMPT} ")
    with pytest.raises(ValueError):
        api._validate_prompt(f"Human: Hello{anthropic.AI_PROMPT}")
