#!/usr/bin/env -S uv run python
"""Example: Creating a skill using files_from_zip and files_from_dir helpers.

Demonstrates three ways to pass files to `client.beta.skills.create()`:

1. `files_from_dir` — load all files from a local directory
2. `files_from_zip` — load all files from a zip archive
3. Manual file tuples — MIME type is optional (2-tuple and 3-tuple can be mixed)
"""

import anthropic
from anthropic.lib import files_from_dir, files_from_zip

client = anthropic.Anthropic()

# ── Option 1: Load files from a directory ────────────────────────────────────
skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=files_from_dir("/path/to/financial_analysis_skill"),
    betas=["skills-2025-10-02"],
)
print(f"Created skill from directory: {skill.id}")

# ── Option 2: Load files from a zip archive ─────────────────────────────────
skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=files_from_zip("financial_analysis_skill.zip"),
    betas=["skills-2025-10-02"],
)
print(f"Created skill from zip: {skill.id}")

# ── Option 3: Manual file tuples (MIME type is optional) ────────────────────
#
# You can freely mix 2-tuples (filename, content) and 3-tuples
# (filename, content, mime_type). The SDK handles both formats.
skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=[
        (
            "financial_skill/SKILL.md",
            open("financial_skill/SKILL.md", "rb"),
            "text/markdown",  # Optional MIME type
        ),
        (
            "financial_skill/analyze.py",
            open("financial_skill/analyze.py", "rb"),
            # No MIME type — this is perfectly fine
        ),
    ],
    betas=["skills-2025-10-02"],
)
print(f"Created skill from tuples: {skill.id}")
