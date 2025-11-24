from copy import deepcopy

import pytest
from inline_snapshot import snapshot

from anthropic.lib._parse._transform import transform_schema


def test_ref_schema():
    schema = {"$ref": "#/components/schemas/SomeSchema"}
    result = transform_schema(schema)
    assert result == snapshot({"$ref": "#/components/schemas/SomeSchema"})


def test_anyof_schema():
    schema = {
        "anyOf": [
            {"type": "string"},
            {"type": "integer", "minimum": 1},
        ]
    }
    result = transform_schema(schema)
    assert result == snapshot(
        {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "integer",
                    "description": "{minimum: 1}",
                },
            ]
        }
    )


def test_allof():
    schema = {
        "allOf": [
            {"type": "object", "properties": {"name": {"type": "string"}}},
            {"type": "object", "properties": {"age": {"type": "integer", "minimum": 0}}},
        ]
    }
    result = transform_schema(schema)
    assert result == snapshot(
        {
            "allOf": [
                {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "additionalProperties": False,
                },
                {
                    "type": "object",
                    "properties": {"age": {"type": "integer", "description": "{minimum: 0}"}},
                    "additionalProperties": False,
                },
            ]
        }
    )


def test_object_schema():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "default": "John"},
            "age": {"type": "integer", "minimum": 0},
        },
        "required": ["name"],
        "description": "Person object",
    }
    result = transform_schema(schema)
    assert result == snapshot(
        {
            "type": "object",
            "description": "Person object",
            "properties": {
                "name": {"type": "string", "description": "{default: John}"},
                "age": {"type": "integer", "description": "{minimum: 0}"},
            },
            "additionalProperties": False,
            "required": ["name"],
        }
    )


def test_array_schema():
    schema = {
        "type": "array",
        "items": {"type": "string"},
        "minItems": 2,
        "description": "A list of strings",
    }
    result = transform_schema(schema)
    assert result == snapshot(
        {
            "type": "array",
            "description": """\
A list of strings

{minItems: 2}\
""",
            "items": {"type": "string"},
        }
    )


def test_string_schema_with_format_and_default():
    schema = {
        "type": "string",
        "format": "email",
        "default": "user@example.com",
        "description": "User email",
    }
    result = transform_schema(schema)
    assert result == snapshot(
        {
            "type": "string",
            "description": """\
User email

{default: user@example.com}\
""",
            "format": "email",
        }
    )


def test_string_schema_without_format():
    schema = {"type": "string"}
    result = transform_schema(schema)
    assert result == snapshot({"type": "string"})


def test_integer_schema_with_min_max_exclusive():
    schema = {
        "type": "integer",
        "minimum": 1,
        "maximum": 10,
        "exclusiveMinimum": 0,
        "exclusiveMaximum": 20,
        "description": "A number",
    }
    result = transform_schema(schema)
    assert result == snapshot(
        {
            "type": "integer",
            "description": """\
A number

{minimum: 1, maximum: 10, exclusiveMinimum: 0, exclusiveMaximum: 20}\
""",
        }
    )


def test_boolean_schema():
    schema = {"type": "boolean", "description": "A flag"}
    result = transform_schema(schema)
    assert result == snapshot({"type": "boolean", "description": "A flag"})


def test_null_schema():
    schema = {"type": "null"}
    result = transform_schema(schema)
    assert result == snapshot({"type": "null"})


def test_unsupported_type_asserts():
    schema = {"type": "unsupported"}
    with pytest.raises(AssertionError):
        transform_schema(schema)


def test_original_schema_not_mutated():
    original_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "default": "John"},
            "age": {"type": "integer", "minimum": 0},
        },
        "required": ["name"],
        "description": "Person object",
        "additionalProperties": True,
    }

    original_schema_backup = deepcopy(original_schema)

    transform_schema(original_schema)

    assert original_schema == original_schema_backup
