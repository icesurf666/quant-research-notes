"""Fail when public files contain common credentials or private local paths."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "private macOS path": re.compile("/" + "Users" + r"/[^/\s]+/"),
}
FORBIDDEN_NAMES = {".env", ".env.local", "id_rsa", "id_ed25519"}


def public_worktree_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def main() -> None:
    findings: list[str] = []
    for path in public_worktree_files():
        if not path.is_file():
            continue
        if path.name in FORBIDDEN_NAMES:
            findings.append(f"forbidden filename: {path.relative_to(ROOT)}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {path.relative_to(ROOT)}")
    if findings:
        raise SystemExit("\n".join(findings))


if __name__ == "__main__":
    main()
