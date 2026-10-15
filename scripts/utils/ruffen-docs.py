# fork of https://github.com/asottile/blacken-docs adapted for ruff
from __future__ import annotations

import os
import re
import sys
import argparse
import tempfile
import textwrap
import subprocess
from typing import Match, Sequence

MD_RE = re.compile(
    r"(?P<before>^(?P<indent> *)```\s*python\n)" r"(?P<code>.*?)" r"(?P<after>^(?P=indent)```\s*$)",
    re.DOTALL | re.MULTILINE,
)
DEFAULT_LINE_LENGTH = 100


def format_code_blocks(blocks: Sequence[str]) -> dict[str, str]:
    """Formats all the given blocks with one run of ruff, as starting ruff takes far longer than formatting a block.

    Exits if ruff can't format one of them. Ruff's error names the block by its index, as `<index>.py`.
    """
    # without a path, ruff formats the whole directory
    if not blocks:
        return {}

    # in this directory, so that ruff finds the project's config
    with tempfile.TemporaryDirectory(prefix=".ruffen-docs-", dir=os.curdir) as directory:
        paths = [os.path.join(directory, f"{index}.py") for index in range(len(blocks))]
        for index, block in enumerate(blocks):
            with open(paths[index], "w", encoding="UTF-8") as f:
                f.write(block)

        result = subprocess.run(
            [sys.executable, "-m", "ruff", "format", f"--line-length={DEFAULT_LINE_LENGTH}", *paths],
            stdout=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)

        formatted: dict[str, str] = {}
        for index, block in enumerate(blocks):
            with open(paths[index], encoding="UTF-8") as f:
                formatted[block] = f.read()
        return formatted


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    contents: dict[str, str] = {}
    for filename in args.filenames:
        with open(filename, encoding="UTF-8") as f:
            contents[filename] = f.read()

    formatted = format_code_blocks(
        [textwrap.dedent(match["code"]) for src in contents.values() for match in MD_RE.finditer(src)]
    )

    def _md_match(match: Match[str]) -> str:
        code = textwrap.indent(formatted[textwrap.dedent(match["code"])], match["indent"])
        return f"{match['before']}{code}{match['after']}"

    for filename, src in contents.items():
        new_contents = MD_RE.sub(_md_match, src)
        if src != new_contents:
            print(f"{filename}: Rewriting...")
            with open(filename, "w", encoding="UTF-8") as f:
                f.write(new_contents)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
