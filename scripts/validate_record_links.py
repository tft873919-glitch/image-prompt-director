#!/usr/bin/env python3
"""Validate local file links in an image-prompt project record."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
PROMPT_RE = re.compile(r"_v\d+\.\d+\.\d+\.md$")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()

    record = args.record.expanduser().resolve()
    if not record.is_file():
        raise SystemExit(f"record file not found: {record}")
    if not record.name.endswith("_记录.md"):
        raise SystemExit("record filename must end with _记录.md")

    links = LINK_RE.findall(record.read_text(encoding="utf-8"))
    local_links = [link for link in links if not re.match(r"^[a-z]+://|^#|^mailto:", link)]
    if not any(PROMPT_RE.search(link) for link in local_links):
        raise SystemExit("record must link at least one versioned Prompt file")

    missing: list[str] = []
    for link in local_links:
        clean = unquote(link.strip().strip("<>"))
        target = (record.parent / clean).resolve()
        if not target.exists():
            missing.append(f"{link} -> {target}")

    if missing:
        for item in missing:
            print(f"FAIL: missing link target: {item}")
        raise SystemExit(1)
    print(f"PASS: {record} ({len(local_links)} local links)")


if __name__ == "__main__":
    main()
