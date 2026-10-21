"""Verify frozen headline values and artifact hashes for this public package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

STUDY = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    results = json.loads((STUDY / "evidence" / "results.json").read_text(encoding="utf-8"))
    manifest = json.loads((STUDY / "manifest.json").read_text(encoding="utf-8"))

    assert results["simulation"]["event_count"] == 14399
    assert results["simulation"]["trading_days"] == 365
    assert results["event_level"]["naive_t_stat"] == 8.2
    assert results["day_block_diagnostic"]["t_stat"] == -1.66
    assert results["october_10_2025_sensitivity"]["event_count"] == 434
    assert results["october_10_2025_sensitivity"]["mean_net_bps"] == 835.0

    for relative_path, expected_hash in manifest["sha256"].items():
        actual_hash = sha256(STUDY / relative_path)
        assert actual_hash == expected_hash, f"hash drift: {relative_path}"

    print("day-block-t-diagnostic: evidence snapshot and manifest verified")


if __name__ == "__main__":
    main()
