#!/usr/bin/env python3
"""Copy a render prompt or style spec and bump its semantic version."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FILE_RE = re.compile(r"^(?P<name>.+)_v(?P<version>\d+\.\d+\.\d+)\.md$")


def bump(version: str, kind: str) -> str:
    major, minor, patch = (int(part) for part in version.split("."))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def version_key(data: dict[str, object]) -> str:
    keys = [key for key in ("prompt_version", "style_version") if key in data]
    if len(keys) != 1:
        raise ValueError("JSON must contain exactly one version field: prompt_version or style_version")
    return keys[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--kind", choices=("major", "minor", "patch"), required=True)
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"source file not found: {source}")

    match = FILE_RE.match(source.name)
    if not match:
        raise SystemExit("filename must match <中文项目名>_vX.Y.Z.md")

    old_version = match.group("version")
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"source must contain only one valid JSON object: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("source JSON must be an object")
    try:
        key = version_key(data)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if data.get(key) != old_version:
        raise SystemExit(f"source {key} does not match filename")

    new_version = bump(old_version, args.kind)
    destination = source.with_name(f"{match.group('name')}_v{new_version}.md")
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination}")

    text = source.read_text(encoding="utf-8")
    updated, count = re.subn(
        rf'("{key}"\s*:\s*)"{re.escape(old_version)}"',
        rf'\1"{new_version}"',
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"expected exactly one JSON {key}")
    try:
        json.loads(updated)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"version replacement produced invalid JSON: {exc}") from exc

    destination.write_text(updated, encoding="utf-8")
    print(destination)


if __name__ == "__main__":
    main()
