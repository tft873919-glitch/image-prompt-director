#!/usr/bin/env python3
"""Create or fast-forward the shared lightweight Prompt Cookbook cache."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


REPO_URL = "https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook.git"
BRANCH = "main"
SPARSE_PATHS = (
    "/README.zh-CN.md",
    "/docs/CATALOG.md",
    "/schemas/style-v2.1.schema.json",
    "/styles/*/style.json",
    "/assets/thumbs/*",
)


def default_cache() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "cache" / "image-prompt-director" / "cookbook"


def run(args: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, check=check, text=True, capture_output=True)


def git(cache: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", "-C", str(cache), *args], check=check)


def configure_sparse(cache: Path) -> None:
    git(cache, "sparse-checkout", "set", "--no-cone", *SPARSE_PATHS)


def validate(cache: Path) -> tuple[int, int, list[str]]:
    required = (
        cache / "README.zh-CN.md",
        cache / "docs" / "CATALOG.md",
        cache / "schemas" / "style-v2.1.schema.json",
    )
    missing_required = [str(path) for path in required if not path.is_file()]
    styles = sorted((cache / "styles").glob("*/style.json"))
    thumbs = sorted((cache / "assets" / "thumbs").glob("*.jpg"))
    if missing_required or not styles or not thumbs:
        details = missing_required or ["style JSON or thumbnail set is empty"]
        raise RuntimeError("cache validation failed: " + "; ".join(details))

    thumb_names = {path.name for path in thumbs}
    missing_thumbs = [
        style.parent.name
        for style in styles
        if f"{style.parent.name}-16x9.jpg" not in thumb_names
    ]
    return len(styles), len(thumbs), missing_thumbs


def current_commit(cache: Path) -> str:
    return git(cache, "rev-parse", "HEAD").stdout.strip()


def remote_commit(cache: Path) -> str | None:
    result = git(cache, "ls-remote", "origin", f"refs/heads/{BRANCH}", check=False)
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.split()[0]


def initialize(cache: Path) -> str:
    cache.parent.mkdir(parents=True, exist_ok=True)
    run([
        "git", "clone", "--filter=blob:none", "--depth", "1", "--sparse",
        "--branch", BRANCH, REPO_URL, str(cache),
    ])
    configure_sparse(cache)
    return "INITIALIZED"


def update(cache: Path) -> str:
    origin = git(cache, "remote", "get-url", "origin").stdout.strip()
    if origin.rstrip("/") != REPO_URL.rstrip("/"):
        raise RuntimeError(f"unexpected cache origin: {origin}")
    if git(cache, "status", "--porcelain").stdout.strip():
        raise RuntimeError("cache has local changes; refusing to overwrite them")

    configure_sparse(cache)
    local = current_commit(cache)
    remote = remote_commit(cache)
    if remote is None:
        return "OFFLINE_CACHE"
    if remote == local:
        return "UP_TO_DATE"

    result = git(cache, "pull", "--ff-only", "origin", BRANCH, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"cache update failed without modifying local files: {detail}")
    return "UPDATED"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=default_cache())
    args = parser.parse_args()

    if shutil.which("git") is None:
        raise SystemExit("git is required to sync the Cookbook cache")

    cache = args.cache.expanduser().resolve()
    try:
        if (cache / ".git").is_dir():
            status = update(cache)
        elif cache.exists():
            raise RuntimeError(f"cache path exists but is not a git repository: {cache}")
        else:
            status = initialize(cache)

        styles, thumbs, missing_thumbs = validate(cache)
        commit = current_commit(cache)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc

    print(f"{status}: {cache}")
    print(f"commit={commit} styles={styles} thumbnails={thumbs}")
    if missing_thumbs:
        print("WARNING: missing thumbnails for " + ", ".join(missing_thumbs))


if __name__ == "__main__":
    main()
