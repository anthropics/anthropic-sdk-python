from __future__ import annotations

import sys
from typing import Any, Dict

import pytest

from anthropic._utils import function_has_argument, signature_without_evaluating_annotations


@pytest.mark.skipif(sys.version_info < (3, 14), reason="annotations are evaluated lazily from Python 3.14")
def test_signature_without_evaluating_annotations_tolerates_undefined_names() -> None:
    namespace: Dict[str, Any] = {}
    source = "def func(a: OnlyForTypeCheckers, *, b: int = 1) -> OnlyForTypeCheckers: ..."
    # dont_inherit: this module's `from __future__ import annotations` would turn the annotations into strings.
    exec(compile(source, "<func>", "exec", dont_inherit=True), namespace)

    signature = signature_without_evaluating_annotations(namespace["func"])
    assert list(signature.parameters) == ["a", "b"]
    assert signature.parameters["a"].annotation == "OnlyForTypeCheckers"
    assert signature.parameters["b"].default == 1
    assert function_has_argument(namespace["func"], "b")
