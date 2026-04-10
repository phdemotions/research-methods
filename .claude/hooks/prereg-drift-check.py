#!/usr/bin/env python3
"""
PostToolUse hook: advisory when analysis code may deviate from pre-registration.

Fires after every Edit or Write tool call. If the target file is in an analysis
directory (R/, python/, or analysis-related paths) AND a pre-registration file
exists in the project, emits an advisory reminder to check for drift.

This is advisory only — it never blocks. It's a gentle nudge: "you just changed
analysis code; did you check the pre-registration?"

Fail-open: errors in this hook never disrupt the researcher's work.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def silent_pass() -> None:
    """Exit silently with no output — no advisory needed."""
    sys.exit(0)


def read_hook_input() -> dict:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def get_target_path(payload: dict) -> str | None:
    """Extract the file path from the tool result."""
    # PostToolUse receives tool_input with the original parameters
    tool_input = payload.get("tool_input", {})
    if isinstance(tool_input, dict):
        return tool_input.get("file_path")
    return None


def is_analysis_file(file_path: str, cwd: str) -> bool:
    """Check if the target file is likely analysis code."""
    try:
        target = Path(file_path)
        if not target.is_absolute():
            target = Path(cwd) / target
        target = target.resolve()

        # Check file extension — only care about R and Python analysis files
        suffix = target.suffix.lower()
        if suffix not in (".r", ".rmd", ".qmd", ".py", ".ipynb"):
            return False

        # Check if in an analysis-relevant directory
        parts = [p.lower() for p in target.parts]
        analysis_dirs = {"r", "python", "analysis", "scripts", "code", "src"}
        analysis_files = {"analyze", "analysis", "model", "regression", "mediation",
                          "moderation", "process", "hypothesis", "test_h", "03_"}

        # Is it in an analysis directory?
        if any(d in analysis_dirs for d in parts):
            return True

        # Does the filename suggest analysis?
        stem = target.stem.lower()
        if any(kw in stem for kw in analysis_files):
            return True

        return False
    except Exception:
        return False


def find_prereg(cwd: str) -> Path | None:
    """Look for a pre-registration file in the project."""
    search_root = Path(cwd)
    candidates = [
        search_root / "docs" / "pre-registration.md",
        search_root / "docs" / "preregistration.md",
        search_root / "docs" / "pre-reg.md",
        search_root / "pre-registration.md",
        search_root / "preregistration.md",
    ]
    for path in candidates:
        if path.exists():
            return path

    # Search docs/ for any file with "prereg" in the name
    docs_dir = search_root / "docs"
    if docs_dir.is_dir():
        for f in docs_dir.iterdir():
            if "prereg" in f.name.lower() and f.is_file():
                return f

    return None


def advise(message: str) -> None:
    """Emit an advisory message (non-blocking)."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "decision": "approve",  # never block
            "message": message,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main() -> None:
    payload = read_hook_input()

    # Only act on Edit and Write results
    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        silent_pass()

    # Extract target file path
    file_path = get_target_path(payload)
    if not file_path:
        silent_pass()

    # Get CWD
    cwd = payload.get("cwd", os.getcwd())

    # Is this an analysis file?
    if not is_analysis_file(file_path, cwd):
        silent_pass()

    # Does a pre-registration exist?
    prereg = find_prereg(cwd)
    if prereg is None:
        silent_pass()

    # Advisory: you just edited analysis code and a pre-registration exists
    advise(
        f"PRE-REGISTRATION DRIFT CHECK: You just modified analysis code. "
        f"A pre-registration exists at {prereg.relative_to(Path(cwd))}. "
        f"Please verify this change aligns with the pre-registered analysis plan. "
        f"If this is a deviation, document it in docs/decisions/analysis-decisions.md "
        f"with the rationale."
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Fail open — never disrupt the researcher's work.
        silent_pass()
