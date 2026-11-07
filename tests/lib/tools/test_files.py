from __future__ import annotations

from pathlib import Path

from anthropic.lib.tools._files import read_text_exact, write_text_exact


def test_read_text_exact_keeps_crlf_and_lone_cr(tmp_path: Path) -> None:
    path = tmp_path / "f.txt"
    path.write_bytes(b"a\r\nb\rc\n")
    assert read_text_exact(path) == "a\r\nb\rc\n"
    assert path.read_text(encoding="utf-8") == "a\nb\nc\n"


def test_write_text_exact_writes_verbatim(tmp_path: Path) -> None:
    path = tmp_path / "f.txt"
    write_text_exact(path, "a\r\nb\rc\né")
    assert path.read_bytes() == b"a\r\nb\rc\n\xc3\xa9"
