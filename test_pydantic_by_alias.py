"""Test for Pydantic by_alias None handling fix."""
import pydantic
from anthropic._compat import model_dump

class SimpleModel(pydantic.BaseModel):
    field_name: str = pydantic.Field(alias="fieldName")

def test_model_dump_with_none_by_alias():
    """Test that model_dump handles by_alias=None correctly."""
    model = SimpleModel(fieldName="test_value")
    
    # Should not raise TypeError when by_alias is None
    result = model_dump(model, by_alias=None)
    assert isinstance(result, dict)
    assert result["field_name"] == "test_value"

def test_model_dump_with_true_by_alias():
    """Test that model_dump respects by_alias=True."""
    model = SimpleModel(fieldName="test_value")
    
    result = model_dump(model, by_alias=True)
    assert isinstance(result, dict)
    assert "fieldName" in result or "field_name" in result

def test_model_dump_with_false_by_alias():
    """Test that model_dump respects by_alias=False."""
    model = SimpleModel(fieldName="test_value")
    
    result = model_dump(model, by_alias=False)
    assert isinstance(result, dict)
    assert "field_name" in result

if __name__ == "__main__":
    test_model_dump_with_none_by_alias()
    test_model_dump_with_true_by_alias()
    test_model_dump_with_false_by_alias()
    print("All tests passed!")
