"""Freeze or verify an article study's evidence, claims, and local artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain an object")
    return value


def tracked_files(study: Path, config: dict) -> list[str]:
    return sorted(set(["devto_article.md", "audit.json", *config["files"]]))


def verify(study: Path, *, freeze: bool) -> None:
    config = load(study / "audit.json")
    article = (study / "devto_article.md").read_text(encoding="utf-8")
    failures: list[str] = []

    evidence = study / config["evidence_file"]
    evidence_hash = sha256(evidence)
    if evidence_hash not in article:
        failures.append("article does not contain the current evidence SHA-256")
    for text in config["required_text"]:
        if text not in article:
            failures.append(f"missing required text: {text}")
    for text in config["banned_text"]:
        if text.lower() in article.lower():
            failures.append(f"contains banned text: {text}")
    for relative in tracked_files(study, config):
        if not (study / relative).is_file():
            failures.append(f"missing artifact: {relative}")

    manifest_path = study / "manifest.json"
    hashes = {
        relative: sha256(study / relative)
        for relative in tracked_files(study, config)
        if (study / relative).is_file()
    }
    if freeze and not failures:
        manifest_path.write_text(
            json.dumps({"study": study.name, "sha256": hashes}, indent=2) + "\n",
            encoding="utf-8",
        )
    elif not freeze:
        manifest = load(manifest_path)
        if manifest.get("sha256") != hashes:
            failures.append("manifest hashes do not match current artifacts")

    if failures:
        raise SystemExit("\n".join(failures))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("study", type=Path)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    verify(args.study.resolve(), freeze=args.freeze)


if __name__ == "__main__":
    main()
