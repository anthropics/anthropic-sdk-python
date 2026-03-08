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


def test_simple_tuple() -> None:
    obj1 = ("a", "b")
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)


def test_tuple_with_nested_dict() -> None:
    """Regression test for #1202: deepcopy_minimal should recurse into tuples
    so that dicts nested inside tuples (e.g. FileTypes headers) are copied,
    not shared with the caller."""
    headers = {"content-type": "application/pdf"}
    obj1 = ("file.pdf", b"content", "application/pdf", headers)
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1[3], obj2[3])
    # mutating the copy must not affect the original
    obj2[3]["x-custom"] = "injected"
    assert "x-custom" not in headers
