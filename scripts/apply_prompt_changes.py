#!/usr/bin/env python3
"""Create a bumped prompt version by applying compact JSON Pointer changes."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from bump_prompt import FILE_RE, bump, version_key
from validate_prompt_md import VERSION_DEPENDENCY_PATTERNS, compact_warnings, validate_document


def pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/") or pointer == "/":
        raise ValueError(f"JSON Pointer must target a field below the root: {pointer!r}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def list_index(part: str, length: int, pointer: str) -> int:
    if not part.isdigit():
        raise ValueError(f"list segment must be a non-negative integer in {pointer!r}")
    index = int(part)
    if index >= length:
        raise ValueError(f"list index out of range in {pointer!r}")
    return index


def parent_for(data: Any, parts: list[str], pointer: str) -> tuple[Any, str]:
    node = data
    for part in parts[:-1]:
        if isinstance(node, dict):
            if part not in node:
                raise ValueError(f"missing intermediate object key in {pointer!r}: {part!r}")
            node = node[part]
        elif isinstance(node, list):
            node = node[list_index(part, len(node), pointer)]
        else:
            raise ValueError(f"cannot traverse scalar value in {pointer!r}")
    return node, parts[-1]


def set_pointer(data: Any, pointer: str, value: Any) -> None:
    parts = pointer_parts(pointer)
    parent, leaf = parent_for(data, parts, pointer)
    if isinstance(parent, dict):
        parent[leaf] = value
    elif isinstance(parent, list):
        parent[list_index(leaf, len(parent), pointer)] = value
    else:
        raise ValueError(f"cannot set a child on scalar value in {pointer!r}")


def delete_pointer(data: Any, pointer: str) -> None:
    parts = pointer_parts(pointer)
    parent, leaf = parent_for(data, parts, pointer)
    if isinstance(parent, dict):
        if leaf not in parent:
            raise ValueError(f"object key does not exist in {pointer!r}")
        del parent[leaf]
    elif isinstance(parent, list):
        del parent[list_index(leaf, len(parent), pointer)]
    else:
        raise ValueError(f"cannot delete a child from scalar value in {pointer!r}")


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"{label} file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{label} must contain valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{label} JSON must be an object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--kind", choices=("major", "minor", "patch"), required=True)
    parser.add_argument("--changes", type=Path, required=True)
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    changes_path = args.changes.expanduser().resolve()
    match = FILE_RE.match(source.name)
    if not match:
        raise SystemExit("source filename must match <中文项目名>_vX.Y.Z.md")

    source_data = load_object(source, "source")
    old_version = match.group("version")
    try:
        key = version_key(source_data)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if source_data.get(key) != old_version:
        raise SystemExit(f"source {key} does not match filename")

    changes = load_object(changes_path, "changes")
    unexpected = set(changes) - {"set", "delete"}
    if unexpected:
        raise SystemExit(f"changes has unexpected fields: {sorted(unexpected)}")
    set_values = changes.get("set", {})
    delete_values = changes.get("delete", [])
    if not isinstance(set_values, dict):
        raise SystemExit("changes.set must be an object of JSON Pointer to value")
    if not isinstance(delete_values, list) or not all(isinstance(item, str) for item in delete_values):
        raise SystemExit("changes.delete must be an array of JSON Pointer strings")
    if not set_values and not delete_values:
        raise SystemExit("changes must contain at least one set or delete operation")
    managed_version_paths = {"/prompt_version", "/style_version"}
    if managed_version_paths.intersection(set_values) or managed_version_paths.intersection(delete_values):
        raise SystemExit("prompt_version/style_version is managed by the script and cannot appear in changes")

    updated = copy.deepcopy(source_data)
    try:
        for pointer in delete_values:
            delete_pointer(updated, pointer)
        for pointer, value in set_values.items():
            set_pointer(updated, pointer, value)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    new_version = bump(old_version, args.kind)
    updated[key] = new_version
    destination = source.with_name(f"{match.group('name')}_v{new_version}.md")
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination}")

    text = json.dumps(updated, ensure_ascii=False, indent=2) + "\n"
    errors: list[str] = []
    validate_document(updated, new_version, errors)
    for pattern in VERSION_DEPENDENCY_PATTERNS:
        dependency = pattern.search(text)
        if dependency:
            errors.append(
                "prompt must be self-contained; expand cross-version dependency instead of using: "
                f"{dependency.group(0)!r}"
            )
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)

    destination.write_text(text, encoding="utf-8")
    for warning in compact_warnings(updated, text):
        print(f"WARN: {warning}")
    print(f"PASS: {destination}")


if __name__ == "__main__":
    main()
