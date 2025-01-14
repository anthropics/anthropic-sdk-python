# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .cache_control_ephemeral_param import CacheControlEphemeralParam

__all__ = ["ToolParam", "InputSchema"]


InputSchemaTyped = TypedDict(
    'InputSchemaType',
    {
        '$comment': str,
        '$defs': object,
        '$dynamicAnchor': str,
        '$dynamicRef': str,
        '$id': str,
        '$schema': str,
        'additionalProperties': bool,
        'default': object,
        'deprecated': bool,
        'examples': list[object],
        'if': object,
        'maxProperties': int,
        'minProperties': int,
        'patternProperties': object,
        'properties': object,
        'readOnly': bool,
        'writeOnly': bool,
        'then': object,
        'title': str,
        'description': str,
        'type': Required[Literal["object"]],
        'unevaluatedProperties': bool,
    },
    total=False,
)

InputSchema: TypeAlias = InputSchemaTyped


class ToolParam(TypedDict, total=False):
    input_schema: Required[InputSchema]
    """[JSON schema](https://json-schema.org/) for this tool's input.

    This defines the shape of the `input` that your tool accepts and that the model
    will produce.
    """

    name: Required[str]
    """Name of the tool.

    This is how the tool will be called by the model and in tool_use blocks.
    """

    cache_control: Optional[CacheControlEphemeralParam]

    description: str
    """Description of what this tool does.

    Tool descriptions should be as detailed as possible. The more information that
    the model has about what the tool is and how to use it, the better it will
    perform. You can use natural language descriptions to reinforce important
    aspects of the tool input JSON schema.
    """
