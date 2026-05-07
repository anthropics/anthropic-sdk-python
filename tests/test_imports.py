from __future__ import annotations

import os
import sys
import json
import subprocess
from typing import Any
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_import_check(code: str) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True, env=env)
    return json.loads(result.stdout)


def test_import_anthropic_does_not_load_heavy_reexports() -> None:
    result = run_import_check(
        """
import json
import sys

import anthropic

modules = [
    "httpx",
    "pydantic",
    "anthropic._types",
    "anthropic._client",
    "anthropic._models",
    "anthropic._base_client",
    "anthropic._response",
    "anthropic.types",
    "anthropic.resources",
    "anthropic.lib.tools",
    "anthropic.lib.vertex",
    "anthropic.lib.bedrock",
    "anthropic.lib.streaming",
    "anthropic.lib._parse._transform",
]

print(json.dumps({module: module in sys.modules for module in modules}))
"""
    )

    assert result == {
        "httpx": False,
        "pydantic": False,
        "anthropic._types": False,
        "anthropic._client": False,
        "anthropic._models": False,
        "anthropic._base_client": False,
        "anthropic._response": False,
        "anthropic.types": False,
        "anthropic.resources": False,
        "anthropic.lib.tools": False,
        "anthropic.lib.vertex": False,
        "anthropic.lib.bedrock": False,
        "anthropic.lib.streaming": False,
        "anthropic.lib._parse._transform": False,
    }


def test_lazy_root_reexports_still_resolve() -> None:
    result = run_import_check(
        """
import json

from anthropic import Anthropic, AnthropicBedrock, AnthropicVertex, NotGiven, beta_tool, transform_schema, types

print(json.dumps({
    "types": types.__name__,
    "Anthropic": Anthropic.__name__,
    "AnthropicVertex": AnthropicVertex.__name__,
    "AnthropicBedrock": AnthropicBedrock.__name__,
    "NotGiven": NotGiven.__name__,
    "beta_tool": beta_tool.__name__,
    "transform_schema": transform_schema.__name__,
}))
"""
    )

    assert result == {
        "types": "anthropic.types",
        "Anthropic": "Anthropic",
        "AnthropicVertex": "AnthropicVertex",
        "AnthropicBedrock": "AnthropicBedrock",
        "NotGiven": "NotGiven",
        "beta_tool": "beta_tool",
        "transform_schema": "transform_schema",
    }
