from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest

from anthropic import AsyncAnthropic
from anthropic.lib.tools import _skills


@pytest.mark.asyncio
async def test_failed_skill_extraction_removes_partial_destination(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    async def retrieve_session(session_id: str) -> object:
        assert session_id == "session_1"
        return SimpleNamespace(
            agent=SimpleNamespace(
                skills=[SimpleNamespace(skill_id="skill_1", version="123")],
            )
        )

    async def retrieve_version(version_id: str, *, skill_id: str) -> object:
        assert version_id == "123"
        assert skill_id == "skill_1"
        return SimpleNamespace(name="example-skill")

    client = cast(
        AsyncAnthropic,
        SimpleNamespace(
            beta=SimpleNamespace(
                sessions=SimpleNamespace(retrieve=retrieve_session),
                skills=SimpleNamespace(versions=SimpleNamespace(retrieve=retrieve_version)),
            )
        ),
    )

    async def fail_after_partial_extract(
        client: AsyncAnthropic,
        skill_id: str,
        version_id: str,
        dest: Path,
    ) -> None:
        del client, skill_id, version_id
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "partial.txt").write_text("partial", encoding="utf-8")
        raise RuntimeError("archive failed")

    monkeypatch.setattr(_skills, "_download_and_extract", fail_after_partial_extract)

    downloaded = await _skills.download_session_skills(
        client,
        session_id="session_1",
        workdir=tmp_path,
    )

    assert downloaded == []
    assert not (tmp_path / "skills" / "example-skill").exists()


class _FailingArchive:
    async def __aenter__(self) -> _FailingArchive:
        return self

    async def __aexit__(self, *exc: object) -> None:
        return None

    async def stream_to_file(self, path: str) -> None:
        Path(path).write_bytes(b"partial archive")
        raise RuntimeError("download interrupted")


@pytest.mark.asyncio
async def test_failed_skill_download_removes_temporary_archive(tmp_path: Path) -> None:
    def download(version_id: str, *, skill_id: str) -> _FailingArchive:
        assert version_id == "123"
        assert skill_id == "skill_1"
        return _FailingArchive()

    client = cast(
        AsyncAnthropic,
        SimpleNamespace(
            beta=SimpleNamespace(
                skills=SimpleNamespace(
                    versions=SimpleNamespace(
                        with_streaming_response=SimpleNamespace(download=download),
                    )
                )
            )
        ),
    )
    dest = tmp_path / "skill"

    with pytest.raises(RuntimeError, match="download interrupted"):
        await _skills._download_and_extract(client, "skill_1", "123", dest)

    assert list(tmp_path.glob(".skill-*.archive")) == []
