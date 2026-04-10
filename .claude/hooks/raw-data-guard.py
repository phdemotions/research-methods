#!/usr/bin/env python3
"""
PreToolUse hook: prevent any modification to files in data/raw/.

Raw data is sacred — principle #1 of the research-methods suite.
This hook blocks Edit and Write tool calls that target any file
under a data/raw/ directory in the current project.

Fires on: Edit, Write
Fails open: if anything goes wrong, the tool call proceeds.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail_open() -> None:
    """Exit silently, letting the tool call through."""
    sys.exit(0)


def block(reason: str) -> None:
    """Block the tool call with an explanation."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "decision": "block",
            "reason": reason,
        }
    }
    print(json.dumps(output))
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
    """Extract the file path from an Edit or Write tool call."""
    tool_input = payload.get("tool_input", {})
    # Edit uses "file_path", Write uses "file_path"
    return tool_input.get("file_path")


def is_under_raw_data(file_path: str, cwd: str) -> bool:
    """Check if the file path is under any data/raw/ directory."""
    try:
        resolved = Path(file_path).resolve()
        # Check if "data/raw" appears in the path
        parts = resolved.parts
        for i, part in enumerate(parts):
            if part == "data" and i + 1 < len(parts) and parts[i + 1] == "raw":
                return True
        return False
    except Exception:
        return False


def main() -> None:
    payload = read_hook_input()

    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        fail_open()

    target_path = get_target_path(payload)
    if not target_path:
        fail_open()

    cwd = payload.get("cwd", "")

    if is_under_raw_data(target_path, cwd):
        block(
            "BLOCKED: Cannot modify files in data/raw/. "
            "Raw data is sacred and must never be modified. "
            "Write transformed data to data/processed/ instead. "
            "If you need to fix a data issue, document it in "
            "docs/decisions/ and handle it in your cleaning script."
        )

    fail_open()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        fail_open()
