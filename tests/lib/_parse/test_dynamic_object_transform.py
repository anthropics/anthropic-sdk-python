from typing import Any

import pytest
from pydantic import BaseModel

from anthropic.lib._parse._transform import transform_schema


def test_additional_properties_map_raises_instead_of_becoming_empty_object():
    schema = {
        "type": "object",
        "additionalProperties": {"type": "string"},
    }

    with pytest.raises(ValueError, match="additionalProperties"):
        transform_schema(schema)


def test_additional_properties_true_raises_instead_of_becoming_empty_object():
    schema = {
        "type": "object",
        "additionalProperties": True,
    }

    with pytest.raises(ValueError, match="additionalProperties"):
        transform_schema(schema)


def test_pydantic_typed_dict_field_raises_instead_of_becoming_empty_object():
    class Model(BaseModel):
        values: dict[str, str]

    schema = Model.model_json_schema()["properties"]["values"]

    with pytest.raises(ValueError, match="additionalProperties"):
        transform_schema(schema)


def test_pydantic_arbitrary_dict_field_raises_instead_of_becoming_empty_object():
    class Model(BaseModel):
        values: dict[str, Any]

    schema = Model.model_json_schema()["properties"]["values"]

    with pytest.raises(ValueError, match="additionalProperties"):
        transform_schema(schema)
