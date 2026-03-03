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
    obj1 = ("a", "b", "c")
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)


def test_tuple_with_nested_dict() -> None:
    """Tuples containing dicts should have those dicts deep-copied.

    This is the core fix for issue #1202: FileTypes tuples like
    (filename, content, content_type, headers_dict) must not share
    the headers dict reference with the original.
    """
    headers = {"X-Custom": "value"}
    obj1 = ("file.txt", b"content", "text/plain", headers)
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    # The nested dict inside the tuple must be a separate copy
    assert_different_identities(obj1[3], obj2[3])


def test_dict_with_tuple_value() -> None:
    """Dicts containing tuples with nested dicts should be fully deep-copied."""
    inner_dict = {"key": "value"}
    obj1 = {"file": ("name", b"data", "type", inner_dict)}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1["file"], obj2["file"])
    assert_different_identities(obj1["file"][3], obj2["file"][3])


class MyObject: ...


def test_ignores_other_types() -> None:
    # custom classes
    my_obj = MyObject()
    obj1 = {"foo": my_obj}
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert obj1["foo"] is my_obj
