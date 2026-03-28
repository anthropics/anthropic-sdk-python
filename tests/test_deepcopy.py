from anthropic._utils import deepcopy_minimal


def assert_different_identities(obj1: object, obj2: object) -> None:
    assert obj1 == obj2
    assert id(obj1) != id(obj2)


def test_simple_dict() -> None:
    obj1 = {"foo": "bar"}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)


def test_nested_dict() -> None:
    obj1 = {"foo": {"bar": True}}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1["foo"], obj2["foo"])


def test_complex_nested_dict() -> None:
    obj1 = {"foo": {"bar": [{"hello": "world"}]}}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1["foo"], obj2["foo"])
    assert_different_identities(obj1["foo"]["bar"], obj2["foo"]["bar"])
    assert_different_identities(obj1["foo"]["bar"][0], obj2["foo"]["bar"][0])


def test_simple_list() -> None:
    obj1 = ["a", "b", "c"]
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)


def test_nested_list() -> None:
    obj1 = ["a", [1, 2, 3]]
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1[1], obj2[1])


def test_simple_tuple() -> None:
    obj1 = ("a", "b")
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert obj1[0] is obj2[0]  # immutable strings are same object
    assert obj1[1] is obj2[1]


def test_nested_tuple() -> None:
    obj1 = ("a", {"bar": True})
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1[1], obj2[1])
    assert obj1[0] is obj2[0]  # immutable string preserved


class MyObject: ...


def test_ignores_other_types() -> None:
    # custom classes
    my_obj = MyObject()
    obj1 = {"foo": my_obj}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert obj1["foo"] is my_obj

    # tuples with lists inside - list should be copied
    inner_list = [1, {"x": "y"}]
    obj7 = ("z", inner_list)
    obj8 = deepcopy_minimal(obj7)
    assert obj7 is not obj8  # new tuple created
    assert obj7[1] is not obj8[1]  # list inside is copied
    assert obj7[1][1] is not obj8[1][1]  # dict inside that list is also copied

    # deeply nested: tuple -> dict -> list -> dict
    obj9 = ({"items": [{"name": "a"}]},)
    obj10 = deepcopy_minimal(obj9)
    assert obj9 is not obj10
    assert obj9[0] is not obj10[0]  # dict in tuple copied
    assert obj9[0]["items"] is not obj10[0]["items"]  # list in dict copied
    assert obj9[0]["items"][0] is not obj10[0]["items"][0]  # dict in list copied
