import os
import errno
import asyncio

import pytest

from anthropic.lib.tools._file_store import FileStore


@pytest.mark.parametrize("code", [errno.EACCES, errno.EIO, errno.EROFS])
def test_remove_propagates_failure_in_subtree(tmp_path, monkeypatch, code):
    store = FileStore(tmp_path, removed_on_dispose=False)
    sub = tmp_path / "sub"
    sub.mkdir()
    sentinel = sub / "keep.txt"
    sentinel.write_text("sentinel")
    error = OSError(code, "injected filesystem failure", str(sentinel))
    original = os.unlink

    def fail(path, *args, **kwargs):
        if os.fspath(path).endswith("keep.txt"):
            raise error
        return original(path, *args, **kwargs)

    monkeypatch.setattr(os, "unlink", fail)
    with pytest.raises(OSError) as caught:
        asyncio.run(store.remove("sub"))
    assert caught.value is error
    assert sentinel.read_text() == "sentinel"


def test_remove_tolerates_concurrently_disappearing_child(tmp_path, monkeypatch):
    store = FileStore(tmp_path, removed_on_dispose=False)
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "child").write_text("data")
    original = os.unlink

    def vanish(path, *args, **kwargs):
        original(path, *args, **kwargs)
        raise FileNotFoundError(errno.ENOENT, "already removed", os.fspath(path))

    monkeypatch.setattr(os, "unlink", vanish)
    asyncio.run(store.remove("sub"))
    assert not sub.exists()
