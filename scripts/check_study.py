"""Validate a public study's claims, limitations, figures, and frozen hashes."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_study.py STUDY_DIRECTORY")
    study = Path(sys.argv[1]).resolve()
    metrics = load_json(study / "evidence" / "metrics.json")
    manifest = load_json(study / "manifest.json")
    article = (study / "article.md").read_text(encoding="utf-8")

    failures: list[str] = []
    for display in metrics["locked_displays"]:
        if display not in article:
            failures.append(f"article is missing locked display: {display}")
    for limitation in metrics["limitations"]:
        if limitation not in article:
            failures.append(f"article is missing limitation: {limitation}")
    for banned in metrics["banned_claims"]:
        if banned.lower() in article.lower():
            failures.append(f"article contains banned claim: {banned}")
    for marker in metrics["required_code_markers"]:
        if marker not in article:
            failures.append(f"article is missing required code marker: {marker}")
    for relative, expected in manifest["sha256"].items():
        path = study / relative
        if not path.is_file():
            failures.append(f"manifest file is missing: {relative}")
        elif sha256(path) != expected:
            failures.append(f"hash drift: {relative}")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
