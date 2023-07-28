from typing import Any, Dict, List, Union, Optional, cast
from datetime import datetime, timezone
from typing_extensions import Literal

import pytest
try:
    from pydantic.v1 import Field
except ImportError:
    from pydantic import Field

from anthropic._models import BaseModel


class BasicModel(BaseModel):
    foo: str


@pytest.mark.parametrize("value", ["hello", 1], ids=["correct type", "mismatched"])
def test_basic(value: object) -> None:
    m = BasicModel.construct(foo=value)
    assert m.foo == value


def test_directly_nested_model() -> None:
    class NestedModel(BaseModel):
        nested: BasicModel

    m = NestedModel.construct(nested={"foo": "Foo!"})
    assert m.nested.foo == "Foo!"

    # mismatched types
    m = NestedModel.construct(nested="hello!")
    assert m.nested == "hello!"


def test_optional_nested_model() -> None:
    class NestedModel(BaseModel):
        nested: Optional[BasicModel]

    m1 = NestedModel.construct(nested=None)
    assert m1.nested is None

    m2 = NestedModel.construct(nested={"foo": "bar"})
    assert m2.nested is not None
    assert m2.nested.foo == "bar"

    # mismatched types
    m3 = NestedModel.construct(nested={"foo"})
    assert isinstance(cast(Any, m3.nested), set)
    assert m3.nested == {"foo"}


def test_list_nested_model() -> None:
    class NestedModel(BaseModel):
        nested: List[BasicModel]

    m = NestedModel.construct(nested=[{"foo": "bar"}, {"foo": "2"}])
    assert m.nested is not None
    assert isinstance(m.nested, list)
    assert len(m.nested) == 2
    assert m.nested[0].foo == "bar"
    assert m.nested[1].foo == "2"

    # mismatched types
    m = NestedModel.construct(nested=True)
    assert cast(Any, m.nested) is True

    m = NestedModel.construct(nested=[False])
    assert cast(Any, m.nested) == [False]


def test_optional_list_nested_model() -> None:
    class NestedModel(BaseModel):
        nested: Optional[List[BasicModel]]

    m1 = NestedModel.construct(nested=[{"foo": "bar"}, {"foo": "2"}])
    assert m1.nested is not None
    assert isinstance(m1.nested, list)
    assert len(m1.nested) == 2
    assert m1.nested[0].foo == "bar"
    assert m1.nested[1].foo == "2"

    m2 = NestedModel.construct(nested=None)
    assert m2.nested is None

    # mismatched types
    m3 = NestedModel.construct(nested={1})
    assert cast(Any, m3.nested) == {1}

    m4 = NestedModel.construct(nested=[False])
    assert cast(Any, m4.nested) == [False]


def test_list_optional_items_nested_model() -> None:
    class NestedModel(BaseModel):
        nested: List[Optional[BasicModel]]

    m = NestedModel.construct(nested=[None, {"foo": "bar"}])
    assert m.nested is not None
    assert isinstance(m.nested, list)
    assert len(m.nested) == 2
    assert m.nested[0] is None
    assert m.nested[1] is not None
    assert m.nested[1].foo == "bar"

    # mismatched types
    m3 = NestedModel.construct(nested="foo")
    assert cast(Any, m3.nested) == "foo"

    m4 = NestedModel.construct(nested=[False])
    assert cast(Any, m4.nested) == [False]


def test_list_mismatched_type() -> None:
    class NestedModel(BaseModel):
        nested: List[str]

    m = NestedModel.construct(nested=False)
    assert cast(Any, m.nested) is False


def test_raw_dictionary() -> None:
    class NestedModel(BaseModel):
        nested: Dict[str, str]

    m = NestedModel.construct(nested={"hello": "world"})
    assert m.nested == {"hello": "world"}

    # mismatched types
    m = NestedModel.construct(nested=False)
    assert cast(Any, m.nested) is False


def test_nested_dictionary_model() -> None:
    class NestedModel(BaseModel):
        nested: Dict[str, BasicModel]

    m = NestedModel.construct(nested={"hello": {"foo": "bar"}})
    assert isinstance(m.nested, dict)
    assert m.nested["hello"].foo == "bar"

    # mismatched types
    m = NestedModel.construct(nested={"hello": False})
    assert cast(Any, m.nested["hello"]) is False


def test_unknown_fields() -> None:
    m1 = BasicModel.construct(foo="foo", unknown=1)
    assert m1.foo == "foo"
    assert cast(Any, m1).unknown == 1

    m2 = BasicModel.construct(foo="foo", unknown={"foo_bar": True})
    assert m2.foo == "foo"
    assert cast(Any, m2).unknown == {"foo_bar": True}

    assert m2.dict() == {"foo": "foo", "unknown": {"foo_bar": True}}


def test_strict_validation_unknown_fields() -> None:
    class Model(BaseModel):
        foo: str

    model = Model.parse_obj(dict(foo="hello!", user="Robert"))
    assert model.foo == "hello!"
    assert cast(Any, model).user == "Robert"

    assert model.dict() == {"foo": "hello!", "user": "Robert"}


def test_aliases() -> None:
    class Model(BaseModel):
        my_field: int = Field(alias="myField")

    m = Model.construct(myField=1)
    assert m.my_field == 1

    # mismatched types
    m = Model.construct(myField={"hello": False})
    assert cast(Any, m.my_field) == {"hello": False}


def test_repr() -> None:
    model = BasicModel(foo="bar")
    assert str(model) == "BasicModel(foo='bar')"
    assert repr(model) == "BasicModel(foo='bar')"


def test_repr_nested_model() -> None:
    class Child(BaseModel):
        name: str
        age: int

    class Parent(BaseModel):
        name: str
        child: Child

    model = Parent(name="Robert", child=Child(name="Foo", age=5))
    assert str(model) == "Parent(name='Robert', child=Child(name='Foo', age=5))"
    assert repr(model) == "Parent(name='Robert', child=Child(name='Foo', age=5))"


def test_optional_list() -> None:
    class Submodel(BaseModel):
        name: str

    class Model(BaseModel):
        items: Optional[List[Submodel]]

    m = Model.construct(items=None)
    assert m.items is None

    m = Model.construct(items=[])
    assert m.items == []

    m = Model.construct(items=[{"name": "Robert"}])
    assert m.items is not None
    assert len(m.items) == 1
    assert m.items[0].name == "Robert"


def test_nested_union_of_models() -> None:
    class Submodel1(BaseModel):
        bar: bool

    class Submodel2(BaseModel):
        thing: str

    class Model(BaseModel):
        foo: Union[Submodel1, Submodel2]

    m = Model.construct(foo={"thing": "hello"})
    assert isinstance(m.foo, Submodel2)
    assert m.foo.thing == "hello"


def test_nested_union_of_mixed_types() -> None:
    class Submodel1(BaseModel):
        bar: bool

    class Model(BaseModel):
        foo: Union[Submodel1, Literal[True], Literal["CARD_HOLDER"]]

    m = Model.construct(foo=True)
    assert m.foo is True

    m = Model.construct(foo="CARD_HOLDER")
    assert m.foo is "CARD_HOLDER"

    m = Model.construct(foo={"bar": False})
    assert isinstance(m.foo, Submodel1)
    assert m.foo.bar is False


def test_nested_union_multiple_variants() -> None:
    class Submodel1(BaseModel):
        bar: bool

    class Submodel2(BaseModel):
        thing: str

    class Submodel3(BaseModel):
        foo: int

    class Model(BaseModel):
        foo: Union[Submodel1, Submodel2, None, Submodel3]

    m = Model.construct(foo={"thing": "hello"})
    assert isinstance(m.foo, Submodel2)
    assert m.foo.thing == "hello"

    m = Model.construct(foo=None)
    assert m.foo is None

    m = Model.construct()
    assert m.foo is None

    m = Model.construct(foo={"foo": "1"})
    assert isinstance(m.foo, Submodel3)
    assert m.foo.foo == 1


def test_nested_union_invalid_data() -> None:
    class Submodel1(BaseModel):
        level: int

    class Submodel2(BaseModel):
        name: str

    class Model(BaseModel):
        foo: Union[Submodel1, Submodel2]

    m = Model.construct(foo=True)
    assert cast(bool, m.foo) is True

    m = Model.construct(foo={"name": 3})
    assert isinstance(m.foo, Submodel2)
    assert m.foo.name == "3"


def test_list_of_unions() -> None:
    class Submodel1(BaseModel):
        level: int

    class Submodel2(BaseModel):
        name: str

    class Model(BaseModel):
        items: List[Union[Submodel1, Submodel2]]

    m = Model.construct(items=[{"level": 1}, {"name": "Robert"}])
    assert len(m.items) == 2
    assert isinstance(m.items[0], Submodel1)
    assert m.items[0].level == 1
    assert isinstance(m.items[1], Submodel2)
    assert m.items[1].name == "Robert"

    m = Model.construct(items=[{"level": -1}, 156])
    assert len(m.items) == 2
    assert isinstance(m.items[0], Submodel1)
    assert m.items[0].level == -1
    assert m.items[1] == 156


def test_union_of_lists() -> None:
    class SubModel1(BaseModel):
        level: int

    class SubModel2(BaseModel):
        name: str

    class Model(BaseModel):
        items: Union[List[SubModel1], List[SubModel2]]

    # with one valid entry
    m = Model.construct(items=[{"name": "Robert"}])
    assert len(m.items) == 1
    assert isinstance(m.items[0], SubModel2)
    assert m.items[0].name == "Robert"

    # with two entries pointing to different types
    m = Model.construct(items=[{"level": 1}, {"name": "Robert"}])
    assert len(m.items) == 2
    assert isinstance(m.items[0], SubModel1)
    assert m.items[0].level == 1
    assert isinstance(m.items[1], SubModel1)
    assert cast(Any, m.items[1]).name == "Robert"

    # with two entries pointing to *completely* different types
    m = Model.construct(items=[{"level": -1}, 156])
    assert len(m.items) == 2
    assert isinstance(m.items[0], SubModel1)
    assert m.items[0].level == -1
    assert m.items[1] == 156


def test_dict_of_union() -> None:
    class SubModel1(BaseModel):
        name: str

    class SubModel2(BaseModel):
        foo: str

    class Model(BaseModel):
        data: Dict[str, Union[SubModel1, SubModel2]]

    m = Model.construct(data={"hello": {"name": "there"}, "foo": {"foo": "bar"}})
    assert len(list(m.data.keys())) == 2
    assert isinstance(m.data["hello"], SubModel1)
    assert m.data["hello"].name == "there"
    assert isinstance(m.data["foo"], SubModel2)
    assert m.data["foo"].foo == "bar"

    # TODO: test mismatched type


def test_double_nested_union() -> None:
    class SubModel1(BaseModel):
        name: str

    class SubModel2(BaseModel):
        bar: str

    class Model(BaseModel):
        data: Dict[str, List[Union[SubModel1, SubModel2]]]

    m = Model.construct(data={"foo": [{"bar": "baz"}, {"name": "Robert"}]})
    assert len(m.data["foo"]) == 2

    entry1 = m.data["foo"][0]
    assert isinstance(entry1, SubModel2)
    assert entry1.bar == "baz"

    entry2 = m.data["foo"][1]
    assert isinstance(entry2, SubModel1)
    assert entry2.name == "Robert"

    # TODO: test mismatched type


def test_union_of_dict() -> None:
    class SubModel1(BaseModel):
        name: str

    class SubModel2(BaseModel):
        foo: str

    class Model(BaseModel):
        data: Union[Dict[str, SubModel1], Dict[str, SubModel2]]

    m = Model.construct(data={"hello": {"name": "there"}, "foo": {"foo": "bar"}})
    assert len(list(m.data.keys())) == 2
    assert isinstance(m.data["hello"], SubModel1)
    assert m.data["hello"].name == "there"
    assert isinstance(m.data["foo"], SubModel1)
    assert cast(Any, m.data["foo"]).foo == "bar"


def test_iso8601_datetime() -> None:
    class Model(BaseModel):
        created_at: datetime

    expected = datetime(2019, 12, 27, 18, 11, 19, 117000, tzinfo=timezone.utc)
    expected_json = '{"created_at": "2019-12-27T18:11:19.117000+00:00"}'

    model = Model.construct(created_at="2019-12-27T18:11:19.117Z")
    assert model.created_at == expected
    assert model.json() == expected_json

    model = Model.parse_obj(dict(created_at="2019-12-27T18:11:19.117Z"))
    assert model.created_at == expected
    assert model.json() == expected_json


def test_coerces_int() -> None:
    class Model(BaseModel):
        bar: int

    assert Model.construct(bar=1).bar == 1
    assert Model.construct(bar=10.9).bar == 10
    assert Model.construct(bar="19").bar == 19
    assert Model.construct(bar=False).bar == 0

    # TODO: support this
    # assert Model.construct(bar="True").bar == 1

    # mismatched types are left as-is
    m = Model.construct(bar={"foo": "bar"})
    assert m.bar == {"foo": "bar"}  # type: ignore[comparison-overlap]
