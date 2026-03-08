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


class MyObject: ...


def test_ignores_other_types() -> None:
    # custom classes
    my_obj = MyObject()
    obj1 = {"foo": my_obj}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert obj1["foo"] is my_obj

    # tuples (immutable contents only — still creates new tuple object)
    obj3 = ("a", "b")
    obj4 = deepcopy_minimal(obj3)
    assert obj3 is not obj4
    assert obj3 == obj4


def test_tuple_with_mutable_contents() -> None:
    """Tuples containing mutable objects (like dicts) should have their contents copied.

    This prevents in-place mutation of the original data when the copy is modified.
    See: https://github.com/anthropics/anthropic-sdk-python/issues/1202
    """
    inner_dict = {"content-type": "application/json"}
    obj1 = ("filename.txt", b"content", "application/json", inner_dict)
    obj2 = deepcopy_minimal(obj1)
    assert obj1 == obj2
    # The tuple itself should be a new object
    assert obj1 is not obj2
    # The inner dict should be a different object (deep copied)
    assert obj1[3] is not obj2[3]
    assert obj1[3] == obj2[3]
    # Mutating the copy should not affect the original
    obj2[3]["x-custom"] = "value"
    assert "x-custom" not in obj1[3]


def test_nested_tuple_in_dict() -> None:
    """Tuples nested inside dicts should also have their mutable contents copied."""
    inner_dict = {"key": "value"}
    obj1 = {"file": ("name.txt", b"data", "text/plain", inner_dict)}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    # The tuple should be a new object
    assert obj1["file"] is not obj2["file"]
    # The inner dict should be a new object
    assert obj1["file"][3] is not obj2["file"][3]


def test_tuple_in_list() -> None:
    """Tuples inside lists should also be deep copied."""
    inner_dict = {"header": "value"}
    obj1 = [("file.txt", b"content", "text/plain", inner_dict)]
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert obj1[0] is not obj2[0]
    assert obj1[0][3] is not obj2[0][3]
