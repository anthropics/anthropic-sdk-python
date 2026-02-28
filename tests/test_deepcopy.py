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


def test_tuple_with_mutable_contents() -> None:
    """Tuples containing mutable objects (like FileTypes headers) must be deep copied."""
    headers = {"X-Custom": "value"}
    obj1 = ("test.txt", b"hello", "text/plain", headers)
    obj2 = deepcopy_minimal(obj1)
    assert_different_identities(obj1, obj2)
    assert_different_identities(obj1[3], obj2[3])
    # Mutating the copy must not affect the original
    obj2[3]["X-Injected"] = "surprise"
    assert "X-Injected" not in headers


def test_dict_containing_tuple() -> None:
    """Simulates the files.beta.upload body: deepcopy_minimal({'file': file_tuple})."""
    headers = {"Authorization": "Bearer xyz"}
    file_tuple = ("doc.pdf", b"data", "application/pdf", headers)
    body = {"file": file_tuple}
    body_copy = deepcopy_minimal(body)
    assert_different_identities(body, body_copy)
    assert_different_identities(body["file"], body_copy["file"])
    assert_different_identities(body["file"][3], body_copy["file"][3])
    # Mutating the copy's headers must not affect the original
    body_copy["file"][3]["X-Mutated"] = "yes"
    assert "X-Mutated" not in headers


def test_list_of_tuples() -> None:
    """Simulates the skills/versions.py body: deepcopy_minimal({'files': [file_tuple, ...]})."""
    headers = {"X-H": "v"}
    files = [("a.txt", b"data", "text/plain", headers)]
    body = {"files": files}
    body_copy = deepcopy_minimal(body)
    assert_different_identities(body_copy["files"][0], body["files"][0])
    assert_different_identities(body_copy["files"][0][3], body["files"][0][3])
