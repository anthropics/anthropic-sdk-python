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

    # tuples - new tuple created but immutable contents not copied
    obj3 = ("a", "b")
    obj4 = deepcopy_minimal(obj3)
    assert obj3 is not obj4  # new tuple created
    assert obj3[0] is obj4[0]  # but immutable strings are same object
    assert obj3[1] is obj4[1]

    # tuples with dicts inside - dict should be copied
    inner_dict = {"bar": True}
    obj5 = ("a", inner_dict)
    obj6 = deepcopy_minimal(obj5)
    assert obj5 is not obj6  # new tuple created
    assert obj5[1] is not obj6[1]  # dict inside is copied
