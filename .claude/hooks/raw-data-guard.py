#!/usr/bin/env python3
"""
PreToolUse hook: block any Edit or Write to files under data/raw/.

Raw data is sacred — principle #1 of the research-methods skill suite.
Cleaning code reads from data/raw/ and writes to data/processed/.
The raw data is never modified, overwritten, or deleted.

Behavior:
  - Fires before every Edit or Write tool call
  - Checks if the target file path is under data/raw/
  - If yes: blocks the tool call with a clear error message
  - If no: passes through silently

Fail-open: errors in this hook never block the researcher's work.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def fail_open() -> None:
    """Exit silently, letting the tool call through unmodified."""
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
    """Extract the file path from the tool input.

    Edit tool: payload.tool_input.file_path
    Write tool: payload.tool_input.file_path
    """
    tool_input = payload.get("tool_input", {})
    if isinstance(tool_input, dict):
        return tool_input.get("file_path")
    return None


def is_under_data_raw(file_path: str, cwd: str) -> bool:
    """Check if the target path is under any data/raw/ directory."""
    try:
        target = Path(file_path)
        # Handle relative paths by resolving against CWD
        if not target.is_absolute():
            target = Path(cwd) / target
        target = target.resolve()

        # Check if any parent directory sequence contains data/raw
        parts = target.parts
        for i in range(len(parts) - 1):
            if parts[i] == "data" and i + 1 < len(parts) and parts[i + 1] == "raw":
                return True
        return False
    except Exception:
        return False


def block(reason: str) -> None:
    """Block the tool call with an error message."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "decision": "block",
            "reason": reason,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main() -> None:
    payload = read_hook_input()

    # Only act on Edit and Write tool calls
    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        fail_open()

    # Extract target file path
    file_path = get_target_path(payload)
    if not file_path:
        fail_open()

    # Get CWD for resolving relative paths
    cwd = payload.get("cwd", os.getcwd())

    # Check if the target is under data/raw/
    if is_under_data_raw(file_path, cwd):
        block(
            "BLOCKED: Raw data is sacred. Files under data/raw/ must never be "
            "modified. Cleaning code should read from data/raw/ and write to "
            "data/processed/. If you need to fix the raw data itself, do so "
            "outside of Claude Code and re-import."
        )

    # Not a raw data file — allow the tool call
    fail_open()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Fail open — never block the researcher's work due to hook errors.
        fail_open()
